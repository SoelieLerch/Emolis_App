from fastapi.testclient import TestClient
from server import app
from class_DAO import class_emotion_DAO, class_transcript_DAO, class_video_DAO,class_user_DAO
client=TestClient(app)

def create_user(login, age, genre, physio_bool):
    response=client.put("/user/", json={"login": login, "age": age, "genre":genre, "physio_bool":physio_bool})
    return response
def get_user(login):
    response = client.get(
        "/user/"+login)
    return response

def create_video(title, path):
    response = client.put(
        "/video/",
        json={"title": title, "path":  path},
    )
    print(response.status_code)
    assert response.status_code == 201, response.text
    data = response.json()
    print(data)

def find_all_videos(number, page):
    response = client.get(
        "/videos?number="+str(number)+"&page="+str(page))
    return response

def find_video_id(id):
    response = client.get(
        "/video/"+str(id))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data    

def find_video_title(name):
    response = client.get(
        "/video?name="+name)
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data  



def create_emotion(name):
    response = client.put(
        "/emotion/",
        json={"name": name},
    )
    print(response.status_code)
    assert response.status_code == 201, response.text
    data = response.json()
    print(data)
def create_transcript(title, num_dialogue, text,begin_utterance, end_utterance, emotions):    
    response = client.put(
        "/transcript/",
        json={"title":title, "num_dialogue":num_dialogue, "text":text,"begin_utterance":begin_utterance, "end_utterance":end_utterance, "emotions":emotions},
    )
    print(response.status_code)
    assert response.status_code == 201, response.text
    data = response.json()
    print(data)

def get_transcripts(id_video, number, page):
    response = client.get(
        "/transcript?id_video="+str(id_video)+"&number="+str(number)+"&page="+str(page))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def get_emotions_from_transcript(id_transcript):
    response = client.get(
        "/emotions?id_transcript="+str(id_transcript))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def init_reco_video(id_video_ref, id_video_reco, id_user, rank, note):
    
    response = client.put(
        "/emotion_rank/",
        json={"id_video_ref":id_video_ref, "id_video_reco": id_video_reco,"id_user":id_user, "rank":rank, "note":note},
    )
    print(response.status_code)
    assert response.status_code == 201, response.text
    data = response.json()
    print(data)

def find_video_reco_first_ranks(id_video_ref,id_user, seuil):
    response = client.get("/emotion_rank?id_video_ref="+str(id_video_ref)+"&id_user="+str(id_user)+"&seuil="+str(seuil))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data
def find_video_reco_from_rank(id_video_ref, id_user, rank):
    response = client.get("/emotion_rank_one?id_video_ref="+str(id_video_ref)+"&id_user="+str(id_user)+"&rank="+str(rank))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def note_video_recommendation(id_video_ref,id_video_reco, id_user,rank, note):
    response = client.patch("/emotion_rank/",
        json={"id_video_ref":id_video_ref, "id_video_reco": id_video_reco,"id_user":id_user, "rank":rank,"note":note},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def find_noted_videos(id_user, page, number):
    response = client.get("/note_video_user?id_user="+str(id_user)+"&page="+str(page)+"&number="+str(number))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def find_noted_videos2(id_video_ref, page, number):
    response = client.get("/note_video_ref?id_video_ref="+str(id_video_ref)+"&page="+str(page)+"&number="+str(number))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def download_picture(name):
    response = client.get("/picture?name="+name)
    return response

def download_movie(name):
    response = client.get("/movie?name="+name)
    return response

