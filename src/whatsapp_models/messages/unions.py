"""Discriminated unions for outgoing messages.

OutgoingMessage resolves the correct model from the top-level `type` field.
For interactive messages, the nested `interactive.type` field further
discriminates the sub-type via InteractiveObject inside InteractiveMessage.
"""

from typing import Annotated

from pydantic import Field

from whatsapp_models.messages.contacts import ContactsMessage
from whatsapp_models.messages.interactive import InteractiveMessage
from whatsapp_models.messages.location import LocationMessage
from whatsapp_models.messages.media import (
    AudioMessage,
    DocumentMessage,
    ImageMessage,
    StickerMessage,
    VideoMessage,
)
from whatsapp_models.messages.reaction import ReactionMessage
from whatsapp_models.messages.template import TemplateMessage
from whatsapp_models.messages.text import TextMessage

OutgoingMessage = Annotated[
    TextMessage
    | AudioMessage
    | ImageMessage
    | VideoMessage
    | DocumentMessage
    | StickerMessage
    | LocationMessage
    | ContactsMessage
    | ReactionMessage
    | TemplateMessage
    | InteractiveMessage,
    Field(discriminator="type"),
]
