"""Template creation request and API response models.

docs:
  create: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-management#create-templates
  manage: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-management
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.message_templates.components import TemplateComponent
from whatsapp_models.message_templates.enums import TemplateCategory, TemplateStatus


class CreateTemplateRequest(BaseModel):
    """Payload for creating a new WhatsApp message template via the API."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[
        str,
        Field(description="Template name. Only lowercase alphanumeric characters and underscores allowed."),
    ]
    language: Annotated[str, Field(description="BCP-47 language code for the template (e.g. 'pt_BR').")]
    category: Annotated[
        TemplateCategory,
        Field(description="Template category that determines pricing and policy rules."),
    ]
    components: Annotated[
        list[TemplateComponent],
        Field(description="List of template components: HEADER, BODY, FOOTER, BUTTONS."),
    ] = []
    allow_category_change: Annotated[
        bool,
        Field(description="When True, Meta may re-categorize the template if the chosen category is incorrect."),
    ] = False


class TemplateResponse(BaseModel):
    """API response returned after creating or updating a template."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Unique identifier of the created or updated template.")]
    status: Annotated[TemplateStatus, Field(description="Current review status of the template.")]
    category: Annotated[TemplateCategory, Field(description="Category assigned to the template after creation.")]
