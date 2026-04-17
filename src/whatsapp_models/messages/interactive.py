"""Interactive message models.

Covers: reply buttons, list, CTA URL, flow, location request, call permission request, product, product list.

The top-level InteractiveMessage uses a discriminated union on interactive.type
to resolve the correct sub-type.

docs:
  reply buttons:    https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-reply-buttons-messages
  list:             https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-list-messages
  CTA URL:          https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-cta-url-messages
  flow:             https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-flow-messages
  location request: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-location-request-messages
"""

from collections.abc import Sequence
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.base import MessageBase


class InteractiveBody(BaseModel):
    """Body text displayed in an interactive message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    text: Annotated[str, Field(description="Body text of the interactive message.", max_length=1024)]


class InteractiveHeader(BaseModel):
    """Optional header for interactive messages. Supports text, image, video, or document."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["text", "image", "video", "document"], Field(description="Header type.")]
    text: Annotated[str | None, Field(description="Header text, used when type is 'text'.", max_length=60)] = None
    sub_text: Annotated[
        str | None, Field(description="Secondary header text, used when type is 'text'.", max_length=60)
    ] = None
    image: Annotated[dict[str, Any] | None, Field(description="Image media object, used when type is 'image'.")] = None
    video: Annotated[dict[str, Any] | None, Field(description="Video media object, used when type is 'video'.")] = None
    document: Annotated[
        dict[str, Any] | None,
        Field(description="Document media object, used when type is 'document'."),
    ] = None


class InteractiveFooter(BaseModel):
    """Optional footer text for interactive messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    text: Annotated[str, Field(description="Footer text of the interactive message.", max_length=60)]


class ReplyButton(BaseModel):
    """Identifier and label for a reply button."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Unique identifier for the button, returned in the webhook on selection.")]
    title: Annotated[str, Field(description="Button label shown to the user. Max 20 characters.")]


class Button(BaseModel):
    """A single reply button entry."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["reply"], Field(description="Button type. Always 'reply'.")]
    reply: Annotated[ReplyButton, Field(description="Reply button identifier and label.")]


class ReplyButtonsAction(BaseModel):
    """Action payload for reply buttons interactive messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    buttons: Annotated[
        Sequence[Button],
        Field(min_length=1, max_length=3, description="List of reply buttons. Min 1, max 3."),
    ]


class ReplyButtonsInteractive(BaseModel):
    """Interactive object for reply buttons messages (interactive.type = 'button')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["button"], Field(description="Interactive sub-type discriminator.")] = "button"
    body: Annotated[InteractiveBody, Field(description="Body text of the message.")]
    action: Annotated[ReplyButtonsAction, Field(description="Action containing the reply buttons.")]
    header: Annotated[InteractiveHeader | None, Field(description="Optional message header.")] = None
    footer: Annotated[InteractiveFooter | None, Field(description="Optional message footer.")] = None


class ListRow(BaseModel):
    """A single selectable row in a list section."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[
        str, Field(description="Unique identifier for the row, returned in the webhook on selection.", max_length=200)
    ]
    title: Annotated[str, Field(description="Row label shown to the user.", max_length=24)]
    description: Annotated[str | None, Field(description="Optional row description.", max_length=72)] = None


class ListSection(BaseModel):
    """A section grouping rows in a list message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    title: Annotated[
        str | None,
        Field(description="Section title, required when more than one section is present.", max_length=24),
    ] = None
    rows: Annotated[Sequence[ListRow], Field(description="List of selectable rows in this section.")]


class ListAction(BaseModel):
    """Action payload for list messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    button: Annotated[str, Field(description="Label of the button that opens the list. Max 20 characters.")]
    sections: Annotated[
        Sequence[ListSection],
        Field(min_length=1, max_length=10, description="List of sections. Min 1, max 10."),
    ]


class ListInteractive(BaseModel):
    """Interactive object for list messages (interactive.type = 'list')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["list"], Field(description="Interactive sub-type discriminator.")] = "list"
    body: Annotated[InteractiveBody, Field(description="Body text of the message.")]
    action: Annotated[ListAction, Field(description="Action containing list sections and rows.")]
    header: Annotated[InteractiveHeader | None, Field(description="Optional message header.")] = None
    footer: Annotated[InteractiveFooter | None, Field(description="Optional message footer.")] = None


class CtaUrlParameters(BaseModel):
    """Parameters for the CTA URL button action."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    display_text: Annotated[str, Field(description="Button label shown to the user.")]
    url: Annotated[str, Field(description="URL opened when the user taps the button.")]


class CtaUrlAction(BaseModel):
    """Action payload for CTA URL button messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[Literal["cta_url"], Field(description="Action name. Always 'cta_url'.")]
    parameters: Annotated[CtaUrlParameters, Field(description="Display text and target URL for the button.")]


class CtaUrlInteractive(BaseModel):
    """Interactive object for CTA URL button messages (interactive.type = 'cta_url')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["cta_url"], Field(description="Interactive sub-type discriminator.")] = "cta_url"
    body: Annotated[InteractiveBody, Field(description="Body text of the message.")]
    action: Annotated[CtaUrlAction, Field(description="Action containing the CTA URL button.")]
    header: Annotated[InteractiveHeader | None, Field(description="Optional message header.")] = None
    footer: Annotated[InteractiveFooter | None, Field(description="Optional message footer.")] = None


