# app/database.py
from sqlmodel import SQLModel, create_engine , Session
from app import settings


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, 
    connect_args={"sslmode": "require"}, 
    pool_recycle=300 , 
    echo=bool(settings.DEBUG)      # Enable SQL echo based on DEBUG setting
)

def create_db_and_tables():
    print("Dubigging ...........",settings.DEBUG)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
