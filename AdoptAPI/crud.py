from sqlalchemy.orm import Session
from sqlalchemy import select
import models, schemas
import logging

logger = logging.getLogger("AdoptAPI")

def get_pets(db: Session):
    logger.debug("Obteniendo todas las mascotas de la base de datos ordenadas por ID")
    pets = db.execute(select(models.Pet).order_by(
        models.Pet.id.desc())).scalars().all()
    logger.info("Se han obtenido %d mascotas", len(pets))
    return pets

def get_persons(db: Session):
    logger.debug("Obteniendo todas las personas de la base de datos ordenadas por ID")
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