"""Base models and enums shared across all outgoing message types.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages
"""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class MessagingProduct(StrEnum):
    """Messaging product identifier, always 'whatsapp' for this API."""

    whatsapp = "whatsapp"


class RecipientType(StrEnum):
    """Recipient type for outgoing messages."""

    individual = "individual"
    group = "group"


class MessageContext(BaseModel):
    """Context object for replying to a specific message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    message_id: Annotated[str, Field(description="ID of the message being replied to.")]


class MessageBase(BaseModel):
    """Base fields present in every outgoing WhatsApp message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    messaging_product: Annotated[
        Literal[MessagingProduct.whatsapp],
        Field(description="Messaging product. Always 'whatsapp'."),
    ] = MessagingProduct.whatsapp
    recipient_type: Annotated[
        RecipientType,
        Field(description="Recipient type: 'individual' or 'group'."),
    ] = RecipientType.individual
    to: Annotated[str, Field(description="WhatsApp phone number or group ID of the recipient.")]
    context: Annotated[
        MessageContext | None,
        Field(description="Context for replying to a specific message."),
    ] = None
