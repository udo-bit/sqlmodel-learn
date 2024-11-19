## 1. 创建表

```python
from sqlmodel import SQLModel,Field,create_engine,Session

engine = create_engine("sqlite:///database.db")

# 定义表
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

# 创建表
SQLModel.metadata.create_all(engine)
```

## 2. 插入数据

- session.commit 添加数据后，此时数据被标记为 expire, 无法打印实例，但是可以访问实例属性
- 使用 session.refresh(obj) 刷新数据，可以即时打印实例

```python
from sqlmodel import Field, Session, SQLModel, create_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    print("Before interacting with the database")
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        print("After adding to the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        session.commit()

        print("After committing the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        print("After committing the session, show IDs")
        print("Hero 1 ID:", hero_1.id)
        print("Hero 2 ID:", hero_2.id)
        print("Hero 3 ID:", hero_3.id)

        print("After committing the session, show names")
        print("Hero 1 name:", hero_1.name)
        print("Hero 2 name:", hero_2.name)
        print("Hero 3 name:", hero_3.name)

        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)

        print("After refreshing the heroes")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

    print("After the session closes")
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)

def main():
    create_db_and_tables()
    create_heroes()

if __name__ == "__main__":
    main()
```

## 3. select 查询数据

- ession.exec(select(Hero)) 得到一个可迭代对象，可以使用 for 循环进行遍历
- session.exec(select(Hero)).all() 得到一个对象列表，可以直接打印

```python
def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print(heroes)
```

## 4. where 条件查询

- where 中的逻辑判断包括：
  - or\_() 表示或
  - 用\,隔开多个条件表示与
  - 多个 where 语句表示与
  - 此外还支持 >= , <= , != , in\_ 等操作
- col() 修饰对象属性，可以声明属性为数据表的列，避免出现类似 None 和数字无法比较的问题
- in\_是 sqlmodel 的内置函数，用于判断某个值是否在某个范围内,不需要 import 引入

```python
def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(col(Hero.age) >= 35).where(Hero.age.in_(range(35,37)))
        results = session.exec(statement)
        for hero in results:
            print(hero)
```

## 5. 添加索引

- 添加索引可以提高查询效率

```python
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
```

## 6. 读取一行数据

- first() 读取第一行数据,为空时返回 None,为空或多于一行不报错
- one() 读取一行数据,为空时报错,多于一行也报错
- get() 根据 id 获取数据

```python
# 读取第一行数据
with Session(engine) as session:
    session.exec(select(Heror).where(Hero.id == 1)).first()
# 仅有一条数据，为空或多于一条数据都会报错
with Session(engine) as session:
    session.exec(select(Heror).where(Hero.id == 1)).one()
# 根据id获取数据
with Session(engine) as session:
    session.get(Hero, 1)
```

## 7. Offect 和 Limit

```python
def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age > 32).offset(1).limit(2)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
```

## 8. 更新数据

1. 查找数据对象
2. 修改数据对象
3. 将修改后的数据对象加入 session
4. session.commit() 提交修改

```python
with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    results = session.exec(statement)
    hero_1 = results.one()
    print("Hero 1:", hero_1)

    statement = select(Hero).where(Hero.name == "Captain North America")
    results = session.exec(statement)
    hero_2 = results.one()
    print("Hero 2:", hero_2)

    hero_1.age = 16
    hero_1.name = "Spider-Youngster"
    # 将更新后的对象加入 session
    session.add(hero_1)

    hero_2.name = "Captain North America Except Canada"
    hero_2.age = 110
    # 将更新后的对象加入 session
    session.add(hero_2)

    # 同时更新多条数据
    session.commit()
    # 刷新数据
    session.refresh(hero_1)
    session.refresh(hero_2)

    print("Updated hero 1:", hero_1)
    print("Updated hero 2:", hero_2)
```

## 9. 删除数据

1. 查找数据对象
2. session.delete() 删除数据对象
3. session.commit() 提交删除

```python

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Youngster")
    results = session.exec(statement)
    hero = results.one()
    print("Hero: ", hero)

    session.delete(hero)
    session.commit()
```

## 10. 表关联

