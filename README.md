# WeCareForYou Healthcare Application

A full-stack healthcare management system with role-based access control for **Admin**, **Doctor**, and **Patient** users.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Angular 18 + Bootstrap 5 |
| Backend | Python Flask REST API |
| Database | Supabase PostgreSQL |
| Authentication | JWT (Bearer Token) |

## Project Structure

```
WeCareForYou/
â”œâ”€â”€ backend/          # Flask REST API
â”œâ”€â”€ frontend/         # Angular application
â”œâ”€â”€ database/         # SQL schema
â””â”€â”€ README.md
```

## Prerequisites

- Python 3.7+
- Node.js 18+
- Supabase PostgreSQL database

## Setup Instructions

### 1. Database Setup

```sql
-- Run database/schema.sql in Supabase SQL editor or psql
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env         # Edit secrets if needed
python app.py
```

The API runs at `http://localhost:5000`

**Default Admin Account** (auto-seeded on first run):
- Email: `admin@wecareforyou.com`
- Password: `Admin@123`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app runs at `http://localhost:4200`

### Docker

Create `backend/.env` from `backend/.env.example`, then run:

```bash
docker compose up --build
```

The Docker frontend runs at `http://localhost:4200` and proxies `/api` to the backend.

On Windows, you can also start the Docker app from the project root with:

```bat
start-docker.bat
```

Or with npm from the project root:

```bash
npm start
```

Use `http://localhost:4200` for the Docker app. Use `frontend:dev` only when you specifically want Angular dev server mode.

The backend requires `DATABASE_URL`; it will not silently fall back to a local SQLite database unless `ALLOW_SQLITE_FALLBACK=true` is explicitly set.

### Ubuntu and Jenkins

For Ubuntu deployment and Jenkins CI/CD instructions, see:

```text
docs/UBUNTU_JENKINS.md
```

Quick Ubuntu start:

```bash
chmod +x scripts/ubuntu-run.sh
./scripts/ubuntu-run.sh
```

The Jenkins pipeline is defined in `Jenkinsfile`. Add these Jenkins Secret text credentials before running the pipeline:

- `wecare-database-url`
- `wecare-secret-key`
- `wecare-jwt-secret-key`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login & get JWT |
| POST | `/api/auth/logout` | Logout |

### Patient
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patient/doctors` | View doctors |
| GET | `/api/patient/doctors?search=&speciality=` | Search doctors |
| GET | `/api/patient/doctors/{id}/availability?date=YYYY-MM-DD` | View doctor availability |
| POST | `/api/patient/appointment` | Book appointment |
| GET | `/api/patient/upcoming` | Upcoming appointments |
| PUT | `/api/patient/reschedule/{id}` | Reschedule |
| GET | `/api/patient/history` | Consultation history |

### Doctor
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/doctor/appointments` | View appointments |
| PUT | `/api/doctor/accept/{id}` | Accept appointment |
| PUT | `/api/doctor/reject/{id}` | Reject appointment |
| POST | `/api/doctor/consultation` | Add consultation |
| POST | `/api/doctor/prescription` | Add prescription |
| GET | `/api/doctor/medicines?search=` | Search medicine names |
| POST | `/api/doctor/test` | Recommend test |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/dashboard` | Dashboard stats |
| POST | `/api/admin/doctor` | Add doctor |
| PUT | `/api/admin/doctor/{id}` | Update doctor |
| DELETE | `/api/admin/doctor/{id}` | Delete doctor |
| POST | `/api/admin/patient` | Add patient |
| PUT | `/api/admin/patient/{id}` | Update patient |
| DELETE | `/api/admin/patient/{id}` | Delete patient |
| GET | `/api/admin/appointments` | All appointments |
| PUT | `/api/admin/reschedule/{id}` | Reschedule |

## Authentication Flow

```
User Login â†’ JWT Generated â†’ Store Token â†’ Route Guard â†’ Role Validation â†’ Dashboard
```

## Roles & Features

- **Patient**: Book appointments, view history, manage profile
- **Doctor**: Accept/reject appointments, conduct consultations, prescribe medicines
- **Admin**: CRUD for doctors, patients, and appointments

## Development Order

1. Git repository âœ“
2. Database schema âœ“
3. Flask backend âœ“
4. JWT authentication âœ“
5. All REST APIs âœ“
6. Angular frontend âœ“
7. Role guards & validation âœ“
8. Logging module âœ“

## Testing with Postman

1. Register or login to get a JWT token
2. Add header: `Authorization: Bearer <token>`
3. Test endpoints by role

## License

Educational project - WeCareForYou Healthcare Application
