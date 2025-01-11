from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Virtual Machine IP
IP = '192.168.56.102'

# Database URLs
# TO DO:
# make changes on master not replication_user
URL_DATABASE_MASTER = 'mysql+mysqlconnector://app_user:app_pass@' + IP + ':3306/car_rental_db'
URL_DATABASE_SLAVE = 'mysql+mysqlconnector://app_user:app_pass@' + IP + ':3307/car_rental_db'

# Engines
engine_master = create_engine(URL_DATABASE_MASTER, connect_args={"ssl_disabled": False, "ssl_cert": None, "ssl_ca": None, "ssl_key": None})
engine_slave = create_engine(URL_DATABASE_SLAVE)

# Sessions
SessionLocal_Master = sessionmaker(autocommit=False, autoflush=False, bind=engine_master)
SessionLocal_Slave = sessionmaker(autocommit=False, autoflush=False, bind=engine_slave)

# Base
Base = declarative_base()