import urllib


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://@SBU\\SQLEXPRESS/Shelter?driver=SQL+Server&trusted_connection=yes"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    youtube_dl_path = "D:\\_Prog\\Projects\\Shelter\\Shelter.back\\external\\youtube-dl.exe"
    ffmpeg_path = "D:\\_Prog\\Projects\\Shelter\\Shelter.back\\external\\ffmpeg.exe"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
