import mongoorm
from config import config


def conn_init():
    aliases = (
        'db-jianfei',
    )
    for alias in aliases:
        mongoorm.register_connection(
            db_alias=alias,
            database=config[alias],
            host=config['mongo_host'],
            port=config['mongo_port'],
            username=config['mongo_username'],
            password=config['mongo_password'],
            authSource='admin',
        )
