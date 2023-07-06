from fastapi import FastAPI, HTTPException
from class_metiers  import class_user

from class_DAO import class_user_DAO
from pydantic import BaseModel
import uvicorn


class User(BaseModel):
	login: str
	age: int
	genre : str



app = FastAPI()

@app.put("/user/")
def create_user(user :  User, status_code=200):
	userDAO=class_user_DAO.User_DAO()
	user_exist=userDAO.find_user_from_name(user.login)
	if user_exist==None :
		userDAO.add_user(user.login, user.age, user.genre)
		return {"login": user.login, "age": user.age, "genre":user.genre}
	else :
		raise HTTPException(status_code=405, detail="Error 405 : Login already exist")

@app.get("/user/{login}")
def get_user(login :str):
	userDAO=class_user_DAO.User_DAO()
	user=userDAO.find_user_from_name(login)
	if user!=None:
		return {"id_user":user.id_user,"login": user.login, "age": user.age, "genre":user.genre}
	else :
		raise HTTPException(status_code=404, detail="Error 404 : Login not found")




if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
