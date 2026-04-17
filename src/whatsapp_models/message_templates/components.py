"""Template component models and their discriminated union.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components
"""

from collections.abc import Sequence
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.message_templates.enums import ButtonType, ComponentType, HeaderFormat


class HeaderComponent(BaseModel):
    """HEADER component of a template. Supports text, image, video, document, or location."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ComponentType.HEADER],
        Field(description="Component type discriminator."),
    ] = ComponentType.HEADER
    format: Annotated[HeaderFormat, Field(description="Media format of the header.")]
    text: Annotated[
        str | None,
        Field(description="Header text with optional {{N}} variables. Used when format is TEXT."),
    ] = None
    example: Annotated[
        dict[str, Any] | None,
        Field(description="Example values for header variables or media handle."),
    ] = None


class BodyComponent(BaseModel):
    """BODY component of a template. Contains the main message text with optional variables."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ComponentType.BODY],
        Field(description="Component type discriminator."),
    ] = ComponentType.BODY
    text: Annotated[str, Field(description="Body text with optional {{N}} variables.")]
    example: Annotated[
        dict[str, Any] | None,
        Field(description="Example values for body text variables, keyed by 'body_text'."),
    ] = None


class FooterComponent(BaseModel):
    """FOOTER component of a template. Displays a short text below the body."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ComponentType.FOOTER],
        Field(description="Component type discriminator."),
    ] = ComponentType.FOOTER
    text: Annotated[str, Field(description="Footer text. Does not support variables.")]


class QuickReplyButton(BaseModel):
    """A QUICK_REPLY button that the user can tap to send a predefined reply."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ButtonType.QUICK_REPLY],
        Field(description="Button type discriminator."),
    ] = ButtonType.QUICK_REPLY
    text: Annotated[str, Field(description="Button label shown to the user. Max 25 characters.")]


class UrlButton(BaseModel):
    """A URL button that opens a web page when tapped."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ButtonType.URL],
        Field(description="Button type discriminator."),
    ] = ButtonType.URL
    text: Annotated[str, Field(description="Button label shown to the user. Max 25 characters.")]
    url: Annotated[
        str,
        Field(description="URL opened when the button is tapped. Supports one {{1}} variable."),
    ]
    example: Annotated[
        Sequence[str],
        Field(description="Example value for the URL variable."),
    ] = []


class PhoneNumberButton(BaseModel):
    """A PHONE_NUMBER button that dials a number when tapped."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ButtonType.PHONE_NUMBER],
        Field(description="Button type discriminator."),
    ] = ButtonType.PHONE_NUMBER
    text: Annotated[str, Field(description="Button label shown to the user. Max 25 characters.")]
    phone_number: Annotated[
        str,
        Field(description="Phone number dialed when the button is tapped, in E.164 format."),
    ]


class OtpButton(BaseModel):
    """An OTP button used in authentication templates to copy or autofill a one-time password."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ButtonType.OTP],
        Field(description="Button type discriminator."),
    ] = ButtonType.OTP
    otp_type: Annotated[
        str,
        Field(description="OTP delivery mechanism: COPY_CODE or ONE_TAP."),
    ]
    text: Annotated[
        str | None,
        Field(description="Button label override. Defaults to 'Copy Code' or 'Autofill'."),
    ] = None
    autofill_text: Annotated[
        str | None,
        Field(description="Button label for ONE_TAP autofill. Max 25 characters."),
    ] = None
    package_name: Annotated[
        str | None,
        Field(description="Android app package name. Required for ONE_TAP."),
    ] = None
    signature_hash: Annotated[
        str | None,
        Field(description="Android app signature hash. Required for ONE_TAP."),
    ] = None


Button = Annotated[
    QuickReplyButton | UrlButton | PhoneNumberButton | OtpButton,
    Field(discriminator="type"),
]
"""Discriminated union of all button types within a BUTTONS component."""


class ButtonsComponent(BaseModel):
    """BUTTONS component of a template. Contains one or more interactive buttons."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal[ComponentType.BUTTONS],
        Field(description="Component type discriminator."),
    ] = ComponentType.BUTTONS
    buttons: Annotated[
        Sequence[Button],
        Field(min_length=1, description="List of buttons. Max 10 total, with specific limits per type combination."),
    ]


TemplateComponent = Annotated[
    HeaderComponent | BodyComponent | FooterComponent | ButtonsComponent,
    Field(discriminator="type"),
]
"""Discriminated union of all template component types, resolved by the type field."""