class FlowParameters(BaseModel):
    """Parameters for a Flow interactive message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    flow_message_version: Annotated[str, Field(description="Flow message spec version. Use '3'.")]
    flow_token: Annotated[
        str,
        Field(description="Unique token generated by the business to identify this flow session."),
    ]
    flow_id: Annotated[str, Field(description="Identifier of the Flow to open.")]
    flow_cta: Annotated[str, Field(description="Button label that opens the Flow. Max 30 characters.", max_length=30)]
    flow_action: Annotated[
        Literal["navigate", "data_exchange"],
        Field(description="Flow action: 'navigate' to open a specific screen, 'data_exchange' for custom data."),
    ] = "navigate"
    flow_action_payload: Annotated[
        dict[str, Any] | None,
        Field(description="Payload passed to the first screen when flow_action is 'navigate'."),
    ] = None


class FlowAction(BaseModel):
    """Action payload for Flow messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[Literal["flow"], Field(description="Action name. Always 'flow'.")]
    parameters: Annotated[FlowParameters, Field(description="Flow configuration parameters.")]


class FlowInteractive(BaseModel):
    """Interactive object for Flow messages (interactive.type = 'flow')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["flow"], Field(description="Interactive sub-type discriminator.")] = "flow"
    body: Annotated[InteractiveBody, Field(description="Body text of the message.")]
    action: Annotated[FlowAction, Field(description="Action containing Flow parameters.")]
    header: Annotated[InteractiveHeader | None, Field(description="Optional message header.")] = None
    footer: Annotated[InteractiveFooter | None, Field(description="Optional message footer.")] = None


class LocationRequestAction(BaseModel):
    """Action payload for location request messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[Literal["send_location"], Field(description="Action name. Always 'send_location'.")]


class LocationRequestInteractive(BaseModel):
    """Interactive object for location request messages (interactive.type = 'location_request_message')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal["location_request_message"],
        Field(description="Interactive sub-type discriminator."),
    ] = "location_request_message"
    body: Annotated[InteractiveBody, Field(description="Body text prompting the user to share their location.")]
    action: Annotated[LocationRequestAction, Field(description="Action triggering the location share prompt.")]


class CallPermissionRequestAction(BaseModel):
    """Action payload for call permission request messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[
        Literal["call_permission_request"], Field(description="Action name. Always 'call_permission_request'.")
    ]


class CallPermissionRequestInteractive(BaseModel):
    """Interactive object for call permission request messages (interactive.type = 'call_permission_request')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[
        Literal["call_permission_request"],
        Field(description="Interactive sub-type discriminator."),
    ] = "call_permission_request"
    body: Annotated[InteractiveBody, Field(description="Body text for the call permission request.")]
    action: Annotated[CallPermissionRequestAction, Field(description="Action for the call permission request.")]


class ProductSection(BaseModel):
    """A section containing product items for product list messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    title: Annotated[str | None, Field(description="Section title.", max_length=24)] = None
    product_items: Annotated[
        Sequence[dict[str, str]],
        Field(min_length=1, max_length=30, description="List of products. Each item needs 'product_retailer_id'."),
    ]


class ProductAction(BaseModel):
    """Action payload for single product messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    catalog_id: Annotated[str, Field(description="ID of the WhatsApp catalog.")]
    product_retailer_id: Annotated[str, Field(description="Retailer-defined product ID.")]


class ProductInteractive(BaseModel):
    """Interactive object for single product messages (interactive.type = 'product')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["product"], Field(description="Interactive sub-type discriminator.")] = "product"
    body: Annotated[InteractiveBody | None, Field(description="Optional body text.")] = None
    action: Annotated[ProductAction, Field(description="Action with catalog and product IDs.")]
    header: Annotated[InteractiveHeader | None, Field(description="Optional message header.")] = None
    footer: Annotated[InteractiveFooter | None, Field(description="Optional message footer.")] = None


class ProductListAction(BaseModel):
    """Action payload for product list messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    catalog_id: Annotated[str, Field(description="ID of the WhatsApp catalog.")]
    sections: Annotated[
        Sequence[ProductSection],
        Field(min_length=1, max_length=10, description="List of product sections."),
    ]


class ProductListInteractive(BaseModel):
    """Interactive object for product list messages (interactive.type = 'product_list')."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[Literal["product_list"], Field(description="Interactive sub-type discriminator.")] = "product_list"
    body: Annotated[InteractiveBody, Field(description="Body text of the message.")]
    action: Annotated[ProductListAction, Field(description="Action with catalog and product sections.")]
    header: Annotated[InteractiveHeader, Field(description="Required header for product list messages.")]
    footer: Annotated[InteractiveFooter | None, Field(description="Optional message footer.")] = None


InteractiveObject = Annotated[
    ReplyButtonsInteractive
    | ListInteractive
    | CtaUrlInteractive
    | FlowInteractive
    | LocationRequestInteractive
    | CallPermissionRequestInteractive
    | ProductInteractive
    | ProductListInteractive,
    Field(discriminator="type"),
]
"""Discriminated union of all interactive sub-types, resolved by interactive.type."""


class InteractiveMessage(MessageBase):
    """Outgoing WhatsApp interactive message. The concrete sub-type is resolved via interactive.type."""

    type: Annotated[
        Literal[MessageType.interactive],
        Field(description="Message type discriminator."),
    ] = MessageType.interactive
    interactive: Annotated[
        InteractiveObject,
        Field(description="Interactive payload, discriminated by its own type field."),
    ]
