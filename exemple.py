import controller_login

response=controller_login.get_emotions(1)
response=response.json()
print(response)
response=controller_login.get_labels(1)
response=response.json()
print(response)