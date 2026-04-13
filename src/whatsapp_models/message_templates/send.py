"""Template send parameter types and language selector.

These models are used when filling template variables in an outgoing message.
Media-based parameters (document, image, video) and the message envelope itself
live in messages.template, which depends on messages.media.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/template-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import Language


class TemplateLanguage(BaseModel):
    """Language selector for a template message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    code: Annotated[Language, Field(description="BCP-47 language code for the template to be sent.")]
    policy: Annotated[
        Literal["deterministic"],
        Field(description="Language policy. Always 'deterministic'."),
    ] = "deterministic"


class CurrencyObject(BaseModel):
    """Currency value for a template currency parameter."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    fallback_value: Annotated[str, Field(description="Default text if localisation fails.")]
    code: Annotated[str, Field(description="ISO 4217 currency code.")]
    amount_1000: Annotated[int, Field(description="Amount multiplied by 1000.")]


class DateTimeObject(BaseModel):
    """DateTime value for a template date_time parameter."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    fallback_value: Annotated[str, Field(description="Default text if localisation fails.")]


class TextParameter(BaseModel):
    """Template parameter of type 'text'."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["text"], Field(description="Parameter type discriminator.")] = "text"
    text: Annotated[str, Field(description="Text value for the parameter.")]


class CurrencyParameter(BaseModel):
    """Template parameter of type 'currency'."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["currency"], Field(description="Parameter type discriminator.")] = "currency"
    currency: Annotated[CurrencyObject, Field(description="Currency object.")]


class DateTimeParameter(BaseModel):
    """Template parameter of type 'date_time'."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["date_time"], Field(description="Parameter type discriminator.")] = "date_time"
    date_time: Annotated[DateTimeObject, Field(description="DateTime object.")]


class ButtonPayloadParameter(BaseModel):
    """Button parameter carrying a dynamic payload (quick_reply buttons)."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["payload"], Field(description="Parameter type discriminator.")] = "payload"
    payload: Annotated[str, Field(description="Developer-defined payload for quick_reply buttons.")]


class ButtonTextParameter(BaseModel):
    """Button parameter carrying dynamic URL suffix text (url buttons)."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["text"], Field(description="Parameter type discriminator.")] = "text"
    text: Annotated[str, Field(description="URL suffix appended to the static URL in a url button.")]


ButtonParameter = Annotated[
    ButtonPayloadParameter | ButtonTextParameter,
    Field(discriminator="type"),
]
"""Discriminated union of button parameter types."""
