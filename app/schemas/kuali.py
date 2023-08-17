import datetime
from pydantic import BaseModel, Field, Json
from typing import Any


class KualiCatalogTimestampItem(BaseModel):
    date: datetime.datetime
    id: str
    name: str


class KualiCatalogItem(BaseModel):
    id: str
    end_date: str = Field(alias="endDate")
    start_date: str = Field(alias="startDate")
    title: str
    modified: KualiCatalogTimestampItem
    created: KualiCatalogTimestampItem


class KualiCourseItem(BaseModel):
    id: str
    pid: str
    title: str
    description: str
    supplementalNotes: str
    proForma: str
    credits: dict[str, Any]
    crossListedCourses: list[dict[str, Any]]
    start_date: str = Field(alias="dateStart")
    subjectCode: dict[str, Any]
    hoursCatalogText: str
    catalogActivationDate: str
