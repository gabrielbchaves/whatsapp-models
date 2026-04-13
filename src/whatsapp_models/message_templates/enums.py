"""Enums for template creation and management.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview
"""

from enum import StrEnum


class TemplateCategory(StrEnum):
    """Category that determines the pricing and policy rules for a template."""

    MARKETING = "MARKETING"
    UTILITY = "UTILITY"
    AUTHENTICATION = "AUTHENTICATION"


class TemplateStatus(StrEnum):
    """Review status of a message template."""

    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    PAUSED = "PAUSED"
    DISABLED = "DISABLED"
    IN_APPEAL = "IN_APPEAL"


class ComponentType(StrEnum):
    """Type of a template component."""

    HEADER = "HEADER"
    BODY = "BODY"
    FOOTER = "FOOTER"
    BUTTONS = "BUTTONS"


class HeaderFormat(StrEnum):
    """Media format for a HEADER component.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components
    """

    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    LOCATION = "LOCATION"


class ButtonType(StrEnum):
    """Type of button within a BUTTONS component.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components
    """

    QUICK_REPLY = "QUICK_REPLY"
    URL = "URL"
    PHONE_NUMBER = "PHONE_NUMBER"
    OTP = "OTP"
    FLOW = "FLOW"
    CATALOG = "CATALOG"
    MPM = "MPM"
    VOICE_CALL = "VOICE_CALL"
