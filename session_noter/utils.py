import yaml


def read_config_file():
    with open('./config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    return config
