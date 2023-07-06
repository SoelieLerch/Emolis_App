from fastapi.testclient import TestClient
from server import app
from class_metiers import class_user

client=TestClient(app)

def create_user(login, age, genre):
    response = client.put(
        "/user/",
        json={"login": login, "age": age, "genre":genre},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
def get_user(login):
    response = client.get(
        "/user/"+login)
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    data=class_user.User(data["id_user"], data["login"], data["age"], data["genre"])
    return data
