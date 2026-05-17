from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, session_routes, agent_routes, scripts_routes
from .config import settings

app = FastAPI(
    title="Bitcoin Smart Contract Agent",
    description="AI-powered Bitcoin script generation and validation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(session_routes.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(agent_routes.router, prefix="/api/agent", tags=["Agent"])
app.include_router(scripts_routes.router, prefix="/api/scripts", tags=["Scripts"])

@app.get("/")
async def root():
    return {"message": "Bitcoin Smart Contract Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}