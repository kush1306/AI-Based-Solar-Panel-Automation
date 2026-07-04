from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, Response

from app.api.health import router as health_router
from app.api import router as api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import RequestLoggingMiddleware, setup_logging

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#0f172a"/>
  <circle cx="16" cy="16" r="7" fill="#f59e0b"/>
  <g stroke="#f59e0b" stroke-width="2" stroke-linecap="round">
    <line x1="16" y1="2" x2="16" y2="7"/>
    <line x1="16" y1="25" x2="16" y2="30"/>
    <line x1="2" y1="16" x2="7" y2="16"/>
    <line x1="25" y1="16" x2="30" y2="16"/>
  </g>
</svg>"""

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Production REST API for the Solar Intelligence Platform. "
        "Provides CRUD access to weather, solar, battery, telemetry, "
        "alerts, and system logs. AI inference is intentionally deferred."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=FAVICON_SVG, media_type="image/svg+xml")


app.include_router(health_router)
app.include_router(api_router, prefix="/api")
