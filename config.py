import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = "sdsd94234sddf324"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://shreyas:mysql*1729@mysql-17532-0.cloudclusters.net:17538/question_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
print(os.path.join(basedir,'app.db'))