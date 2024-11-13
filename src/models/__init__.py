"""Models."""

from pydantic import BaseModel, Field

class ProxyBody(BaseModel):
    lat: float = Field(None, description="Latitude")
    long: float = Field(None, description="Longitude")
    radius: float = Field(None, description="Radius")
