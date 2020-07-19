from typing import List
from pydantic import BaseModel,Field
import databases, sqlalchemy, datetime, uuid
from fastapi import Depends, FastAPI, HTTPException
DATABASE_URL = "mysql://user:password@localhost:3306/database_name"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table( "table_name", metadata,
    sqlalchemy.Column("id", sqlalchemy.String(200), primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(15)),
    sqlalchemy.Column("password", sqlalchemy.String(15)),
    sqlalchemy.Column("first_name", sqlalchemy.String(15)),
    sqlalchemy.Column("last_name", sqlalchemy.String(15)),
    sqlalchemy.Column("gender", sqlalchemy.CHAR),
    sqlalchemy.Column("create_at", sqlalchemy.String(250)),
    sqlalchemy.Column("status", sqlalchemy.CHAR))

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

# MODELS
class UserList(BaseModel):
    id: str
    username: str
    password: str
    first_name: str
    last_name: str
    gender: str
    create_at: str
    status: str
class UserEntry(BaseModel):
    username: str=  Field(..., example = "potingg")
    password: str=  Field(..., example = "potingg")
    first_name: str=  Field(..., example = "potin")
    last_name: str=  Field(..., example = "sablin")
    gender: str=  Field(..., example = "S")
class UserUpdate(BaseModel):
    id: str = Field(..., example = "your id plz")
    first_name: str=  Field(..., example = "potin")
    last_name: str=  Field(..., example = "sablin")
    gender: str=  Field(..., example = "S")
    status: str = Field(..., example ="1")
class UserDelete(BaseModel):
    id: str = Field(..., example = "Enter id")

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model = List[UserList])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.post("/users", response_model = UserList)
async def register_user(user: UserEntry):
    gID  = str(uuid.uuid1())
    gDate= str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username = user.username,
        password = user.password,
        first_name = user.first_name,
        last_name = user.last_name,
        gender = user.gender,
        create_at = gDate,
        status = "1"
    )
    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at": gDate,
        "status": "1"
    }

@app.get("/users/{userid}", response_model=UserList)
async def find_user_by_id(userid: str):
    query = users.select().where(users.c.id == userid)
    return await database.fetch_one(query)

@app.put("/users", response_model=UserList)
async def update_user(user: UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(user.id == user.id).\
        values(
        first_name = user.first_name,
        last_name = user.last_name,
        gender = user.gender,
        create_at = gDate,
    )
    await database.execute(query)
    return await find_user_by_id(user.id)

@app.delete("/users/{userid}")
async def delete_user(user:UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)
    return {
        "status": True,
        "message": "delete successful"
    }
