# Interacciones clave: WorkerProfile
## Contexto

La aplicación permite que un usuario trabajador (niñera, ama de casa, cocinero/a, etc.) publique su perfil en la plataforma. Ese perfil (WorkerProfile) incluye su presentación, disponibilidad, educación, formación y experiencias previas.
Un flujo común es cuando el usuario añade una nueva experiencia laboral y, además, actualiza parte de la información general de su perfil.

### Paso 1: añadir experiencia

1) El frontend envía un POST a /worker/<profile_id>/experience/add/ con los datos de la nueva experiencia.
```json
{
  "title": "Niñera part-time",
  "description": "Cuidado de dos niños pequeños, preparación de comidas y actividades educativas.",
  "currently_working": false
}
```
#### 2) El backend valida la solicitud con el serializer WorkerProfileExperienceSerializer, que comprueba que:

    -title tenga ≤ 80 caracteres
    -description tenga ≤ 400 caracteres

#### 3) Si los datos son válidos, crea un registro en la tabla WorkerProfileExperience asociado al perfil.

#### 📤 Response (201 Created)
```http
{
  "id": 15,
  "title": "Niñera part-time",
  "description": "Cuidado de dos niños pequeños, preparación de comidas y actividades educativas.",
  "currently_working": false,
  "worker": 7
}
```
### Paso 2: actualizar información del perfil

#### 1) El frontend envía un PUT a /worker/<profile_id>/info/update/ con los datos actualizados del perfil, por ejemplo la ubicación.

📥 Request
```json
{
  "neighborhood": "Cofico",
  "municipality": 1021,
  "province": 10
}
```
#### 2) El backend procesa esos datos:

    -Si el perfil ya tenía una Location, la actualiza.
    
    -Si no, crea una nueva Location y la asigna al WorkerProfile.

#### 3) Luego actualiza el perfil y devuelve el JSON completo serializado con WorkerProfileSerializer.

#### 📤 Response (200 OK)
```json
{
  "id": 7,
  "introduction": "Niñera con 3 años de experiencia en cuidado infantil.",
  "hour_price": 2500,
  "location": {
    "neighborhood": "Cofico",
    "municipality": {
      "id": 1021,
      "name": "Capital"
    },
    "province": {
      "id": 10,
      "name": "Córdoba"
    }
  },
  "services": [
    { "id": 1, "title": "babysitter", "title_display": "Niñera" }
  ],
  "tasks": [
    { "id": 4, "title": "childcare", "title_display": "Cuidado de bebés y niños/as" }
  ],
  "work_arrangements": [
    { "id": 2, "value": "part_time", "value_display": "Part time" }
  ]
}
```

## Qué asegura el backend en este proceso

Validación previa: no se persisten datos inválidos.

Integridad: cada experiencia queda ligada al WorkerProfile correcto.

Consistencia: si la ubicación cambia, se actualiza la relación Location sin duplicar registros.

Respuestas claras:

201 Created con la nueva experiencia

200 OK con el perfil actualizado

400/404 en caso de errores





