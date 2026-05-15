"""Webhook notification envelope and nested structures.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview
"""

from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import Language
from whatsapp_models.message_templates.enums import ButtonType, TemplateCategory, TemplateStatus
from whatsapp_models.message_templates.enums import TemplateQualityScore as TemplateQualityScore
from whatsapp_models.messages.base import MessagingProduct
from whatsapp_models.webhooks.errors import WebhookError
from whatsapp_models.webhooks.messages import IncomingGroupMessage, IncomingMessage
from whatsapp_models.webhooks.statuses import MessageStatus


class ChangeField(StrEnum):
    """Possible values for the 'field' property of a webhook Change object."""

    messages = "messages"
    group_lifecycle_update = "group_lifecycle_update"
    group_settings_update = "group_settings_update"
    group_participant_update = "group_participant_update"
    message_template_status_update = "message_template_status_update"
    message_template_quality_update = "message_template_quality_update"
    message_template_components_update = "message_template_components_update"


class Metadata(BaseModel):
    """Phone number metadata included in every webhook Value object."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    display_phone_number: Annotated[str, Field(description="The display phone number for the business.")]
    phone_number_id: Annotated[str, Field(description="ID of the phone number in the WhatsApp Business Account.")]


class GroupParticipant(BaseModel):
    """A participant added or removed in a group lifecycle event."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    input: Annotated[str | None, Field(description="Phone number or WhatsApp ID as provided.")] = None
    wa_id: Annotated[str | None, Field(description="Resolved WhatsApp ID of the participant.")] = None


class GroupEventType(StrEnum):
    """Type of group lifecycle event."""

    group_create = "group_create"
    group_delete = "group_delete"
    group_settings_update = "group_settings_update"
    group_add_participants = "group_add_participants"
    group_remove_participants = "group_remove_participants"


class GroupEvent(BaseModel):
    """A group lifecycle event received via webhook (create, delete, participants change)."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    timestamp: Annotated[int, Field(description="Unix timestamp of the event.")]
    group_id: Annotated[str, Field(description="ID of the affected group.")]
    type: Annotated[GroupEventType, Field(description="Type of group lifecycle event.")]
    request_id: Annotated[str, Field(description="Unique ID for this event request.")]
    subject: Annotated[str | None, Field(description="Group subject, present for create/settings events.")] = None
    description: Annotated[str | None, Field(description="Group description, present for create events.")] = None
    added_participants: Annotated[Sequence[GroupParticipant], Field(description="Participants added.")] = []
    removed_participants: Annotated[Sequence[GroupParticipant], Field(description="Participants removed.")] = []


class NotificationContactProfile(BaseModel):
    """Profile information included in a webhook contact entry."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[str, Field(description="Display name of the contact.")]


class NotificationContact(BaseModel):
    """Sender profile information included in a webhook Value object."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    wa_id: Annotated[str, Field(description="WhatsApp ID of the sender.")]
    user_id: Annotated[str | None, Field(description="Platform user ID of the sender.")] = None
    profile: Annotated[
        NotificationContactProfile | None,
        Field(description="Profile information of the sender."),
    ] = None


class TemplateDisableInfo(BaseModel):
    """Disable timestamp included when a template is disabled."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    disable_date: Annotated[str, Field(description="Timestamp at which the template was disabled.")]


class TemplateOtherInfo(BaseModel):
    """Title and description included when a template is locked or unlocked."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    title: Annotated[str, Field(description="Title of the lock/unlock notification.")]
    description: Annotated[str, Field(description="Description of the lock/unlock notification.")]


class TemplateRejectionInfo(BaseModel):
    """Rejection details included when a template is rejected with INVALID_FORMAT."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    reason: Annotated[str, Field(description="Reason for the rejection.")]
    recommendation: Annotated[str, Field(description="Recommendation to resolve the rejection.")]


class TemplateStatusUpdateValue(BaseModel):
    """Value payload for a message_template_status_update webhook change."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    event: Annotated[TemplateStatus, Field(description="New status of the template.")]
    message_template_id: Annotated[int, Field(description="ID of the affected template.")]
    message_template_name: Annotated[str, Field(description="Name of the affected template.")]
    message_template_language: Annotated[Language, Field(description="Language code of the affected template.")]
    message_template_category: Annotated[
        TemplateCategory | None, Field(description="Category of the affected template.")
    ] = None
    reason: Annotated[str | None, Field(description="Reason for rejection or pause, if applicable.")] = None
    disable_info: Annotated[
        TemplateDisableInfo | None, Field(description="Disable date. Present only when the template is disabled.")
    ] = None
    other_info: Annotated[
        TemplateOtherInfo | None,
        Field(description="Lock/unlock details. Present only when the template is locked or unlocked."),
    ] = None
    rejection_info: Annotated[
        TemplateRejectionInfo | None,
        Field(description="Rejection details. Present only when the template is rejected with INVALID_FORMAT."),
    ] = None


class TemplateQualityUpdateValue(BaseModel):
    """Value payload for a message_template_quality_update webhook change."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    message_template_id: Annotated[int, Field(description="ID of the affected template.")]
    message_template_name: Annotated[str, Field(description="Name of the affected template.")]
    message_template_language: Annotated[Language, Field(description="Language code of the affected template.")]
    previous_quality_score: Annotated[TemplateQualityScore, Field(description="Previous quality score.")]
    new_quality_score: Annotated[TemplateQualityScore, Field(description="New quality score.")]


