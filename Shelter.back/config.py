class Config(object):
    DEBUG = False
    TESTING = False
    POSTGRES_URL = "127.0.0.1:5432"
    POSTGRES_USER = "Simon"
    POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
    POSTGRES_DB = "shelter"

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER,
        pw=POSTGRES_PW,
        url=POSTGRES_URL,
        db=POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
