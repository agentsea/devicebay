from typing import List, Optional, Dict
import uuid
import time
import json

from sqlalchemy import or_

from .db.models import DeviceTypeRecord
from .db.conn import WithDB
from .models import (
    V1EnvVarOpt,
    V1LLMProviders,
    V1DeviceTypeFile,
    V1LLMProviders,
)


class DeviceType(WithDB):
    """A type of device"""

    def __init__(
        self,
        name: str,
        description: str,
        image: str,
        versions: Dict[str, str],
        supported_runtimes: List[str],
        owner_id: Optional[str] = None,
        env_opts: List[V1EnvVarOpt] = [],
        public: bool = False,
        icon: Optional[str] = None,
        mem_request: Optional[str] = "500m",
        mem_limit: Optional[str] = "2gi",
        cpu_request: Optional[str] = "1",
        cpu_limit: Optional[str] = "4",
        gpu_mem: Optional[str] = None,
        llm_providers: Optional[V1LLMProviders] = None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.image = image
        self.versions = versions
        self.supported_runtimes = supported_runtimes
        self.owner_id = owner_id
        self.env_opts = env_opts
        self.public = public
        self.icon = icon
        self.mem_request = mem_request
        self.mem_limit = mem_limit
        self.cpu_request = cpu_request
        self.cpu_limit = cpu_limit
        self.gpu_mem = gpu_mem
        self.created = time.time()
        self.updated = time.time()
        self.llm_providers: Optional[V1LLMProviders] = llm_providers
        self.save()

    def to_schema(self) -> V1DeviceTypeFile:
        return V1DeviceTypeFile(
            id=self.id,
            name=self.name,
            description=self.description,
            image=self.image,
            versions=self.versions,
            env_opts=self.env_opts,
            supported_runtimes=self.supported_runtimes,
            created=self.created,
            updated=self.updated,
            public=self.public,
            icon=self.icon,
            mem_request=self.mem_request,
            mem_limit=self.mem_limit,
            cpu_request=self.cpu_request,
            cpu_limit=self.cpu_limit,
            gpu_mem=self.gpu_mem,
            llm_providers=self.llm_providers,
            owner_id=self.owner_id,
        )

    @classmethod
    def from_schema(cls, schema: V1DeviceTypeFile) -> "DeviceType":
        obj = cls.__new__(cls)
        obj.id = schema.id
        obj.name = schema.name
        obj.owner_id = schema.owner_id
        obj.description = schema.description
        obj.image = schema.image
        obj.env_opts = schema.env_opts
        obj.supported_runtimes = schema.supported_runtimes
        obj.created = schema.created
        obj.updated = schema.updated
        obj.public = schema.public
        obj.icon = schema.icon
        obj.mem_limit = schema.mem_limit
        obj.mem_request = schema.mem_request
        obj.cpu_limit = schema.cpu_limit
        obj.cpu_request = schema.cpu_request
        obj.gpu_mem = schema.gpu_mem
        obj.versions = schema.versions
        obj.llm_providers = schema.llm_providers
        return obj

    def to_record(self) -> DeviceTypeRecord:
        versions = json.dumps(self.versions)
        llm_providers = None
        if self.llm_providers:
            llm_providers = json.dumps(self.llm_providers.model_dump())

        return DeviceTypeRecord(
            id=self.id,
            name=self.name,
            description=self.description,
            image=self.image,
            versions=versions,
            env_opts=json.dumps([opt.model_dump() for opt in self.env_opts]),
            supported_runtimes=json.dumps(self.supported_runtimes),
            created=self.created,
            updated=self.updated,
            owner_id=self.owner_id,
            public=self.public,
            icon=self.icon,
            mem_limit=self.mem_limit,
            mem_request=self.mem_request,
            cpu_limit=self.cpu_limit,
            cpu_request=self.cpu_request,
            gpu_mem=self.gpu_mem,
            llm_providers=llm_providers,
        )

    @classmethod
    def from_record(cls, record: DeviceTypeRecord) -> "DeviceType":
        versions = {}
        if len(str(record.versions)) != 0:
            versions = json.loads(str(record.versions))

        llm_providers = None
        if len(str(record.llm_providers)) != 0:
            llm_providers = V1LLMProviders(**json.loads(str(record.llm_providers)))

        obj = cls.__new__(cls)
        obj.id = record.id
        obj.name = record.name
        obj.description = record.description
        obj.image = record.image
        obj.versions = versions
        obj.env_opts = [V1EnvVarOpt(**opt) for opt in json.loads(str(record.env_opts))]
        obj.supported_runtimes = json.loads(str(record.supported_runtimes))
        obj.created = record.created
        obj.updated = record.updated
        obj.owner_id = record.owner_id
        obj.public = record.public
        obj.icon = record.icon
        obj.mem_limit = record.mem_limit
        obj.mem_request = record.mem_request
        obj.cpu_limit = record.cpu_limit
        obj.cpu_request = record.cpu_request
        obj.gpu_mem = record.gpu_mem
        obj.llm_providers = llm_providers
        return obj

    def save(self) -> None:
        for session in self.get_db():
            if session:
                record = self.to_record()
                session.merge(record)
                session.commit()

    @classmethod
    def find(cls, **kwargs) -> List["DeviceType"]:
        for session in cls.get_db():
            records = session.query(DeviceTypeRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

        return []

    @classmethod
    def find_for_user(
        cls, user_id: str, name: Optional[str] = None
    ) -> List["DeviceType"]:
        for session in cls.get_db():
            # Base query
            query = session.query(DeviceTypeRecord).filter(
                or_(
                    DeviceTypeRecord.owner_id == user_id,
                    DeviceTypeRecord.public == True,
                )
            )

            # Conditionally add name filter if name is provided
            if name is not None:
                query = query.filter(DeviceTypeRecord.name == name)

            records = query.all()
            return [cls.from_record(record) for record in records]
        return []

    @classmethod
    def delete(cls, id: str, owner_id: str) -> None:
        for session in cls.get_db():
            if session:
                record = (
                    session.query(DeviceTypeRecord)
                    .filter_by(id=id, owner_id=owner_id)
                    .first()
                )
                if record:
                    session.delete(record)
                    session.commit()

    def update(self, model: V1DeviceTypeFile) -> None:
        """
        Updates the current DeviceType instance with values from an DeviceTypeModel instance.
        """
        # Track if any updates are needed
        updated = False

        # Compare and update fields
        if self.name != model.name:
            self.name = model.name
            updated = True

        if self.description != model.description:
            self.description = model.description
            updated = True

        if self.image != model.image:
            self.image = model.image
            updated = True

        if self.versions != model.versions:
            self.versions = model.versions
            updated = True

        if self.env_opts != model.env_opts:
            self.env_opts = model.env_opts
            updated = True

        if self.supported_runtimes != model.supported_runtimes:
            self.supported_runtimes = model.supported_runtimes
            updated = True

        if self.public != model.public:
            self.public = model.public
            updated = True

        if self.icon != model.icon:
            self.icon = model.icon
            updated = True

        if self.mem_request != model.mem_request:
            self.mem_request = model.mem_request
            updated = True

        if self.mem_limit != model.mem_limit:
            self.mem_limit = model.mem_limit
            updated = True

        if self.cpu_request != model.cpu_request:
            self.cpu_request = model.cpu_request
            updated = True

        if self.cpu_limit != model.cpu_limit:
            self.cpu_limit = model.cpu_limit
            updated = True

        if self.gpu_mem != model.gpu_mem:
            self.gpu_mem = model.gpu_mem
            updated = True

        if self.llm_providers != model.llm_providers:
            self.llm_providers = model.llm_providers
            updated = True

        # If anything was updated, set the updated timestamp and save changes
        if updated:
            self.updated = time.time()
            self.save()
