from sqlmodel import SQLModel,create_engine,Session,select,Field, or_, and_
from typing import List,Optional

engine = create_engine("mysql+pymysql://root:gxl911025@localhost:3306/test")


class Hero(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str
    sec_name:str
    age:Optional[int] = None
    team_id:Optional[int] = Field(default=None,foreign_key="team.id")

class Team(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str


with Session(engine) as session:
    stmt = session.select(Hero,Team).left_join(Team).on(Hero.team_id == Team.id)
    heroes = session.exec(stmt)

    for hero,team in heroes:
        print(hero)







