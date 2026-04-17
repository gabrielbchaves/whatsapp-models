"""Delivery status models for webhook notifications.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status
"""

from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.webhooks.errors import WebhookError


class DeliveryStatus(StrEnum):
    """Possible delivery states for an outgoing WhatsApp message."""

    sent = "sent"
    delivered = "delivered"
    read = "read"
    failed = "failed"


class ConversationOrigin(BaseModel):
    """Origin of a conversation billing entry."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[str | None, Field(description="Conversation category, e.g. 'business_initiated'.")] = None


class Conversation(BaseModel):
    """Conversation window metadata attached to a message status update."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str | None, Field(description="Conversation ID.")] = None
    expiration_timestamp: Annotated[
        str | None, Field(description="Unix timestamp when the conversation window expires.")
    ] = None
    origin: Annotated[ConversationOrigin | None, Field(description="Conversation origin and billing category.")] = None


class Pricing(BaseModel):
    """Pricing information attached to a message status update."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    billable: Annotated[bool | None, Field(description="Whether this message is billable.")] = None
    pricing_model: Annotated[Literal["CBP", "PMP"] | None, Field(description="Pricing model applied.")] = None
    category: Annotated[str | None, Field(description="Conversation category for billing purposes.")] = None


class MessageStatus(BaseModel):
    """Status update for a previously sent message, received via webhook."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="WhatsApp message ID (wamid).")]
    status: Annotated[DeliveryStatus, Field(description="Delivery state of the message.")]
    timestamp: Annotated[str, Field(description="Unix timestamp of the status update as a string.")]
    recipient_id: Annotated[str, Field(description="Phone number of the message recipient.")]
    group_id: Annotated[str | None, Field(description="Group ID, present when the message was sent to a group.")] = None
    conversation: Annotated[Conversation | None, Field(description="Conversation window metadata.")] = None
    pricing: Annotated[Pricing | None, Field(description="Pricing information for this message.")] = None
    errors: Annotated[
        Sequence[WebhookError],
        Field(description="List of errors, present when status is 'failed'."),
    ] = []
