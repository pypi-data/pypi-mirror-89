import os
import pathlib

from yaml_pyconf.base import BaseConfig


class FlaskConfig(BaseConfig):
    def __new__(
            cls,
            yaml_path=pathlib.Path(__file__).parent.joinpath("samples").joinpath("sample-yaml").joinpath("flask-choose-env.yaml"),
            dotenv_path=pathlib.Path(__file__).parent.joinpath("samples").joinpath("sample-dotenv").joinpath(".env"),
    ):
        return super(FlaskConfig, cls).__new__(
            cls, yaml_path=yaml_path, dotenv_path=dotenv_path
        )

    @classmethod
    def select_config(cls, conf):
        conf = super(FlaskConfig, cls).select_config(conf)
        env = os.getenv("ENVIRONMENT")
        if env is not None:
            try:
                conf = conf[env]
                return conf
            except KeyError:
                raise NotImplementedError("The value set for 'ENVIRONMENT' attribute "
                                          "must match a section in your yaml config")
        else:
            raise NotImplementedError("You must set a variable called 'ENVIRONMENT', "
                                      "in your .env or by using "
                                      "'export ENVIRONMENT={yourEnvValue}, and "
                                      "{yourEnvValue} must match a section in your yaml "
                                      "file. If this doesn't make sense for your "
                                      "project, use SimpleConfig instead")

    @classmethod
    def set_dotenv_var_from_yaml_conf(cls, instance, conf, list_name="LOAD_FROM_ENV"):
        return super(FlaskConfig, cls).set_dotenv_var_from_yaml_conf(
            instance,
            conf,
            list_name=list_name
        )
