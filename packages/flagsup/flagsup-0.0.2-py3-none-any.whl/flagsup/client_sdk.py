from .constants import Constant
from logging import Logger
import requests


class FlagsupClient:

    def __init__(self, target_host=Constant.DEFAULT_TARGET_HOST):
        self.target_host = target_host
        self.flags = {}
        self.logger = Logger("flagsup_client")

    def post(self, endpoint, data, default):
        try:
            print("Hello posting")
            print("calling endpoint, endpoint=%s, data=%s", self.target_host + endpoint, data)
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

        # Cache hit, return
        if flag_key in self.flags:
            return self.flags[flag_key]

        # Cache miss, call FlagSup server
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

        # Save to cache
        self.flags[flag_key] = flag

        return flag

    def get_flag_status(self, flag_key, default_status=False):
        """
        Fetch a flag value without user ID. Response is cached in memory for subsequent calls.
        :param flag_key: flag key (name) to fetch
        :param default_status: default status to return in case of errors
        :return: dict {
            "enabled": flag status,
        }
        """

        # Cache hit, return
        if flag_key in self.flags:
            return self.flags[flag_key]

        # Cache miss, call FlagSup server
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

        # Save to cache
        self.flags[flag_key] = flag

        return flag
