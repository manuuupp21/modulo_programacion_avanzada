# Entrega Módulo Programación Avanzada.

Una API que gestiona animales disponibles para adopción y solicitudes de adopción de los clientes.

## 🐶 AdoptAPI — Estructura del Proyecto

### 📁 **Archivos principales**

#### ⚙️ `main.py`
Contiene la aplicación principal de **FastAPI**.  
- Define los **endpoints** para gestionar:
  - 🐾 Mascotas (`/pets`)
  - 👤 Personas (`/persons`)
  - 💌 Solicitudes de adopción (`/adoptions`)
- Implementa la **lógica de adopción**, verificando:
  - IDs duplicados  
  - Existencia de persona y mascota  
  - Estado de adopción (si ya fue adoptada)
- Configura el **sistema de logs** (consola y archivos `debug.log` / `warning.log`).  
- Inicializa la base de datos y crea las tablas al arrancar la API.

---

#### 🧩 `schemas.py`
Define los **esquemas de datos (Pydantic)** usados para validar y estructurar la información que entra o sale de la API.  
Incluye:
- `Pet` → Datos de la mascota (nombre, edad, tipo, estado de adopción)  
- `Person` → Datos de la persona (nombre, email, teléfono)  
- `AdoptionRequest` → Solicitud de adopción (persona, mascota, fecha y estado)  
- `RequestStatus` → Estados posibles de las solicitudes de adopción:  
  - 🕓 `pending`  
  - ✅ `approved`  
  - ❌ `rejected`

---

#### 🗄️ `models.py`
Define los **modelos ORM (SQLAlchemy)** que representan las tablas de la base de datos.  
Incluye las entidades:
- `Pet` → Tabla de mascotas  
- `Person` → Tabla de personas  
- `AdoptionRequest` → Tabla de solicitudes de adopción, con relaciones entre `Person` y `Pet`  
Cada clase define sus columnas, tipos de datos y relaciones entre entidades.

---

### 💾 `database.py`
Configura la **conexión con la base de datos** mediante **SQLAlchemy**.  
- Define la URL de la base de datos SQLite (`AdoptAPI.db`).  
- Crea el **motor de conexión (`engine`)** y la **sesión (`SessionLocal`)** que se usa en toda la aplicación para interactuar con la base de datos.  
- Esta configuración permite manejar las operaciones de lectura y escritura de forma segura y centralizada.

---

### 🧠 `crud.py`
Contiene las **funciones CRUD (Create, Read, Update, Delete)** que manejan la lógica de acceso a la base de datos.  
Incluye:
- `get_pets()` / `get_persons()` → Obtiene todas las mascotas o personas.  
- `add_pet()` / `add_person()` → Añade nuevos registros a la base de datos.  
- `add_adoption_request()` → Registra una nueva solicitud de adopción.  
- `get_all_adoption_requests()` → Devuelve todas las solicitudes registradas.  
- `delete_adoption_request()` → Revoca una adopción (elimina la solicitud asociada).  

---

### 🧪 `test_api_requests.py`
Script de **pruebas automáticas** que verifica el correcto funcionamiento de la API usando el módulo `requests`.  
Ejecuta una serie de peticiones a los endpoints:
1. 🧍‍♂️ Crea personas (`/persons`)  
2. 🐕 Crea mascotas (`/pets`)  
3. 💌 Envía solicitudes de adopción (`/adoptions`)  
4. ❌ Prueba la eliminación de una adopción (`DELETE /adoptions/{pet_id}`)  

---

