import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#Database name
sqlite_file_name = "../database.sqlite"
#Path fot this file
base_dir = os.path.dirname(os.path.realpath(__file__))

#Connecting to database 
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

#Database motor,"echo=True" to show trough console what is being done
engine = create_engine(database_url, echo=True)

#Session to connect with the database
Session = sessionmaker(bind=engine)

#Handle the database tables
Base = declarative_base()