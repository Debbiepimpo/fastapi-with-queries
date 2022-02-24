
import string
import secrets

from fastapi import FastAPI
from auth import AuthByToken
from config import ConnectionDB

app = FastAPI()

db = ConnectionDB
@app.post("/")
async def user_token(username: str, password: str) -> None:
    conn = db.connection
    cursor = conn.cursor()
    cursor.execute("Select username, password, token from users")
    users = cursor.fetchall()
    for user in users:
        if user[0] == username and user[1] == password:
            return {"token": user[2]}

@app.post("/new_user")
async def create_user(username: str, password: str, token: str) -> None:
    auth = AuthByToken
    if auth.auth_by_token(token):
        alphabet = string.ascii_letters + string.digits
        new_token = ''.join(secrets.choice(alphabet) for i in range(8))
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO users(username, password, token) values ('{username}','{password}', '{new_token}')")
        conn.commit()
    return {"username": username, "token": new_token }

@app.post("/update_user")
async def update_user(username: str, password: str, token: str) -> None:
    auth = AuthByToken
    if auth.auth_by_token:
        conn = db.connection
        cursor = conn.cursor()
        q = " UPDATE users set "
        if  auth.auth_by_token(username) != username and auth.auth_by_token(password) != password:
            cursor.execute(q + f"username = '{username}', password = '{password}'  where token = '{token}'")
            conn.commit()
        elif auth.auth_by_token(username) != username:
            cursor.execute(q + f"username = '{username}' where token = '{token}'")
            conn.commit()
        elif auth.auth_by_token(password) != password:
            cursor.execute(q + f", password = '{password}' where token = '{token}")
            conn.commit()
    return {"username": username, "token": token}

@app.delete("/delete_user")
async def delete_user(id: int) -> None:
    auth = AuthByToken
    if auth.auth_by_token:
        conn = db.connection
        cursor = conn.cursor()
        q = " Delete from users "
        if  auth.auth_by_token(id) != id:
            cursor.execute(q + f"where id = {id}")
            conn.commit()
    return {"message": "User delted"}
