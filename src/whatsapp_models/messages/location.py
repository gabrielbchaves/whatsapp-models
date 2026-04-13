"""Location message model.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/location-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.base import MessageBase


class LocationObject(BaseModel):
    """Geographic location payload for a location message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    latitude: Annotated[float, Field(description="Latitude of the location in decimal degrees.")]
    longitude: Annotated[float, Field(description="Longitude of the location in decimal degrees.")]
    name: Annotated[str, Field(description="Name of the location shown to the recipient.")]
    address: Annotated[str, Field(description="Address of the location shown to the recipient.")]


class LocationMessage(MessageBase):
    """Outgoing WhatsApp location message."""

    type: Annotated[
        Literal[MessageType.location],
        Field(description="Message type discriminator."),
    ] = MessageType.location
    location: Annotated[LocationObject, Field(description="Location payload.")]
