import os
from enum import Enum
from typing import Any, Dict


class DeployEnv(Enum):
    """
    Enum of supported environment names
    """

    LOCAL = "local"
    DEV = "development"
    TEST = "test"
    PERF = "performance"
    PRE_PROD = "pre-production"
    PROD = "production"


deploy_env = DeployEnv(os.getenv("DEPLOY_ENV", "development").lower())


def get_config(default_value: Any, env_config: Dict[DeployEnv, Any]) -> Any:
    """
    Provide a default value, then environment specific overrides, which will be applied if the prescribed environment
    is identified to be in use.
    :param default_value: The value to be used if a qualifying environment specific override is not found.
    :param env_config: A dictionary of Key (environment name), Value (environment specific value) pairs.
        Key: attribute of DeployEnv
        Value: Any
    :return: The qualified environment configuration value
    """
    return env_config.get(deploy_env, default_value)
