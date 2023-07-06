from fastapi.testclient import TestClient
from server import app
from class_DAO import class_emotion_DAO, class_transcript_DAO, class_video_DAO

client=TestClient(app)

def create_user(login, age, genre):
    response = client.put(
        "/user/",
        json={"login": login, "age": age, "genre":genre},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    print(data)
def get_user(login):
    response = client.get(
        "/user/"+login)
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

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
        "/video?number="+str(number)+"&page="+str(page))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data

def find_video_id(id):
    response = client.get(
        "/video/"+str(id))
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
        "/video?id_video="+str(id_video)+"&number="+str(number)+"&page="+str(page))
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    return data
create_video("babyboom", "moi")
create_emotion("Joie")
create_transcript("babyboom", 0, "I love you", 0, 1, ["Joie"])
get_transcripts(1, 50, 0)
