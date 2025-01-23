
# Task Management API

This is the **Task Management API**, built with **FastAPI** and powered by Python. The API provides a backend for managing tasks, user authentication, and user data.

## Features

- **User Authentication**: Secure authentication using JWT (JSON Web Tokens).
- **Task Management**: Create, update, delete, and retrieve tasks.
- **CORS Support**: Configured for frontend integration.
- **Database Integration**: Uses a relational database for persistent storage.
- **HTTPS Support**: Fully configured to run with HTTPS behind an AWS ALB.
- **Containerized Deployment**: Dockerized for easy deployment.

---

## Prerequisites

Ensure the following are installed on your system:
- Python 3.10 or higher
- Docker (if using containerized deployment)
- AWS account (if deploying on AWS with ALB)
- PostgreSQL database or any relational DB configured

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/mnallamada/task-management-api.git
cd task-management-api
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://username:password@host:port/dbname
JWT_SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --proxy-headers
```

The API will be accessible at: `http://localhost:8080`

---

## Endpoints

### Authentication
- `POST /auth/login`: Authenticate a user and retrieve a JWT token.
- `POST /auth/register`: Register a new user.

### Tasks
- `GET /tasks`: Retrieve all tasks (supports search query).
- `POST /tasks`: Create a new task.
- `PUT /tasks/{task_id}`: Update a task.
- `DELETE /tasks/{task_id}`: Delete a task.

### Users
- `GET /users/{user_id}`: Retrieve user details.
- `GET /users`: Retrieve all users.

---

## Docker Deployment

### Build and Run the Container
1. Build the Docker image:
    ```bash
    docker build -t task-management-api .
    ```

2. Run the container:
    ```bash
    docker-compose up -d
    ```

The API will be available at `http://localhost`.

---

## Deployment on AWS

1. **Set up ALB and Target Group**:
   - Create an ALB in AWS and configure a target group pointing to your EC2 instance.

2. **Update Security Groups**:
   - Ensure your EC2 instance allows traffic from the ALB on port `8080`.

3. **Domain and HTTPS**:
   - Add a CNAME in your DNS to map your domain to the ALB.
   - Use AWS ACM to issue a certificate for HTTPS.

4. **Configure `.env` with Production Settings**:
   - Use environment variables for sensitive data and avoid hardcoding secrets.

---

## Testing

### Using Postman or cURL
- Import the API into Postman or test endpoints using `curl`:
  ```bash
  curl -X POST https://your-domain.com/auth/login \
       -H "Content-Type: application/json" \
       -d '{"username": "testuser", "password": "password"}'
  ```

### Unit Tests
Run unit tests:
```bash
pytest
```

---

## Project Structure

```
task-management-api/
├── app/
│   ├── models/        # Database models
│   ├── routers/       # API routes
│   ├── schemas/       # Pydantic models
│   ├── services/      # Business logic
│   ├── utils/         # Utility functions
├── main.py            # Main FastAPI application
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore file
├── .env               # Environment variables (not tracked in Git)
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── README.md          # Project documentation
```

---

## Contributing

Contributions are welcome! Please fork this repository, create a feature branch, and submit a pull request.

---