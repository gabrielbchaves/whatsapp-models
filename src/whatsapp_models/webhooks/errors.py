"""Error model reported inside webhook payloads.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages
"""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field


class WebhookError(BaseModel):
    """Error object reported by the WhatsApp platform inside webhook notifications."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    code: Annotated[int, Field(description="Error code reported by the platform.")]
    title: Annotated[str, Field(description="Short description of the error.")]
    message: Annotated[str | None, Field(description="Detailed error message.")] = None
    error_data: Annotated[dict[str, Any] | None, Field(description="Additional error metadata.")] = None
    href: Annotated[str | None, Field(description="Link to error documentation.")] = None
