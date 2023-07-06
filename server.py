from fastapi import FastAPI, HTTPException, status
from class_metiers  import class_user

from class_DAO import class_user_DAO, class_video_DAO
from pydantic import BaseModel
import uvicorn
from fastapi.responses import JSONResponse


class User(BaseModel):
	login: str
	age: int
	genre : str

class Video(BaseModel):
	title: str
	path: str


app = FastAPI()

@app.put("/user/")
def create_user(user :  User, status_code=201):
	userDAO=class_user_DAO.User_DAO()
	user_exist=userDAO.find_user_from_name(user.login)
	if user_exist==None :
		userDAO.add_user(user.login, user.age, user.genre)
		return JSONResponse(status_code=status.HTTP_201_CREATED, content={"login": user.login, "age": user.age, "genre":user.genre})
	else :
		raise HTTPException(status_code=405, detail="Error 405 : Login already exist")


@app.put("/video/")
def create_video(video :  Video, status_code=201):
	videoDAO=class_video_DAO.Video_DAO()
	video_exist=videoDAO.find_video_from_title(video.title)
	path_exist=videoDAO.find_video_from_path(video.path)
	if path_exist!=None :
		return JSONResponse(status_code=status.HTTP_201_CREATED, content={"title": video.title, "path": video.path})
	if video_exist==None :
		videoDAO.add_Video(video.title, video.path)
		return JSONResponse(status_code=status.HTTP_201_CREATED, content={"title": video.title, "path": video.path})
	else :
		raise HTTPException(status_code=405, detail="Error 405 : Title already exist")


@app.get("/user/{login}")
def get_user(login :str):
	userDAO=class_user_DAO.User_DAO()
	user=userDAO.find_user_from_name(login)
	if user!=None:
		return {"id_user":user.id_user,"login": user.login, "age": user.age, "genre":user.genre}
	else :
		raise HTTPException(status_code=404, detail="Error 404 : Login not found")

@app.get("/video/")
def find_all_videos(number, page):
	videoDAO=class_video_DAO.Video_DAO()
	videos=videoDAO.find_all(int(number), int(page))
	data_request=[]
	for v in videos :
		data_request.append({"id_video":v.id_video, "Title":v.title, "Path":v.path})
	return data_request

@app.get("/video/{id_video}")
def find_video_from_id(id_video):
	videoDAO=class_video_DAO.Video_DAO()
	video=videoDAO.find_video_from_id(id_video)
	return {"id_video":video.id_video, "Title":video.title, "Path":video.path}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
