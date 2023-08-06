from typing import List, Dict

from .client import FlagsupClient
from .utils import EvaluateRequest
from .constants import Constant


class CachedFlagsupClient(FlagsupClient):
    def __init(self, target_host=Constant.DEFAULT_TARGET_HOST):
        super().__init__(target_host)
        self._flags = {}
        self._evals = {}

    def evaluate_flag(self, flag_key: str, entity_id: str,
                      default_status: bool = False, default_treatment: str = "",
                      default_exp_id: int = 0, default_branch_id: int = 0) -> Dict:
        """
        Fetch a flag value for the logged in user. Response is cached in memory for subsequent calls.
        :param flag_key: flag key (name) to fetch
        :param entity_id: user ID from IAM service
        :param default_status: default status to return in case of errors
        :param default_treatment: (experiment only) default treatment to return in case of errors
        :param default_exp_id: (experiment only) default experiment to return in case of errors
        :param default_branch_id: (experiment only) default branch to return in case of errors
        :return: dict {
            "enabled": flag status,
            "treatment": treatment,
            "exp_id": exp ID,
            "exp_branch_id": exp branch ID
        }
        """

        # Cache hit, return
        if (flag_key, entity_id) in self._flags:
            return self._evals[flag_key, entity_id]

        # Cache miss, call FlagSup server
        flag = super().evaluate_flag(flag_key, entity_id,
                                     default_status, default_treatment, default_exp_id, default_branch_id)

        # Save to cache
        self._evals[flag_key, entity_id] = flag

        return flag

    def get_flag_status(self, flag_key: str, default_status: bool = False) -> bool:
        """
        Fetch a flag value without user ID. Response is cached in memory for subsequent calls.
        :param flag_key: flag key (name) to fetch
        :param default_status: default status to return in case of errors
        :return: bool, flag status
        """
        # Cache hit, return
        if flag_key in self._flags:
            return self._flags[flag_key]

        # Cache miss, call FlagSup server
        flag = super().get_flag_status(flag_key, default_status)

        # Save to cache
        self._flags[flag_key] = flag

        return flag

    def batch_evaluate_flag(self, reqs: List[EvaluateRequest],
                            default_status: bool = False, default_treatment: str = "",
                            default_exp_id: int = 0, default_branch_id: int = 0) -> List[Dict]:
        """
        Fetch a flag value for the logged in user. Response is cached in memory for subsequent calls.
        :param reqs: a list of EvaluateRequest
        :param default_status: default status to return in case of errors
        :param default_treatment: (experiment only) default treatment to return in case of errors
        :param default_exp_id: (experiment only) default experiment to return in case of errors
        :param default_branch_id: (experiment only) default branch to return in case of errors
        :return: [{
            "flag_key": str, flag key,
            "entity_id": str, user id,
            "enabled": bool, flag status,
            "treatment": str, treatment,
            "exp_id": int, exp ID,
            "exp_branch_id": int, exp branch ID
        }]
        """
        cache_hit = all([(req.flag_key, req.entity_id) in self._evals for req in reqs])
        # Cache hit, return
        if cache_hit:
            return [{
                "flag_key": req.flag_key,
                "entity_id": req.entity_id,
                **self._evals[req.flag_key, req.entity_id]
            } for req in reqs]

        # Cache miss, call FlagSup server
        batch_response = super().batch_evaluate_flag(reqs, default_status, default_treatment, default_exp_id, default_branch_id)

        # Save to cache
        for response in batch_response:
            self._evals[(response["flag_key"], response["entity_id"])] = response

        return batch_response

    def batch_get_flag_status(self, flag_keys: List[str], default_status: bool = False) -> List[Dict]:
        """
        Fetch a flag value for the logged in user. Response is cached in memory for subsequent calls.
        :param flag_keys: a list of EvaluateRequest
        :param default_status: default status to return in case of errors
        :return: [dict {
            "flag_key": str, flag key,
            "enabled": bool, flag status,
        }]
        """
        cache_hit = all([flag_key in self._flags for flag_key in flag_keys])
        # Cache hit, return
        if cache_hit:
            return [{
                "flag_key": flag_key,
                "enabled": self._flags[flag_key]
            } for flag_key in flag_keys]

        # Cache miss, call FlagSup server
        batch_response = super().batch_get_flag_status(flag_keys, default_status)

        # Save to cache
        for response in batch_response:
            self._flags[response["flag_key"]] = response

        return batch_response