class TemplateButtonUpdate(BaseModel):
    """A button entry inside a message_template_components_update payload."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    message_template_button_type: Annotated[ButtonType, Field(description="Button type.")]
    message_template_button_text: Annotated[str, Field(description="Label text of the button.")]
    message_template_button_url: Annotated[
        str | None, Field(description="Button URL. Present only for URL buttons.")
    ] = None
    message_template_button_phone_number: Annotated[
        str | None, Field(description="Phone number. Present only for PHONE_NUMBER buttons.")
    ] = None


class TemplateComponentsUpdateValue(BaseModel):
    """Value payload for a message_template_components_update webhook change."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    message_template_id: Annotated[int, Field(description="ID of the affected template.")]
    message_template_name: Annotated[str, Field(description="Name of the affected template.")]
    message_template_language: Annotated[Language, Field(description="Language code of the affected template.")]
    message_template_element: Annotated[str, Field(description="Body text of the template.")]
    message_template_title: Annotated[
        str | None, Field(description="Header text. Present only when the template has a text header.")
    ] = None
    message_template_footer: Annotated[
        str | None, Field(description="Footer text. Present only when the template has a footer.")
    ] = None
    message_template_buttons: Annotated[
        Sequence[TemplateButtonUpdate],
        Field(description="Buttons. Present only when the template has URL or phone number buttons."),
    ] = []


class Value(BaseModel):
    """Value object containing the actual notification payload inside a Change."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    messaging_product: Annotated[MessagingProduct, Field(description="Always 'whatsapp'.")]
    metadata: Annotated[
        Metadata,
        Field(description="Metadata identifying the receiving phone number."),
    ]
    contacts: Annotated[
        Sequence[NotificationContact],
        Field(description="Contact profile information for the sender."),
    ] = []
    messages: Annotated[
        Sequence[IncomingGroupMessage | IncomingMessage],
        Field(description="List of incoming messages. Group messages are resolved before direct messages."),
    ] = []
    statuses: Annotated[
        Sequence[MessageStatus],
        Field(description="List of message delivery status updates."),
    ] = []
    errors: Annotated[
        Sequence[WebhookError],
        Field(description="List of errors reported by the platform."),
    ] = []
    groups: Annotated[
        Sequence[GroupEvent],
        Field(description="List of group lifecycle events."),
    ] = []


class MessagesChange(BaseModel):
    """Change entry for messages, statuses, and group events."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    field: Annotated[
        Literal[
            ChangeField.messages,
            ChangeField.group_lifecycle_update,
            ChangeField.group_settings_update,
            ChangeField.group_participant_update,
        ],
        Field(description="The field that changed."),
    ]
    value: Annotated[Value, Field(description="The payload associated with this change.")]


class TemplateStatusChange(BaseModel):
    """Change entry for message_template_status_update events."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    field: Annotated[
        Literal[ChangeField.message_template_status_update],
        Field(description="The field that changed."),
    ]
    value: Annotated[TemplateStatusUpdateValue, Field(description="The payload associated with this change.")]


class TemplateQualityChange(BaseModel):
    """Change entry for message_template_quality_update events."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    field: Annotated[
        Literal[ChangeField.message_template_quality_update],
        Field(description="The field that changed."),
    ]
    value: Annotated[TemplateQualityUpdateValue, Field(description="The payload associated with this change.")]


class TemplateComponentsChange(BaseModel):
    """Change entry for message_template_components_update events."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    field: Annotated[
        Literal[ChangeField.message_template_components_update],
        Field(description="The field that changed."),
    ]
    value: Annotated[TemplateComponentsUpdateValue, Field(description="The payload associated with this change.")]


Change = Annotated[
    MessagesChange | TemplateStatusChange | TemplateQualityChange | TemplateComponentsChange,
    Field(discriminator="field"),
]
"""Discriminated union of all webhook change types, resolved by the 'field' value."""


class Entry(BaseModel):
    """A single entry in the webhook notification, representing one WhatsApp Business Account."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="WhatsApp Business Account ID.")]
    changes: Annotated[Sequence[Change], Field(description="List of changes included in this entry.")]


class WebhookNotification(BaseModel):
    """Root envelope of every WhatsApp webhook notification.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    object: Annotated[Literal["whatsapp_business_account"], Field(description="Always 'whatsapp_business_account'.")]
    entry: Annotated[Sequence[Entry], Field(description="List of entries, one per WhatsApp Business Account.")]
