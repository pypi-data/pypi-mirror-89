from logging import Logger
from typing import List, Dict
import requests

from .constants import Constant
from .utils import EvaluateRequest


class FlagsupClient:

    def __init__(self, target_host=Constant.DEFAULT_TARGET_HOST):
        self.target_host = target_host
        self.logger = Logger("flagsup_client")
        self.flags = {}
        self.evals = {}

    def post(self, endpoint, data, default):
        try:
            response = requests.post(self.target_host + endpoint, json=data)
            return response.json()
        except Exception as e:
            self.logger.warning(f"Error getting flag, endpoint={endpoint}, data={data}, error={e}")
            return default

    def evaluate_flag(self, flag_key: str, user_id: str,
                      default_status: bool = False, default_treatment: str = "",
                      default_exp_id: int = 0, default_branch_id: int = 0):
        """
        Fetch a flag value for the logged in user. Response is cached in memory for subsequent calls.
        :param flag_key: flag key (name) to fetch
        :param user_id: user ID from IAM service
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
        default_response = {
            "enabled": default_status,
            "treatment": default_treatment,
            "exp_id": default_exp_id,
            "exp_branch_id": default_branch_id
        }

        flag = self.post(
            Constant.EVALUATION_ENDPOINT,
            {
                "flag_key": flag_key,
                "entity_id": user_id
            },
            default_response
        )

        return flag

    def get_flag_status(self, flag_key, default_status=False):
        """
        Fetch a flag value without user ID. Response is cached in memory for subsequent calls.
        :param flag_key: flag key (name) to fetch
        :param default_status: default status to return in case of errors
        :return: bool, flag status
        """
        default_response = {
            "enabled": default_status,
        }

        flag = self.post(
            Constant.GET_STATUS_ENDPOINT,
            {
                "flag_key": flag_key
            },
            default_response
        )

        return flag["enabled"]

    def batch_evaluate_flag(self, reqs: List[EvaluateRequest],
                            default_status: bool = False, default_treatment: str = "",
                            default_exp_id: int = 0, default_branch_id: int = 0):
        """
        Fetch a flag value for the logged in user. Response is cached in memory for subsequent calls.
        :param reqs: a list of EvaluateRequest
        :param default_status: default status to return in case of errors
        :param default_treatment: (experiment only) default treatment to return in case of errors
        :param default_exp_id: (experiment only) default experiment to return in case of errors
        :param default_branch_id: (experiment only) default branch to return in case of errors
        :return: [{
            "flag_key": flag key,
            "entity_id": user id,
            "enabled": flag status,
            "treatment": treatment,
            "exp_id": exp ID,
            "exp_branch_id": exp branch ID
        }]
        """
        default_response = {
            "responses": [{
                "flag_key": req.flag_key,
                "entity_id": req.user_id,
                "enabled": default_status,
                "treatment": default_treatment,
                "exp_id": default_exp_id,
                "exp_branch_id": default_branch_id
            } for req in reqs]
        }

        batch_response = self.post(
            Constant.BATCH_EVALUATION_ENDPOINT,
            {
                "requests": list(map(lambda r: r.get_json(), reqs))
            },
            default_response
        )

        return batch_response["responses"]

    def batch_get_flag_status(self, flag_keys: List[str],
                              default_status: bool = False):
        """
        Fetch a flag value for the logged in user. Response is cached in memory for subsequent calls.
        :param flag_keys: a list of EvaluateRequest
        :param default_status: default status to return in case of errors
        :return: [dict {
            "flag_key": str, "flag key",
            "enabled": bool, "flag status",
        }]
        """
        default_response = {
            "responses": [{
                "flag_key": flag_key,
                "enabled": default_status,
            } for flag_key in flag_keys]
        }

        batch_response = self.post(
            Constant.BATCH_GET_STATUS_ENDPOINT,
            {
                "requests": [{
                    "flag_key": flag_key
                } for flag_key in flag_keys]
            },
            default_response
        )

        return batch_response["responses"]
