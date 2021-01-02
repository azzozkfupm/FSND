import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = False

# Connect to the database
ENV = 'prod'
if ENV == 'dev':
    DEBUG = True
# DATABASE URL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/Casting'

elif ENV == 'test':
    DEBUG = True
# DATABASE URL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/testCasting'

else:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://mvyfdfurasadmo:7afbd66cc44b56fa6b93ef6f85d12afab607bf138f661e2ea33e8878aafffdfb@ec2-54-159-107-189.compute-1.amazonaws.com:5432/dfvdhj4cgf9oru'

SQLALCHEMY_TRACK_MODIFICATIONS = False
