"""Text message model.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/text-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.base import MessageBase


class TextObject(BaseModel):
    """Text content of a WhatsApp text message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    body: Annotated[str, Field(description="Message body text. Supports emoji and markdown.")]
    preview_url: Annotated[
        bool,
        Field(description="Whether to render a URL preview when the body contains a URL."),
    ] = False


class TextMessage(MessageBase):
    """Outgoing WhatsApp text message."""

    type: Annotated[
        Literal[MessageType.text],
        Field(description="Message type discriminator."),
    ] = MessageType.text
    text: Annotated[TextObject, Field(description="Text content of the message.")]
