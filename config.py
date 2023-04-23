import hydra
from omegaconf import OmegaConf

def to_container(config):
    return OmegaConf.to_container(config, resolve=True)

class Config:

    config_path = "conf"
    config_name = "config"

    def __init__(self):
        hydra.initialize(version_base=None, config_path=self.config_path)
        self.config = hydra.compose(config_name=self.config_name)

    def __enter__(self):
        return self.config

    def __exit__(self, exc_type, exc_value, traceback):
        """ TODO: store changes upon exiting context """
        pass
