"""Message status update models.

Used to mark an incoming message as read, optionally with a typing indicator.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/mark-messages-as-read
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.messages.base import MessagingProduct


class TypingIndicatorContent(BaseModel):
    """Typing indicator payload. Only 'text' is currently supported."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["text"], Field(description="Typing indicator type. Always 'text'.")] = "text"


class MessageStatusUpdate(BaseModel):
    """Mark an incoming message as read, optionally showing a typing indicator to the sender."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    messaging_product: Annotated[
        Literal[MessagingProduct.whatsapp],
        Field(description="Messaging product. Always 'whatsapp'."),
    ] = MessagingProduct.whatsapp
    status: Annotated[Literal["read"], Field(description="Status to set. Always 'read'.")] = "read"
    message_id: Annotated[str, Field(description="ID of the incoming message to mark as read.")]
    typing_indicator: Annotated[
        TypingIndicatorContent | None,
        Field(description="Optional typing indicator shown to the sender after the read receipt."),
    ] = None
