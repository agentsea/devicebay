from pydantic import BaseModel


class DeviceModel(BaseModel):
    name: str
    config: BaseModel
