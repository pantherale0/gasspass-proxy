"""GasPass proxy service."""

from flask_openapi3 import Tag, APIBlueprint

from src.limiter import limiter
from src.models import ProxyBody
from src.gaspass_api import get_fuels

tag = Tag(name="GasPass Proxy", description="A proxy service to retrieve data from GasPass")
api = APIBlueprint(
    "gaspass",
    __name__,
    url_prefix="/api/v1/gaspass",
    abp_tags=[tag]
)

@api.post("/")
@limiter.limit("4/minute")
def get_data(body: ProxyBody):
    """Get data."""
    return get_fuels(
        lat=body.lat,
        long=body.long,
        rad=body.radius
    )
