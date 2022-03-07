# config.py
SECRET_KEY = 'swsv3wd112da14'
SQLALCHEMY_DATABASE_URI = 'mysql://user108:#108user#@203.170.190.171:3306/108or'


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
