from fastapi import FastAPI, HTTPException, status
from class_metiers  import class_user

from class_DAO import class_user_DAO, class_video_DAO, class_emotion_DAO, class_transcript_DAO
from pydantic import BaseModel
import uvicorn
from fastapi.responses import JSONResponse, FileResponse




class Videos_recommendation_user(BaseModel):
    id_video_ref : int
    id_video_reco : int
    id_user : int
    rank : int
    note : int

class User(BaseModel):
	login: str
	age: int
	genre : str
	physio_bool:bool

class Transcript(BaseModel):
	title:str
	num_dialogue :str
	text : str
	begin_utterance : int
	end_utterance :int
	emotions : list
	labels:list

class Video(BaseModel):
	title: str
	path: str

class Emotion(BaseModel):
	name: str

app = FastAPI()



@app.put("/user/")
def create_user(user :  User, status_code=201):
	userDAO=class_user_DAO.User_DAO()
	user_exist=userDAO.find_user_from_name(user.login)
	if user_exist==None :
		userDAO.add_user(user.login, user.age, user.genre, user.physio_bool)
		return JSONResponse(status_code=status.HTTP_201_CREATED, content={"login": user.login, "age": user.age, "genre":user.genre, "physio":user.physio_bool})
	else :
		raise HTTPException(status_code=405, detail="Error 405 : Login already exist")


@app.put("/video/")
def create_video(video :  Video, status_code=201):
	videoDAO=class_video_DAO.Video_DAO()
	video_exist=videoDAO.find_video_from_title(video.title)
	path_exist=videoDAO.find_video_from_path(video.path)
	if video_exist==None :
		videoDAO.add_Video(video.title, video.path)
		return JSONResponse(status_code=status.HTTP_201_CREATED, content={"title": video.title, "path": video.path})
	else :
		raise HTTPException(status_code=405, detail="Error 405 : Title already exist")


@app.put("/emotion")
def create_emotion(emotion :Emotion, status_code=201):
	emotionDAO=class_emotion_DAO.Emotion_DAO()
	emotionDAO.add_Emotion(emotion.name)
	return JSONResponse(status_code=status.HTTP_201_CREATED, content={"name": emotion.name})

@app.put("/transcript")
def create_transcript(transcript:Transcript, status_code=201):
	transcript_DAO=class_transcript_DAO.Transcript_DAO()
	video_DAO=class_video_DAO.Video_DAO()
	video=video_DAO.find_video_from_title(transcript.title)
	transcript_DAO.add_Transcript_from_video(video.id_video, transcript.num_dialogue, transcript.text, transcript.begin_utterance, transcript.end_utterance)
	transcript_DAO.add_emotions_to_transcript(video.id_video, transcript.num_dialogue, transcript.emotions, transcript.labels)
	return JSONResponse(status_code=status.HTTP_201_CREATED, content={"title":transcript.title, "num_dialogue":transcript.num_dialogue, "text":transcript.text,"begin_utterance":transcript.begin_utterance, "end_utterance":transcript.end_utterance})

@app.put("/emotion_rank/")
def init_reco_video(videos_recommendation_user : Videos_recommendation_user):
	userDAO=class_user_DAO.User_DAO()
	userDAO.init_reco_video(videos_recommendation_user.id_video_ref, videos_recommendation_user.id_video_reco, videos_recommendation_user.id_user, videos_recommendation_user.rank)
	return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id_video_ref":videos_recommendation_user.id_video_ref, "id_video_reco": videos_recommendation_user.id_video_reco,"id_user":videos_recommendation_user.id_user, "rank":videos_recommendation_user.rank, "note":videos_recommendation_user.note})


@app.get("/user/{login}")
def get_user(login :str):
	userDAO=class_user_DAO.User_DAO()
	user=userDAO.find_user_from_name(login)
	if user!=None:
		return {"id_user":user.id_user,"login": user.login, "age": user.age, "genre":user.genre, "physio":user.physio_bool}
	else :
		raise HTTPException(status_code=404, detail="Error 404 : Login not found")

@app.get("/videos/")
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



@app.get("/video/")
def find_video_from_title(name):
	videoDAO=class_video_DAO.Video_DAO()
	video=videoDAO.find_video_from_title(name)
	return {"id_video":video.id_video, "Title":video.title, "Path":video.path}




