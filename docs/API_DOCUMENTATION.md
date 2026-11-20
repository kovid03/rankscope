# RankScope — REST API Documentation

Base URL: `http://localhost:8000/api/v1`

---

## 1. Authentication (`/auth`)

### `POST /auth/register`
Create a new user account.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false,
    "created_at": "2026-11-20T11:50:00Z"
  }
  ```

### `POST /auth/login`
Authenticate and receive a JWT Bearer token.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```

### `GET /auth/me`
Retrieve profile of currently authenticated user.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):** User object.

---

## 2. Projects (`/projects`)

### `GET /projects`
List all projects belonging to the user.

### `POST /projects`
Create a new project workspace.
- **Request Body:**
  ```json
  {
    "name": "E-Commerce SEO Campaign",
    "description": "Tracking search rankings and competitor gaps"
  }
  ```

### `GET /projects/{project_id}`
Retrieve a specific project.

### `PUT /projects/{project_id}`
Update project details.

### `DELETE /projects/{project_id}`
Delete a project and all associated tracked domains (Cascade).

---

## 3. Domains (`/domains`)

### `POST /domains`
Add a target or competitor domain to track.
- **Request Body:**
  ```json
  {
    "domain": "https://example.com/",
    "project_id": 1,
    "display_name": "Example Corp",
    "is_primary": true
  }
  ```
- **Response (201 Created):** Normalized domain entry.

### `GET /domains?project_id={id}`
List all tracked domains under a project.

### `DELETE /domains/{domain_id}`
Remove a tracked domain.
