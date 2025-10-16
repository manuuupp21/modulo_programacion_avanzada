
import logging
from fastapi import FastAPI, HTTPException
from models import Pet, Person, AdoptionRequest, RequestStatus

# Configuración de logging
logger = logging.getLogger("AdoptAPI")
logger.setLevel(logging.DEBUG)

# Handler para consola (DEBUG+)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

app = FastAPI(title="AdoptAPI")
logger.info("AdoptAPI initialized")

# Datos en memoria (simulación de base de datos)
pets = []
persons = []

# ======================
# ENDPOINTS DE PRUEBA
# ======================
@app.get("/pets")
def get_pets(pets):
    logger.debug("GET /pets solicitado")
    return pets

@app.get("/persons")
def get_persons(persons):
    logger.debug("GET /persons solicitado")
    return persons

@app.post("/pets")
def add_pet(pet: Pet, pets):
    if any(p.id == pet.id for p in pets):
        logger.warning("Intento de añadir mascota con ID duplicado: %d", pet.id)
        raise HTTPException(status_code=400, detail="Pet ID already exists")
    pets.append(pet)
    logger.info("Nueva mascota añadida: %s", pet.name)
    return {"message": "Pet added successfully", "pet": pet}

@app.post("/persons")
def add_person(person: Person, persons):
    if any(p.id == person.id for p in persons):
        logger.warning("Intento de añadir persona con ID duplicado: %d", person.id)
        raise HTTPException(status_code=400, detail="Person ID already exists")
    persons.append(person)
    logger.info("Nueva persona añadida: %s", person.name)
    return {"message": "Person added successfully", "person": person}

adoptions = []  # lista global de solicitudes

@app.post("/adoptions/")
def adopt_pet(request: AdoptionRequest, persons, pets):
    logger.debug(f"Solicitud de adopción recibida: persona={request.person_id}, mascota={request.pet_id}")

    # 1. Verificar que existan persona y mascota
    person = next((p for p in persons if p.id == request.person_id), None)
    pet = next((p for p in pets if p.id == request.pet_id), None)

    if not person or not pet:
        logger.warning(f"Adopción fallida: persona o mascota inexistente (persona={request.person_id}, mascota={request.pet_id})")
        raise HTTPException(status_code=404, detail="Persona o mascota no encontrada")

    # 2. Comprobar si la mascota ya fue adoptada
    if pet.adopted:
        logger.warning(f"Intento de adoptar mascota ya adoptada: {pet.name}")
        raise HTTPException(status_code=400, detail="Mascota ya adoptada")

    # 3. Crear la solicitud
    pet.adopted = True
    request.status = RequestStatus.APPROVED
    adoptions.append(request)

    logger.info(f"Adopción aprobada: {person.name} ha adoptado a {pet.name}")
    return {
        "message": f"{person.name} ha adoptado a {pet.name}",
        "adoption_request": request
    }