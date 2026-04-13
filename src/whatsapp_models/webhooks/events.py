"""Webhook event models for account and history notifications.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update
doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/history
"""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field


class AccountUpdateEvent(BaseModel):
    """Account-level update event received via webhook, e.g. ban state changes.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    phone_number: Annotated[str, Field(description="Phone number associated with the account update.")]
    event: Annotated[str, Field(description="Type of account update event.")]
    ban_info: Annotated[
        dict[str, Any] | None,
        Field(description="Ban state information, present when the account is banned or scheduled for disabling."),
    ] = None


class HistoryEvent(BaseModel):
    """Phone number history event received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/history
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[str, Field(description="History event type.")]
    id: Annotated[str | None, Field(description="Resource ID associated with the history event.")] = None
