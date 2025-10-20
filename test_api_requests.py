import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Creamos una persona
person_data = {
    "id": 1,
    "name": "Manuel",
    "email": "manuel@example.com",
    'phone': '663-555-123'
}
response = requests.post(f"{BASE_URL}/persons", json=person_data)
print("Crear persona:", response.status_code, response.json())
assert response.status_code in [200, 201]
person_id = response.json().get("id")

# 2. Creamos una mascota
pet_data = {
    "id": 1,
    "name": "Bobby",
    "age": 4,
    "type": "dog"
}
response = requests.post(f"{BASE_URL}/pets", json=pet_data)
print("Crear mascota:", response.status_code, response.json())
assert response.status_code in [200, 201]
pet_id = response.json().get("id")

# 3. Esta persona quiere adoptar una mascota.

adoption_request_data = {
    "id": 1,
    "person_id": person_data["id"],
    "pet_id": pet_data["id"]
}
response = requests.post(f"{BASE_URL}/adoptions", json=adoption_request_data)
print("Crear solicitud de adopción:", response.status_code, response.json())
assert response.status_code in [200, 201]

# 4. Listamos todas las mascotas de la base de datos.
response = requests.get(f"{BASE_URL}/pets")
print("Listar mascotas:", response.status_code, response.json())
assert response.status_code in [200, 201]

# 5. Listamos todas las personas de la base de datos.
response = requests.get(f"{BASE_URL}/persons")
print("Listar personas:", response.status_code, response.json())
assert response.status_code in [200, 201]