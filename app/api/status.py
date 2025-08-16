from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import platform
import psutil
import os
from pathlib import Path
from datetime import datetime
from .response import HealthResponse, SystemInfoResponse, APIInfoResponse

status_router = APIRouter(prefix="/status", tags=["status"])


@status_router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        message="Padel Match Analysis API is running",
        timestamp=datetime.now().isoformat()
    )


@status_router.get("/system", response_model=SystemInfoResponse)
async def system_info() -> SystemInfoResponse:
    system = f"{platform.system()} {platform.release()}"
    python_version = platform.python_version()
    cpu_count = psutil.cpu_count()

    memory = psutil.virtual_memory()
    memory_total = f"{memory.total / (1024**3):.1f} GB"
    memory_available = f"{memory.available / (1024**3):.1f} GB"

    disk = psutil.disk_usage('/')
    disk_usage = f"{disk.used / (1024**3):.1f} GB / {disk.total / (1024**3):.1f} GB"
    
    return SystemInfoResponse(
        system=system,
        python_version=python_version,
        cpu_count=cpu_count,
        memory_total=memory_total,
        memory_available=memory_available,
        disk_usage=disk_usage
    )


@status_router.get("/api", response_model=APIInfoResponse)
async def api_info() -> APIInfoResponse:
    return APIInfoResponse(
        name="Padel Match Analysis API",
        version="1.0.0",
        description="API para analizar partidos de padel usando detección de jugadores y pelota",
        endpoints={
            "upload_video": "/match/upload-video",
            "health": "/status/health",
            "system": "/status/system",
            "api_info": "/status/api"
        }
    )

