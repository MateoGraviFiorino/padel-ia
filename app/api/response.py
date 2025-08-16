from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

class SystemInfoResponse(BaseModel):
    system: str
    python_version: str
    cpu_count: int
    memory_total: str
    memory_available: str
    disk_usage: str

class APIInfoResponse(BaseModel):
    name: str
    version: str
    description: str
    endpoints: dict[str, str]
    models_loaded: bool
    data_directory: str