### 10.1 定义外键

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    team_id: int|None = Field(default=None,foreign_key = "team.id")
```

### 10.2 内连接

```python
with Session(engine) as session:
    # 方式一：join
    # 将 Hero和Team同时放入select中为了在结果中能引用到Team
    # 省略on,因为Hero中有team_id字段，Team中有id字段，定义了外键
    statement = select(Hero, Team).join(Team)
    results = session.exec(statement)
    # 结果是一个包含Hero和Team的元组的可迭代对象
    for hero, team in results:
        print("Hero:", hero, "Team:", team)
    # 方式二：
    with Session(engine) as session:
        statement = select(Hero, Team).where(Hero.team_id == Team.id)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)
```

### 10.3 外连接

- 使用 isouter=True 表示外连接

```python
with Session(engine) as session:
    # Hero左连接Team
    statement = select(Hero, Team).join(Team,Hero.id == Team.id isouter=True)
    # Hero右连接Team
    # statement = select(Hero, Team).join(Hero, Hero.id == Team.id, isouter=True)
    results = session.exec(statement)
    for hero, team in results:
        print("Hero:", hero, "Team:", team)

```

### 10.4 定义关联属性

```python
class Team(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str
    heroes:List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str
    sec_name:str
    age:Optional[int] = None
    team_id:Optional[int] = Field(default=None,foreign_key="team.id")
    team: Team |None = Relationship(back_populates="heroes")
```

### 10.5 通过关联属性添加数据

- 不需要再单独对 Team 进行 add 和 commit，直接对 Hero 进行添加即可,反之亦然

```python
with Session(engine) as session:
    team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

    hero_deadpond = Hero(
        name="Deadpond", secret_name="Dive Wilson", team=team_z_force
    )
    hero_rusty_man = Hero(
        name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
    )
    hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    session.add(hero_deadpond)
    session.add(hero_rusty_man)
    session.add(hero_spider_boy)
    session.commit()

    session.refresh(hero_deadpond)
    session.refresh(hero_rusty_man)
    session.refresh(hero_spider_boy)

    print("Created hero:", hero_deadpond)
    print("Created hero:", hero_rusty_man)
    print("Created hero:", hero_spider_boy)
```

### 10.6 通过关联属性查询数据

```python
with Session(engine) as session:
    statement = select(Team).where(Team.name == "Preventers")
    result = session.exec(statement)
    team_preventers = result.one()

    # 通过属性即可查到关联数据
    print("Preventers heroes:", team_preventers.heroes)

```

### 10.7 通过关联属性更新数据

```python
with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    result = session.exec(statement)
    hero_spider_boy = result.one()

    # 将关联属性置为 None
    hero_spider_boy.team = None
    session.add(hero_spider_boy)
    session.commit()

    session.refresh(hero_spider_boy)
    print("Spider-Boy without team:", hero_spider_boy)
```

## 11. 级联操作

### 11.1 父表删除时级联删除子表

- 当 Team 中的数据被删除时，与之相关的 Hero 中的数据也会被删除

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team", cascade_delete=True)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="CASCADE")
    team: Team | None = Relationship(back_populates="heroes")
```

### 11.2 父表删除时，子表关联属性置为 None

- 当 Team 中的数据被删除时，与之相关的 Hero 中的数据的 team_id 属性会被置为 None
- 可以在 Team 中的 heroes 属性中添加 passive_deletes="all"
- 默认为这种方式，但是如果直接通过 sql 语句删除数据，Hero 表中的 team_id 会继续保留不存在的 Team 的 id

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(
        default=None, foreign_key="team.id", ondelete="SET NULL"
    )
    team: Team | None = Relationship(back_populates="heroes")
```

### 11.3 父表删除时，如果子表中有与之关联的数据，会删除失败并报错

- 在父表中 Relationship 中设置 passive_deletes="all"
- 在子表中 Field 中设置 ondelete="RESTRICT"
- 删除父表时，首先将子表中数据设置为 None，然后再删除父表

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team", passive_deletes="all")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(
        default=None, foreign_key="team.id", ondelete="RESTRICT"
    )
    team: Team | None = Relationship(back_populates="heroes")

with Session(engine) as session:
    statement = select(Team).where(Team.name == "Wakaland")
    team = session.exec(statement).one()
    # 将子表中与之相关的数据的关联字段置为None
    team.heroes.clear()
    session.add(team)
    session.commit()
    session.refresh(team)
    print("Team with removed heroes:", team)
```

## 12. 多对多关联

### 12.1 建立多对多关联关系

- 中间表中可以有多个主键
- 实体表不再需要 foreign_key 字段
- 实体表 Relationship 属性中增加 link_model 属性指向中间表

```python
# 中间表
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)
```

### 12.2 向多对多实体表中添加数据

```python
with Session(engine) as session:
    team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

    hero_deadpond = Hero(
        name="Deadpond",
        secret_name="Dive Wilson",
        teams=[team_z_force, team_preventers],
    )
    hero_rusty_man = Hero(
        name="Rusty-Man",
        secret_name="Tommy Sharp",
        age=48,
        teams=[team_preventers],
    )
    hero_spider_boy = Hero(
        name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
    )
    session.add(hero_deadpond)
    session.add(hero_rusty_man)
    session.add(hero_spider_boy)
    session.commit()

    session.refresh(hero_deadpond)
    session.refresh(hero_rusty_man)
    session.refresh(hero_spider_boy)

    print("Deadpond:", hero_deadpond)
    print("Deadpond teams:", hero_deadpond.teams)
    print("Rusty-Man:", hero_rusty_man)
    print("Rusty-Man Teams:", hero_rusty_man.teams)
    print("Spider-Boy:", hero_spider_boy)
    print("Spider-Boy Teams:", hero_spider_boy.teams)
```

### 12.3 更新或删除多对多实体表中的数据

```python
with Session(engine) as session:
    hero_spider_boy = session.exec(
        select(Hero).where(Hero.name == "Spider-Boy")
    ).one()
    team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

    team_z_force.heroes.append(hero_spider_boy)
    session.add(team_z_force)
    session.commit()

    print("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
    print("Z-Force heroes:", team_z_force.heroes)

    hero_spider_boy.teams.remove(team_z_force)
    session.add(team_z_force)
    session.commit()

    print("Reverted Z-Force's heroes:", team_z_force.heroes)
    print("Reverted Spider-Boy's teams:", hero_spider_boy.teams)
```

### 12.4 在中间表中增加额外字段

```python
# 修改中间表
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    is_training: bool = False

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")

# 修改实体表
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    hero_links: list[HeroTeamLink] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_links: list[HeroTeamLink] = Relationship(back_populates="hero")


# 添加初始数据
with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
        )
        deadpond_team_z_link = HeroTeamLink(team=team_z_force, hero=hero_deadpond)
        deadpond_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_deadpond, is_training=True
        )
        spider_boy_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_spider_boy, is_training=True
        )
        rusty_man_preventers_link = HeroTeamLink(
            team=team_preventers, hero=hero_rusty_man
        )

        session.add(deadpond_team_z_link)
        session.add(deadpond_preventers_link)
        session.add(spider_boy_preventers_link)
        session.add(rusty_man_preventers_link)
        session.commit()

        for link in team_z_force.hero_links:
            print("Z-Force hero:", link.hero, "is training:", link.is_training)

        for link in team_preventers.hero_links:
            print("Preventers hero:", link.hero, "is training:", link.is_training)

# 添加数据
with Session(engine) as session:
    hero_spider_boy = session.exec(
        select(Hero).where(Hero.name == "Spider-Boy")
    ).one()
    team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

    spider_boy_z_force_link = HeroTeamLink(
        team=team_z_force, hero=hero_spider_boy, is_training=True
    )
    team_z_force.hero_links.append(spider_boy_z_force_link)
    session.add(team_z_force)
    session.commit()

    print("Updated Spider-Boy's Teams:", hero_spider_boy.team_links)
    print("Z-Force heroes:", team_z_force.hero_links)

# 更新数据
with Session(engine) as session:
    # Code here omitted
    for link in hero_spider_boy.team_links:
        if link.team.name == "Preventers":
            link.is_training = False
    session.add(hero_spider_boy)
    session.commit()
    for link in hero_spider_boy.team_links:
        print("Spider-Boy team:", link.team, "is training:", link.is_training)
```
