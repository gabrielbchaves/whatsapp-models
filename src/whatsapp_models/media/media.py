"""Media upload response and reference models.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MediaUploadResponse(BaseModel):
    """Response returned by the WhatsApp API after a successful media upload."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Media asset ID assigned by WhatsApp after upload.")]


class MediaObject(BaseModel):
    """Reference to a media asset, either by uploaded ID or hosted URL.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str | None, Field(description="Media asset ID returned by the upload API.")] = None
    link: Annotated[str | None, Field(description="Publicly hosted URL of the media file.")] = None
    caption: Annotated[str | None, Field(description="Optional caption displayed with the media.")] = None
    filename: Annotated[str | None, Field(description="Optional filename, used for document messages.")] = None

    @model_validator(mode="after")
    def require_id_or_link(self) -> "MediaObject":
        """Ensure that at least one of id or link is provided."""
        if self.id is None and self.link is None:
            raise ValueError("Either 'id' or 'link' must be provided.")
        return self
