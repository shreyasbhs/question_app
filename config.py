import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = "sdsd94234sddf324"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql*1729@localhost/questionapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
print(os.path.join(basedir,'app.db'))