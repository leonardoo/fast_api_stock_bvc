import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

import ormar

from models.base import BaseMeta


class Stock(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stockmodel"

    id: Optional[UUID] = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid1, nullable=True)
    name: str = ormar.String(max_length=100)
    nemo: str = ormar.String(max_length=100, unique=True)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow, onupdate=datetime.utcnow)


