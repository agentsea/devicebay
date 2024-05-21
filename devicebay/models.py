from typing import Optional, Dict, List, TypeVar, Generic
from pydantic import BaseModel

ConnectConfigType = TypeVar("ConnectConfigType")
ProvisionConfigType = TypeVar("ProvisionConfigType")


class V1Lock(BaseModel):
    owner_id: str
    created: float
    expires: float
    locked: bool
    reason: Optional[str] = None


class V1Device(BaseModel, Generic[ConnectConfigType]):
    type: str
    name: Optional[str] = None
    config: Optional[ConnectConfigType] = None


class V1DeviceType(BaseModel, Generic[ProvisionConfigType]):
    name: str
    config: Optional[ProvisionConfigType] = None


class V1EnvVarOpt(BaseModel):
    name: str
    description: Optional[str] = None
    required: bool = False
    default: Optional[str] = None
    secret: bool = False
    options: List[str] = []


class V1LLMProviders(BaseModel):
    preference: List[str] = []


class V1DeviceTypeFile(BaseModel):
    id: Optional[str] = None
    name: str
    owner_id: Optional[str] = None
    description: str
    image: Optional[str] = None
    versions: Optional[Dict[str, str]] = None
    env_opts: List[V1EnvVarOpt] = []
    supported_runtimes: List[str] = []
    created: Optional[float] = None
    updated: Optional[float] = None
    public: bool = False
    icon: Optional[str] = None
    mem_request: Optional[str] = "500m"
    mem_limit: Optional[str] = "2gi"
    cpu_request: Optional[str] = "1"
    cpu_limit: Optional[str] = "4"
    gpu_mem: Optional[str] = None
    llm_providers: Optional[V1LLMProviders] = None


class V1DeviceTypeFiles(BaseModel):
    types: List[V1DeviceTypeFile]
