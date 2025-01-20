from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import engine


def get_session() -> Session:
    with Session(autoflush=False, bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
