import urllib


class Config(object):
  DEBUG = False
  TESTING = False
  # POSTGRES_URL = "127.0.0.1:5432"
  # POSTGRES_USER = "Simon"
  # POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
  # POSTGRES_DB = "shelter"

  # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
  #   user=POSTGRES_USER,
  #   pw=POSTGRES_PW,
  #   url=POSTGRES_URL,
  #   db=POSTGRES_DB)

  # params = urllib.parse.quote_plus(
  #    'DRIVER={SQL Server};SERVER=SBU\SQLEXPRESS;DATABASE=Shelter;Trusted_Connection=yes;')
  # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params

  SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://@SBU\\SQLEXPRESS/Shelter?driver=SQL+Server&trusted_connection=yes"

  SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
  pass


class DevelopmentConfig(Config):
  DEBUG = True
