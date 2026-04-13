"""Contact message models.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contacts-messages
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import AddressType, EmailType, MessageType, PhoneType, UrlType
from whatsapp_models.messages.base import MessageBase


class Address(BaseModel):
    """Physical address entry within a contact."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    street: Annotated[str | None, Field(description="Street name and number.")] = None
    city: Annotated[str | None, Field(description="City name.")] = None
    state: Annotated[str | None, Field(description="State or province abbreviation.")] = None
    zip: Annotated[str | None, Field(description="Postal or ZIP code.")] = None
    country: Annotated[str | None, Field(description="Full country name.")] = None
    country_code: Annotated[str | None, Field(description="ISO 3166-1 alpha-2 country code.")] = None
    type: Annotated[AddressType | None, Field(description="Address type: HOME or WORK.")] = None


class PhoneEntry(BaseModel):
    """Phone number entry within a contact."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    phone: Annotated[str | None, Field(description="Phone number in E.164 or local format.")] = None
    type: Annotated[PhoneType | None, Field(description="Phone type: CELL, MAIN, IPHONE, HOME or WORK.")] = None
    wa_id: Annotated[str | None, Field(description="WhatsApp ID of the phone number, without the '+' prefix.")] = None


class EmailEntry(BaseModel):
    """Email address entry within a contact."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    email: Annotated[str | None, Field(description="Email address.")] = None
    type: Annotated[EmailType | None, Field(description="Email type: HOME or WORK.")] = None


class UrlEntry(BaseModel):
    """URL entry within a contact."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    url: Annotated[str | None, Field(description="URL string.")] = None
    type: Annotated[UrlType | None, Field(description="URL type: HOME or WORK.")] = None


class ContactName(BaseModel):
    """Name fields for a contact entry."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    formatted_name: Annotated[str, Field(description="Full formatted name of the contact.")]
    first_name: Annotated[str | None, Field(description="First name.")] = None
    last_name: Annotated[str | None, Field(description="Last name.")] = None
    middle_name: Annotated[str | None, Field(description="Middle name.")] = None
    suffix: Annotated[str | None, Field(description="Name suffix (e.g. Jr., Sr.).")] = None
    prefix: Annotated[str | None, Field(description="Name prefix (e.g. Dr., Prof.).")] = None


class Contact(BaseModel):
    """A single contact entry in a contacts message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[ContactName, Field(description="Name fields of the contact.")]
    addresses: Annotated[list[Address], Field(description="List of physical addresses.")] = []
    birthday: Annotated[str | None, Field(description="Birthday in YYYY-MM-DD format.")] = None
    emails: Annotated[list[EmailEntry], Field(description="List of email addresses.")] = []
    org: Annotated[
        dict[str, str] | None,
        Field(description="Organization info with optional 'company', 'department', 'title'."),
    ] = None
    phones: Annotated[list[PhoneEntry], Field(description="List of phone numbers.")] = []
    urls: Annotated[list[UrlEntry], Field(description="List of URLs.")] = []


class ContactsMessage(MessageBase):
    """Outgoing WhatsApp contacts message."""

    type: Annotated[
        Literal[MessageType.contacts],
        Field(description="Message type discriminator."),
    ] = MessageType.contacts
    contacts: Annotated[
        list[Contact],
        Field(min_length=1, description="List of contacts to send. At least one required."),
    ]
