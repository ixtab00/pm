from sqlalchemy.orm import declarative_base, sessionmaker, relationship, mapped_column
from sqlalchemy import Column, Integer, String, BINARY, create_engine, ForeignKey

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "Credentials"
    id = Column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("Users.id"))
    account = Column(String)
    login = Column(String)
    password = Column(BINARY)
    iv = Column(BINARY)
    date = Column(String)
    user = relationship("User", back_populates="credentials")

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    credentials = relationship("Credentials", back_populates="user")

def init_DB(path: str):
    engine = create_engine(path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
