from sqlmodel import SQLModel,create_engine,Session,select,Field, or_, and_
from typing import List,Optional

engine = create_engine("mysql+pymysql://root:gxl911025@localhost:3306/test")


class Hero(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str
    sec_name:str
    age:Optional[int] = None
ids = [31,32]
with Session(engine) as session:
    stmt = select(Hero).where(Hero.id.in_(ids))
    heroes = session.exec(stmt)

    for hero in heroes:
        print(hero)