@app.get("/transcript")
def get_transcripts(id_video, number, page):
	video_DAO=class_video_DAO.Video_DAO()
	transcripts=video_DAO.find_transcripts(int(id_video),int(number), int(page))
	request=[]
	for transcript in transcripts :
		request.append({"id_transcript":transcript.id_transcript ,"id_video":transcript.id_video, "num_dialogue":transcript.num_dialogue, "text":transcript.text,"begin_utterance":transcript.begin_utterance, "end_utterance":transcript.end_utterance})
	return JSONResponse(status_code=200, content=request)

@app.get("/emotions/")
def get_emotions_from_transcript(id_transcript):
	transcriptDAO=class_transcript_DAO.Transcript_DAO()
	emotions=transcriptDAO.get_emotions_from_transcript(int(id_transcript))
	request=[]
	for emotion in emotions :
		request.append({"id_emotion":emotion.id_emotion, "name":emotion.name})
	return JSONResponse(status_code=200, content=request)		

@app.get("/labels/")
def get_labels_from_transcript(id_transcript):
	transcriptDAO=class_transcript_DAO.Transcript_DAO()
	emotions=transcriptDAO.get_labels_from_transcript(int(id_transcript))
	request=[]
	for emotion in emotions :
		request.append({"id_emotion":emotion.id_emotion, "name":emotion.name})
	return JSONResponse(status_code=200, content=request)		


@app.get("/emotion_rank/")
def find_video_reco_first_ranks(id_video_ref, id_user, seuil):
	userDAO=class_user_DAO.User_DAO()
	videos=userDAO.find_video_reco_first_ranks(id_video_ref, id_user, seuil)
	request=[]
	for video in videos :
		request.append({"id_video":video.id_video, "Title":video.title, "Path":video.path})
	return JSONResponse(status_code=200, content=request)

@app.get("/emotion_rank_one/")
def find_video_reco_first_ranks(id_video_ref, id_user, rank):
	userDAO=class_user_DAO.User_DAO()
	videos=userDAO.find_video_reco_from_rank(id_video_ref, id_user, rank)
	request=[]
	for video in videos :
		request.append({"id_video":video.id_video, "Title":video.title, "Path":video.path})
	return JSONResponse(status_code=200, content=request)

@app.get("/note_video_user/")
def find_noted_videos(id_user, page, number):
	userDAO=class_user_DAO.User_DAO()
	notes=userDAO.find_noted_videos(int(id_user), int(page), int(number))
	request=[]
	for note in notes :
		request.append({"id_video_ref":note[0].id_video, "title_ref":note[0].Title, "path_ref":note[0].Path,"id_video_reco":note[1].id_video, "title_reco":note[1].Title, "path_reco":note[1].Path, "rank":note[2], "note":note[3]})
	return JSONResponse(status_code=200, content=request)

@app.get("/note_video_ref/")
def find_noted_videos2(id_video_ref, page, number):
	videoDAO=class_video_DAO.Video_DAO()
	notes=videoDAO.find_noted_videos(int(id_video_ref), int(page), int(number))
	request=[]
	for note in notes :
		request.append({"id_video_ref":note[0].id_video, "title_ref":note[0].Title, "path_ref":note[0].Path,"id_video_reco":note[1].id_video, "title_reco":note[1].Title, "path_reco":note[1].Path, "rank":note[2], "note":note[3]})
	return JSONResponse(status_code=200, content=request)

@app.get("/picture/")
def download_picture(name):
    return FileResponse(path=name,media_type="image/png")

@app.get("/movie/")
def download_movie(name):
    return FileResponse(path=name,media_type="video/mp4")

@app.patch("/emotion_rank/")
def note_video_recommendation(videos_recommendation_user:Videos_recommendation_user):
	userDAO=class_user_DAO.User_DAO()
	userDAO.note_reco_video(videos_recommendation_user.id_video_ref, videos_recommendation_user.id_video_reco, videos_recommendation_user.id_user, videos_recommendation_user.note)
	return 	JSONResponse(status_code=200, content={"id_video_ref":videos_recommendation_user.id_video_ref, "id_video_reco":videos_recommendation_user.id_video_reco, "id_user":videos_recommendation_user.id_user, "note":videos_recommendation_user.note})



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
