import os
import json
import logging.config


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    '''
    A simple logging config to be used globally (simple dictionary based config)
    :param default_path: path to logging config file JSON
    :param default_level: the default log level (def: INFO)
    :param env_key: the environment key
    '''

    path = os.path.join(os.path.dirname(__file__), default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value
        # print 'PATH', path
    if os.path.exists(path):
        # print 'PATH', path
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(filename='parser.log', level=default_level)
