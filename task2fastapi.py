#import config
import json
from typing import List
from azure.cosmosdb.table.models import Entity
from pydantic import BaseModel,Field
from azure.cosmosdb.table.tableservice import TableService
#from pydantic import BaseModel,Field
#import databases, sqlalchemy, datetime, uuid
from fastapi import Depends, FastAPI, HTTPException
#import azure.common
f = open('config.json') 
data = json.load(f) 
table_service = TableService(account_name=data['account_name'], account_key=data['account_key'])
"""def create_table(table_name):
    table_service.create_table(table_name)"""

#class UserFind(BaseModel):

class UserList(BaseModel):
    table: str=  Field(..., example = "potingg")
    partitionkey: str=  Field(..., example = "potingg")
    rowkey: str=  Field(..., example = "potingg")
    desc: str=  Field(..., example = "potingg")
    somee: str=  Field(..., example = "potingg")

class UserDelete(BaseModel):
    table: str=  Field(..., example = "potingg")
    partitionkey: str = Field(..., example = "Enter id")
    rowkey: str = Field(..., example = "Enter id")

class UserRead(BaseModel):
    table: str=  Field(..., example = "potingg")
    partitionkey: str = Field(..., example = "Enter id")
    rowkey: str = Field(..., example = "Enter id")

def enter_entity(table, partitionkey, rowkey, desc, somee ):
    task = Entity()
    task.PartitionKey = partitionkey
    task.RowKey = rowkey
    task.desc = desc
    task.somee = somee
    table_service.insert_entity(table, task)
    return {
        "table": table,
        "partitionkey": partitionkey,
        "rowkey": rowkey,
        "desc": task.desc,
        "somee": task.somee
    }

def read_entity(table, partitionkey, rowkey):
    task = table_service.get_entity(table, partitionkey, rowkey)
    return {
        "table": table,
        "partitionkey": partitionkey,
        "rowkey": rowkey,
        "desc": task.desc,
        "somee": task.somee
    }

def update_entity(table, partitionkey, rowkey, desc, somee):
    task = Entity()
    task.PartitionKey = partitionkey
    task.RowKey = rowkey
    task.desc = desc
    task.somee = somee
    #task = {'PartitionKey': partitionkey, 'RowKey': rowkey,
    #    'desc': desc, 'somee': somee}
    table_service.update_entity(table, task)
    return {
        "table": table,
        "partitionkey": partitionkey,
        "rowkey": rowkey,
        "desc": task.desc,
        "somee": task.somee }

def delete_entity(table, partitionkey, rowkey):
    table_service.delete_entity(table, partitionkey, rowkey)

app = FastAPI()
#get users
@app.get("/users", response_model = UserRead)
async def find_all_users(user: UserRead):
    return read_entity(user.table, user.partitionkey, user.rowkey)

# enter users
@app.post("/users", response_model = List[UserList])
async def register_user(user: UserList):#table: str, partitionkey: str, rowkey: str, desc: str, somee: str):
    return enter_entity(user.table, user.partitionkey, user.rowkey, user.desc, user.somee)

# update users
@app.put("/users", response_model=UserList)
async def update_user(user: UserList):
    return update_entity(user.table, user.partitionkey, user.rowkey, user.desc, user.somee)

# delete users
@app.delete("/users/{userid}")
async def delete_user(user: UserDelete):
    delete_entity(user.table, user.partitionkey, user.rowkey)
    return {
        "status": True,
        "message": "delete successful"}

#create_table('mytable1')
#enter_entity('table', '12','1','hfsdh', 'example')
#read_entity('table', '12', '1')
#update_entity('table', '1234', '12342', 'fasd', 'efas')
#delete_entity('table', '12', '1')
#read_entity('table', '1234', '12342')