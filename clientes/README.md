# Microservicio de Clientes

Este microservicio maneja la gestión de clientes (hospitales y clínicas, principalmente) siguiendo la arquitectura hexagonal.

## Características

- Lista todos los clientes
- Obtiene un cliente por ID
- Filtra clientes por categoría
- Busca clientes por nombre
- Permite dar de alta nuevos clientes
- Arquitectura hexagonal (Clean Architecture)
- Datos en memoria para simplicidad (puede adaptarse a persistencias reales)

## Estructura del Proyecto

```
src/
├── dominio/
│   ├── entities/
│   │   └── cliente.py              # Entidad Cliente
│   └── repositorios/
│       └── cliente_repository.py   # Interfaz del repositorio
├── aplicacion/
│   ├── dtos/
│   │   └── cliente_dto.py         # DTOs para transferencia de datos
│   ├── mappers/
│   │   └── cliente_mapper.py      # Mappers entre entidades y DTOs
│   ├── servicios/
│   │   └── cliente_service.py     # Lógica de negocio / servicios de dominio
│   └── use_cases/
│       └── cliente_use_case.py    # Casos de uso
└── infraestructura/
    ├── cmd/
    │   └── cliente_cmd.py         # Controladores (Command Handlers)
    ├── config/
    │   └── config.py              # Configuración de la aplicación
    ├── repositorios/
    │   └── cliente_repository.py  # Implementación concreta del repositorio
    └── rutas/
        └── cliente_routes.py      # Definición de rutas/endpoints
```

## Endpoints Disponibles

### GET /clientes
Obtiene todos los clientes registrados.

**Ejemplo de respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": "cli-001",
      "nombre": "Hospital Santa Fe",
      "email": "contacto@santafe.com",
      "telefono": "+57 1 111 2222",
      "direccion": "Calle 123 #45-67",
      "razon_social": "Hospital Santa Fe de Bogotá S.A.",
      "nit": "900123456-7",
      "categoria": "hospital"
    }
  ],
  "total": 1
}
```

### GET /clientes/{id}
Obtiene la información de un cliente específico por su ID.

### GET /clientes/categoria/{categoria}
Filtra los clientes registrados por su categoría.

Categorías ejemplo (pueden adaptarse según negocio):
- hospital
- clinica
- laboratorio
- ips
- eps
- otro

### GET /clientes/buscar?nombre={nombre}
Busca clientes por nombre (búsqueda por coincidencia parcial o total).

### POST /clientes
Crea un nuevo cliente a partir de un JSON con la siguiente estructura mínima:
```json
{
  "nombre": "Hospital La Paz",
  "email": "info@lapaz.com",
  "telefono": "+57 1 555 1234",
  "direccion": "Carrera 19 #34-56",
  "razon_social": "Fundación Hospital La Paz",
  "nit": "900654321-0",
  "categoria": "hospital"
}
```
Respuesta estándar:
```json
{
  "success": true,
  "data": {
    "id": "cli-002",
    "nombre": "Hospital La Paz",
    ...
  }
}
```

## Instalación y Ejecución

### Requisitos
- Python 3.9+
- pipenv

### Instalación
```bash
pipenv install
```

### Ejecución
```bash
pipenv run python src/main.py
```

El servicio estará disponible en `http://localhost:5004`

### Health Check
```bash
curl http://localhost:5004/health
```

## Variables de Entorno

- `ENV`: Entorno de ejecución (default: development)
- `DEBUG`: Modo debug (default: true)
- `HOST`: Host de la aplicación (default: 0.0.0.0)
- `PORT`: Puerto de la aplicación (default: 5004)
- `LOG_LEVEL`: Nivel de logging (default: INFO)

## Docker

### Construir imagen
```bash
docker build -t microservicio-clientes .
```

### Ejecutar contenedor
```bash
docker run -p 5004:5004 microservicio-clientes
```

## Integración con API Gateway

Este microservicio está diseñado para ser consumido a través del API Gateway (por ejemplo, en el puerto 5000). El gateway actúa como proxy y enruta las peticiones a este microservicio utilizando el prefijo `/clientes`.
