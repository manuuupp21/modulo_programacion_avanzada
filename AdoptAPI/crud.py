from sqlalchemy.orm import Session
from sqlalchemy import select
import models, schemas
import logging

logger = logging.getLogger("AdoptAPI")

def get_pets(db: Session):
    logger.debug("Obteniendo todas las mascotas de la base de datos")
    pets = db.execute(select(models.Pet).order_by(
        models.Pet.id.desc())).scalars().all()
    logger.info("Se han obtenido %d mascotas", len(pets))
    return pets

def get_persons(db: Session):
    logger.debug("Obteniendo todas las personas de la base de datos")
    persons = db.execute(select(models.Person).order_by(
        models.Person.id.desc())).scalars().all()
    logger.info("Se han obtenido %d personas", len(persons))
    return persons

def add_pet(db: Session, pet: schemas.Pet):
    logger.debug("Añadiendo nueva mascota con ID %d a la base de datos", pet.id)
    db_pet = models.Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    logger.info("Mascota añadida con éxito: %s", db_pet.name)
    return db_pet

def add_person(db: Session, person: schemas.Person):
    logger.debug("Añadiendo nueva persona con ID %d a la base de datos", person.id)
    db_person = models.Person(**person.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    logger.info("Persona añadida con éxito: %s", db_person.name)
    return db_person

def add_adoption_request(db: Session, request: schemas.AdoptionRequest):
    logger.debug("Añadiendo nueva solicitud de adopción a la base de datos")
    db_request = models.AdoptionRequest(**request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    logger.info("Solicitud de adopción añadida con éxito: ID %d", db_request.id)
    return db_request

def get_all_adoption_requests(db: Session):
    logger.debug("Obteniendo todas las solicitudes de adopción de la base de datos")
    requests = db.execute(select(models.AdoptionRequest).order_by(
        models.AdoptionRequest.id.desc())).scalars().all()
    logger.info("Se han obtenido %d solicitudes de adopción", len(requests))
    return requests

def delete_adoption_request(db: Session, pet_id: int):
    logger.debug("Eliminando solicitud de adopción para la mascota con ID %d", pet_id)
    request = db.execute(select(models.AdoptionRequest).filter(
        models.AdoptionRequest.pet_id == pet_id)).scalar()
    if not request:
        logger.warning("Solicitud de adopción no encontrada: ID %d", pet_id)
        return None
    db.delete(request)
    db.commit()
    logger.info(f"Adopción revocada: La mascota {request.pet.name} ya no está adoptada")
    return request