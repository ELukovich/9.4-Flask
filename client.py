import requests



response = requests.post(
    'http://localhost:5000/advertisement',
    json={"title_adv": "advertisement_1", "description": "adv_1", "owner": "owner_1"},
)

print(response.text)
print(response.status_code)


response = requests.get(
    'http://localhost:5000/advertisement/2',
)

print(response.text)
print(response.status_code)


response = requests.patch(
    'http://localhost:5000/advertisement/2',
    json={"owner": "owner_2"},
)

print(response.text)
print(response.status_code)


response = requests.delete(
    'http://localhost:5000/advertisement/2',
)

print(response.text)
print(response.status_code)