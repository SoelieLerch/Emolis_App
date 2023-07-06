from fastapi.testclient import TestClient
from server import app
from class_metiers import class_user
from class_DAO import class_video_DAO

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


#create_user("lilou783", 28, "femme")
user=get_user("lilou783")
#create_video("baby2", "path")
#find_all_videos(10,0)
find_video_id(2)