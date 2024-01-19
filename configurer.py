import logging
import yaml

config_file = './config.yaml'


def get_configuration():
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            return config

    except FileNotFoundError:
        logging.critical(f"Config File {config_file} not existing, please create it")
        exit(-1)

    except yaml.YAMLError as exc:
        logging.critical(f"Error : parse yaml file error, please check {config_file} format", exc_info=exc)
        exit(-1)
