"""Reaction message model.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/reaction-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.base import MessageBase


class ReactionObject(BaseModel):
    """Reaction payload targeting a specific received message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    message_id: Annotated[str, Field(description="WhatsApp message ID (wamid) of the message to react to.")]
    emoji: Annotated[str, Field(description="Emoji to apply as a reaction.")]


class ReactionMessage(MessageBase):
    """Outgoing WhatsApp reaction message."""

    type: Annotated[
        Literal[MessageType.reaction],
        Field(description="Message type discriminator."),
    ] = MessageType.reaction
    reaction: Annotated[ReactionObject, Field(description="Reaction payload.")]
