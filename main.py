from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest
from typing import List
from uuid import uuid4, UUID

app = FastAPI()

db: List[User] = [
    User(
        id= UUID("9b2b596d-79fb-4a31-809b-9a289caf7b40"),
        first_name="Aditya",
        last_name="Raj",
        middle_name="",
        gender=Gender.male,
        roles=[Role.student]
    ),
    User(
        id=UUID("9142d0c0-b088-4eef-b696-4d94f96973d6"),
        first_name="Aadya",
        last_name="Jones",
        middle_name="",
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    ),
]


@app.get("/")
async def root():
    return {"Hello": "Mundo"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code = 404,
        detail = f"user with id: {user_id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
