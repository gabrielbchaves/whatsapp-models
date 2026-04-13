"""Phone number models for the WhatsApp Business API.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers
"""

from enum import StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field


class QualityRating(StrEnum):
    """Quality rating of a WhatsApp Business phone number."""

    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"
    NA = "NA"


class ThroughputLevel(StrEnum):
    """Message throughput level of a WhatsApp Business phone number."""

    STANDARD = "STANDARD"
    HIGH = "HIGH"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class PhoneNumber(BaseModel):
    """A WhatsApp Business phone number with its associated metadata.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Phone number ID in the WhatsApp Business Account.")]
    display_phone_number: Annotated[str, Field(description="Human-readable phone number.")]
    verified_name: Annotated[str, Field(description="Verified display name for the business.")]
    quality_rating: Annotated[
        QualityRating | None, Field(description="Current quality rating of the phone number.")
    ] = None
    platform_type: Annotated[str | None, Field(description="Platform type, e.g. 'CLOUD_API' or 'ON_PREMISE'.")] = None
    throughput: Annotated[ThroughputLevel | None, Field(description="Messaging throughput level.")] = None
    status: Annotated[str | None, Field(description="Current status of the phone number.")] = None
    country_code: Annotated[str | None, Field(description="ISO 3166-1 alpha-2 country code.")] = None
    country_dial_code: Annotated[str | None, Field(description="Country dial code, e.g. '55' for Brazil.")] = None


class PhoneNumberRegistration(BaseModel):
    """Payload for registering a phone number with the WhatsApp Business API.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    pin: Annotated[str, Field(description="Two-step verification PIN for the phone number.")]


class PhoneNumberList(BaseModel):
    """Paginated list of phone numbers returned by the API.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    data: Annotated[list[PhoneNumber], Field(description="List of phone number objects.")]
    paging: Annotated[
        dict[str, Any] | None, Field(description="Pagination cursors for traversing large result sets.")
    ] = None
