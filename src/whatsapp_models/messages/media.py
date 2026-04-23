"""Media message models: audio, image, video, document, sticker.

docs:
  audio:    https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages
  image:    https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/image-messages
  video:    https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/video-messages
  document: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/document-messages
  sticker:  https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/sticker-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.base import MessageBase


class OutgoingMediaObject(BaseModel):
    """Base media object. Exactly one of 'id' or 'link' must be provided."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str | None, Field(description="Media asset ID previously uploaded via the Media API.")] = None
    link: Annotated[str | None, Field(description="Publicly accessible URL of the media file.")] = None

    @model_validator(mode="after")
    def requires_id_or_link(self) -> "OutgoingMediaObject":
        """Ensure that exactly one of 'id' or 'link' is provided."""
        if self.id is None and self.link is None:
            raise ValueError("Either 'id' or 'link' must be provided.")
        return self


class CaptionedMediaObject(OutgoingMediaObject):
    """Media object that supports an optional text caption."""

    caption: Annotated[
        str | None, Field(description="Optional caption text displayed below the media.", max_length=1024)
    ] = None


class DocumentObject(CaptionedMediaObject):
    """Document media object with optional display filename."""

    filename: Annotated[str | None, Field(description="Filename shown to the recipient for the document.")] = None


class AudioMediaObject(OutgoingMediaObject):
    """Audio media object with optional voice flag for PTT (push-to-talk) messages."""

    voice: Annotated[
        bool,
        Field(description="Set to True when sending a WhatsApp voice message (PTT). Omit or False for regular audio."),
    ] = False


class AudioMessage(MessageBase):
    """Outgoing WhatsApp audio message."""

    type: Annotated[
        Literal[MessageType.audio],
        Field(description="Message type discriminator."),
    ] = MessageType.audio
    audio: Annotated[AudioMediaObject, Field(description="Audio media object.")]


class ImageMessage(MessageBase):
    """Outgoing WhatsApp image message."""

    type: Annotated[
        Literal[MessageType.image],
        Field(description="Message type discriminator."),
    ] = MessageType.image
    image: Annotated[CaptionedMediaObject, Field(description="Image media object.")]


class VideoMessage(MessageBase):
    """Outgoing WhatsApp video message."""

    type: Annotated[
        Literal[MessageType.video],
        Field(description="Message type discriminator."),
    ] = MessageType.video
    video: Annotated[CaptionedMediaObject, Field(description="Video media object.")]


class DocumentMessage(MessageBase):
    """Outgoing WhatsApp document message."""

    type: Annotated[
        Literal[MessageType.document],
        Field(description="Message type discriminator."),
    ] = MessageType.document
    document: Annotated[DocumentObject, Field(description="Document media object.")]


class StickerMessage(MessageBase):
    """Outgoing WhatsApp sticker message."""

    type: Annotated[
        Literal[MessageType.sticker],
        Field(description="Message type discriminator."),
    ] = MessageType.sticker
    sticker: Annotated[OutgoingMediaObject, Field(description="Sticker media object.")]
