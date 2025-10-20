
import logging
from fastapi import FastAPI, HTTPException, Depends
from schemas import Pet, Person, AdoptionRequest, RequestStatus
from database import SessionLocal, engine
from models import Base
import crud

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

Base.metadata.create_all(bind=engine)
logger.debug("Database tables created")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/pets")
def get_pets(db = Depends(get_db)):
    logger.debug("GET /pets solicitado")
    return crud.get_pets(db)

@app.get("/persons")
def get_persons(db = Depends(get_db)):
    logger.debug("GET /persons solicitado")
    return crud.get_persons(db)

@app.post("/pets")
def add_pet(pet: Pet, db = Depends(get_db)):
    if any(p.id == pet.id for p in crud.get_pets(db)):
        logger.warning("Intento de añadir mascota con ID duplicado: %d", pet.id)
        raise HTTPException(status_code=400, detail="ID mascota ya existe")
    return crud.add_pet(db, pet)

@app.post("/persons")
def add_person(person: Person, db = Depends(get_db)):
    if any(p.id == person.id for p in crud.get_persons(db)):
        logger.warning("Intento de añadir persona con ID duplicado: %d", person.id)
        raise HTTPException(status_code=400, detail="ID persona ya existe")
    return crud.add_person(db, person)

@app.post("/adoptions")
def adopt_pet(request: AdoptionRequest, db = Depends(get_db)):
    persons = crud.get_persons(db)
    pets = crud.get_pets(db)
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

    logger.info(f"Adopción aprobada: {person.name} ha adoptado a {pet.name}")
    return {
        "message": f"{person.name} ha adoptado a {pet.name}",
        "adoption_request": request
    }