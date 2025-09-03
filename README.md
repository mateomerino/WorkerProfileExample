## Interacciones clave: WorkerProfile
# Contexto

La plataforma conecta empleadores con trabajadores (niñera, ama de casa, cocinero/a, etc.).
Cada trabajador tiene un WorkerProfile con su presentación, disponibilidad horaria, educación y experiencias laborales.
Flujo típico: el usuario (worker) añade una experiencia y el backend la crea y, si corresponde, actualiza datos del perfil (p. ej., ubicación).

flowchart TD
    A[Frontend: Worker autenticado] --> B[POST /worker/:profile_id/experience/add/]
    B --> C[API: WorkerProfileExperienceView.post]
    C --> D[Serializer: valida title/description/currently_working]
    D --> E{Valido?}
    E -- No --> F[400 con errores de validación]
    E -- Sí --> G[DB: crea WorkerProfileExperience (FK a profile_id)]
    G --> H[201 con JSON de la experiencia creada]
    H --> I[Frontend actualiza UI: lista de experiencias]

    I --> J[Opcional: PUT /worker/:profile_id/info/update/]
    J --> K[API: WorkerProfileInfoView.put]
    K --> L{Trae datos de ubicación?}
    L -- Sí --> M[DB: crea/actualiza Location (OneToOne)]
    L -- No --> N[Sin cambios en Location]
    M --> O[DB: actualiza WorkerProfile con nuevos datos]
    N --> O[DB: actualiza WorkerProfile con otros campos]
    O --> P[200 con JSON del perfil actualizado]
    P --> Q[Frontend refresca sección de perfil]
