import sqlalchemy as alch
import os
from dotenv import load_dotenv

def connecting():

    load_dotenv()

    dbName = "Before_Trilogy2"
    password=os.getenv("sql")


    connectionData = f"mysql+pymysql://root:{password}@localhost/{dbName}"
    return alch.create_engine(connectionData)