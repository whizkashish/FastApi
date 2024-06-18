from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#sqlite3
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

#pgsql
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456789@localhost/Todos'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#mysql
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Aa147147147#@127.0.0.1:3306/todos'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
