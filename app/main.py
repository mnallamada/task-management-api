from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse
from app.routers import auth, tasks
from app.utils.db import init_db

# Initialize the FastAPI application
app = FastAPI(
    title="Task Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize the database
init_db()

# Middleware to rewrite the `location` header for HTTPS
@app.middleware("http")
async def enforce_https_redirect(request: Request, call_next):
    response = await call_next(request)

    # Ensure the `location` header reflects HTTPS
    if (
        "X-Forwarded-Proto" in request.headers
        and request.headers["X-Forwarded-Proto"] == "https"
    ):
        location = response.headers.get("location", "")
        if location.startswith("http://"):
            response.headers["location"] = location.replace("http://", "https://")
    return response

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://taskmanager.mounikanallamada.com", "https://taskmanager-api.mounikanallamada.com"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "taskmanager.mounikanallamada.com",  # Your custom domain
        "taskmanager-api.mounikanallamada.com",  # API domain
        "*.mounikanallamada.com",  # Wildcard for all subdomains
    ],
)

# Define a custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the default OpenAPI schema
    openapi_schema = get_openapi(
        title="Task Management System API",
        version="1.0.0",
        description="Task Management System with JWT Authentication for managing users and tasks.",
        routes=app.routes,
    )

    # Add security schemes for BearerAuth
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply the security scheme to all routes
    for path in openapi_schema.get("paths", {}).values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom OpenAPI function to the app
app.openapi = custom_openapi

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Task Management System API"}

# Debug endpoint for troubleshooting headers
@app.api_route("/debug", methods=["GET", "HEAD"])
def debug_headers(request: Request):
    return {
        "X-Forwarded-Proto": request.headers.get("x-forwarded-proto"),
        "Host": request.headers.get("host"),
        "Headers": dict(request.headers),
    }
