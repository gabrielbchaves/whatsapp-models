"""Webhook notification envelope and nested structures.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview
"""

from enum import StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.webhooks.errors import WebhookError
from whatsapp_models.webhooks.messages import IncomingGroupMessage, IncomingMessage
from whatsapp_models.webhooks.statuses import MessageStatus


class ChangeField(StrEnum):
    """Possible values for the 'field' property of a webhook Change object."""

    messages = "messages"
    group_lifecycle_update = "group_lifecycle_update"
    group_settings_update = "group_settings_update"
    group_participant_update = "group_participant_update"


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
    added_participants: Annotated[list[GroupParticipant], Field(description="Participants added.")] = []
    removed_participants: Annotated[list[GroupParticipant], Field(description="Participants removed.")] = []


class Value(BaseModel):
    """Value object containing the actual notification payload inside a Change."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    messaging_product: Annotated[str, Field(description="Always 'whatsapp'.")]
    metadata: Annotated[Metadata, Field(description="Metadata identifying the receiving phone number.")]
    contacts: Annotated[list[dict[str, Any]], Field(description="Contact profile information for the sender.")] = []
    messages: Annotated[
        list[IncomingGroupMessage | IncomingMessage],
        Field(description="List of incoming messages. Group messages are resolved before direct messages."),
    ] = []
    statuses: Annotated[list[MessageStatus], Field(description="List of message delivery status updates.")] = []
    errors: Annotated[list[WebhookError], Field(description="List of errors reported by the platform.")] = []
    groups: Annotated[list[GroupEvent], Field(description="List of group lifecycle events.")] = []


class Change(BaseModel):
    """A single change entry inside a webhook Entry."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    field: Annotated[ChangeField, Field(description="The field that changed.")]
    value: Annotated[Value, Field(description="The payload associated with this change.")]


class Entry(BaseModel):
    """A single entry in the webhook notification, representing one WhatsApp Business Account."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="WhatsApp Business Account ID.")]
    changes: Annotated[list[Change], Field(description="List of changes included in this entry.")]


class WebhookNotification(BaseModel):
    """Root envelope of every WhatsApp webhook notification.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    object: Annotated[str, Field(description="Always 'whatsapp_business_account'.")]
    entry: Annotated[list[Entry], Field(description="List of entries, one per WhatsApp Business Account.")]
