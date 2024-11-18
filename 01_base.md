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
    statement = select(Hero, Team).join(Team, isouter=True)
    results = session.exec(statement)
    for hero, team in results:
        print("Hero:", hero, "Team:", team)

```
