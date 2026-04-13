"""Outgoing template message models.

Parameter primitives (TemplateLanguage, TextParameter, CurrencyParameter, etc.)
are defined in message_templates.send. This module adds the media parameters
that depend on messages.media, the send component, and the message envelope.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/template-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import MessageType
from whatsapp_models.message_templates.send import (
    ButtonParameter,
    ButtonPayloadParameter,
    ButtonTextParameter,
    CurrencyObject,
    CurrencyParameter,
    DateTimeObject,
    DateTimeParameter,
    TemplateLanguage,
    TextParameter,
)
from whatsapp_models.messages.base import MessageBase
from whatsapp_models.messages.media import MediaObject


class DocumentParameter(BaseModel):
    """Template parameter of type 'document'."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["document"], Field(description="Parameter type discriminator.")] = "document"
    document: Annotated[MediaObject, Field(description="Document media object.")]


class ImageParameter(BaseModel):
    """Template parameter of type 'image'."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["image"], Field(description="Parameter type discriminator.")] = "image"
    image: Annotated[MediaObject, Field(description="Image media object.")]


class VideoParameter(BaseModel):
    """Template parameter of type 'video'."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["video"], Field(description="Parameter type discriminator.")] = "video"
    video: Annotated[MediaObject, Field(description="Video media object.")]


TemplateParameter = Annotated[
    TextParameter | CurrencyParameter | DateTimeParameter | DocumentParameter | ImageParameter | VideoParameter,
    Field(discriminator="type"),
]
"""Discriminated union of all template parameter types."""


class TemplateSendComponent(BaseModel):
    """A component of a template message containing parameters to fill."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal["header", "body", "button"],
        Field(description="Component type: header, body, or button."),
    ]
    sub_type: Annotated[
        Literal["quick_reply", "url", "catalog"] | None,
        Field(description="Button sub-type. Required when type is 'button'."),
    ] = None
    index: Annotated[
        str | None,
        Field(description="Zero-based index of the button. Required when type is 'button'."),
    ] = None
    parameters: Annotated[
        list[TemplateParameter] | list[ButtonParameter],
        Field(description="List of parameter values to fill the component."),
    ] = []


class TemplateObject(BaseModel):
    """Template reference with language and optional component parameters."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[str, Field(description="Name of the approved template to send.")]
    language: Annotated[TemplateLanguage, Field(description="Language in which to send the template.")]
    components: Annotated[
        list[TemplateSendComponent], Field(description="List of components with filled parameters.")
    ] = []


class TemplateMessage(MessageBase):
    """Outgoing WhatsApp template message."""

    type: Annotated[
        Literal[MessageType.template],
        Field(description="Message type discriminator."),
    ] = MessageType.template
    template: Annotated[TemplateObject, Field(description="Template reference and parameter payload.")]


# Re-export primitives so importers of messages.template get the full set
__all__ = [
    "ButtonParameter",
    "ButtonPayloadParameter",
    "ButtonTextParameter",
    "CurrencyObject",
    "CurrencyParameter",
    "DateTimeObject",
    "DateTimeParameter",
    "DocumentParameter",
    "ImageParameter",
    "TemplateLanguage",
    "TemplateMessage",
    "TemplateObject",
    "TemplateParameter",
    "TemplateSendComponent",
    "TextParameter",
    "VideoParameter",
]
