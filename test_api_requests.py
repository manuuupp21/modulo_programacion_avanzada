import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Creamos las personas
person_data1 = {
    "id": 1,
    "name": "Manuel",
    "email": "manuel@example.com",
    'phone': '663-555-123'
}

person_data2 = {
    "id": 2,
    "name": "Gabriela",
    "email": "gabriela@example.com",
    "phone": "622-345-456"
}

try:
    response = requests.post(f"{BASE_URL}/persons", json=person_data1)
    print("Crear persona:", response.status_code, response.json())
    assert response.status_code in [200, 201]
    person_id1 = response.json().get("id")
except Exception as e:
    print("Error al crear persona:", e)

try:
    response = requests.post(f"{BASE_URL}/persons", json=person_data2)
    print("Crear persona:", response.status_code, response.json())
    assert response.status_code in [200, 201]
    person_id2 = response.json().get("id")
except Exception as e:
    print("Error al crear persona:", e)

# 2. Creamos las mascotas
pet_data1 = {
    "id": 1,
    "name": "Bobby",
    "age": 4,
    "type": "dog"
}

pet_data2 = {
    "id": 2,
    "name": "Mittens",
    "age": 2,
    "type": "cat"
}

try:
    response = requests.post(f"{BASE_URL}/pets", json=pet_data1)
    print("Crear mascota:", response.status_code, response.json())
    assert response.status_code in [200, 201]
    pet_id1 = response.json().get("id")
except Exception as e:
    print("Error al crear mascota:", e)
    raise

try:
    response = requests.post(f"{BASE_URL}/pets", json=pet_data2)
    print("Crear mascota:", response.status_code, response.json())
    assert response.status_code in [200, 201]
    pet_id2 = response.json().get("id")
except Exception as e:
    print("Error al crear mascota:", e)
    raise

# 3. Las personas quieren adoptar mascotas.

adoption_request_data1 = {
    "id": 1,
    "person_id": person_data2["id"],
    "pet_id": pet_data1["id"]
}

adoption_request_data2 = {
    "id": 2,
    "person_id": person_data1["id"],
    "pet_id": pet_data2["id"]
}

try:
    response = requests.post(f"{BASE_URL}/adoptions", json=adoption_request_data1)
    print("Crear solicitud de adopción:", response.status_code, response.json())
    assert response.status_code in [200, 201]
    pet_id1 = adoption_request_data1["pet_id"]
except Exception as e:
    print("Error al crear solicitud de adopción:", e)

try:
    response = requests.post(f"{BASE_URL}/adoptions", json=adoption_request_data2)
    print("Crear solicitud de adopción:", response.status_code, response.json())
    assert response.status_code in [200, 201]
    pet_id2 = adoption_request_data2["pet_id"]
except Exception as e:
    print("Error al crear solicitud de adopción:", e)

# 4. Petición GET para verificar la adopción correcta de la mascota.

try:
    response = requests.get(f"{BASE_URL}/pets")
    print("Obtener mascotas:", response.status_code, response.json())
    assert response.status_code == 200
    pets = response.json()
except Exception as e:
    print("Error al obtener mascotas:", e)

adopted_pet1 = next((p for p in pets if p["id"] == pet_id1), None)
assert adopted_pet1['adopted'] is True

adopted_pet2 = next((p for p in pets if p["id"] == pet_id2), None)
assert adopted_pet2['adopted'] is True

# 5. Petición DELETE para eliminar la adopción de la mascota (útil para pruebas).

try:
    response = requests.delete(f"{BASE_URL}/adoptions/{pet_id1}")
    print("Eliminar adopción:", response.status_code, response.json())
    assert response.status_code == 200
except Exception as e:
    print("Error al eliminar adopción:", e)