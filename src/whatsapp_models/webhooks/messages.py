"""Incoming message models received via WhatsApp webhook.

doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages
"""

from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.contacts import Address, ContactName, EmailEntry, PhoneEntry, UrlEntry


class InteractiveReplyType(StrEnum):
    """Interactive reply sub-type for incoming interactive messages."""

    button_reply = "button_reply"
    list_reply = "list_reply"


class IncomingContext(BaseModel):
    """Context object present when the incoming message quotes a previous message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    from_: Annotated[str | None, Field(alias="from", description="Phone number of the original message sender.")] = None
    id: Annotated[str, Field(description="Message ID of the quoted message.")]


class IncomingMessageBase(BaseModel):
    """Fields common to every incoming WhatsApp message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, populate_by_name=True)

    from_: Annotated[str, Field(alias="from", description="Sender's WhatsApp phone number.")]
    id: Annotated[str, Field(description="WhatsApp message ID (wamid).")]
    timestamp: Annotated[str, Field(description="Unix timestamp of the message as a string.")]
    context: Annotated[
        IncomingContext | None,
        Field(description="Context of a quoted/replied message, when present."),
    ] = None


class GroupMixin(BaseModel):
    """Mixin that marks a message as originating from a WhatsApp group.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/group
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, populate_by_name=True)

    group_id: Annotated[str, Field(description="ID of the WhatsApp group the message was sent in.")]


# ---------------------------------------------------------------------------
# Payload objects
# ---------------------------------------------------------------------------


class IncomingTextObject(BaseModel):
    """Text content of an incoming text message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    body: Annotated[str, Field(description="Text body of the message.")]


class IncomingAudioObject(BaseModel):
    """Audio media reference for an incoming audio message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Media asset ID assigned by WhatsApp.")]
    mime_type: Annotated[str, Field(description="MIME type of the audio file.")]
    sha256: Annotated[str, Field(description="SHA-256 hash of the audio file.")]
    voice: Annotated[bool, Field(description="Whether this audio was recorded as a voice message.")]


class IncomingImageObject(BaseModel):
    """Image media reference for an incoming image message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Media asset ID assigned by WhatsApp.")]
    mime_type: Annotated[str, Field(description="MIME type of the image file.")]
    sha256: Annotated[str, Field(description="SHA-256 hash of the image file.")]
    caption: Annotated[str | None, Field(description="Caption attached to the image, if any.")] = None


class IncomingVideoObject(BaseModel):
    """Video media reference for an incoming video message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Media asset ID assigned by WhatsApp.")]
    mime_type: Annotated[str, Field(description="MIME type of the video file.")]
    sha256: Annotated[str, Field(description="SHA-256 hash of the video file.")]
    caption: Annotated[str | None, Field(description="Caption attached to the video, if any.")] = None


class IncomingDocumentObject(BaseModel):
    """Document media reference for an incoming document message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Media asset ID assigned by WhatsApp.")]
    mime_type: Annotated[str, Field(description="MIME type of the document file.")]
    sha256: Annotated[str, Field(description="SHA-256 hash of the document file.")]
    filename: Annotated[str, Field(description="Original filename of the document.")]


class IncomingStickerObject(BaseModel):
    """Sticker media reference for an incoming sticker message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Media asset ID assigned by WhatsApp.")]
    mime_type: Annotated[str, Field(description="MIME type of the sticker file.")]
    sha256: Annotated[str, Field(description="SHA-256 hash of the sticker file.")]
    animated: Annotated[bool, Field(description="Whether the sticker is animated.")]


class IncomingLocationObject(BaseModel):
    """Location payload of an incoming location message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    latitude: Annotated[float, Field(description="Latitude of the shared location.")]
    longitude: Annotated[float, Field(description="Longitude of the shared location.")]
    name: Annotated[str, Field(description="Name of the location.")]
    address: Annotated[str, Field(description="Address of the location.")]
    url: Annotated[str | None, Field(description="URL associated with the location, if any.")] = None


class IncomingReactionObject(BaseModel):
    """Reaction payload of an incoming reaction message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    message_id: Annotated[str, Field(description="ID of the message that was reacted to.")]
    emoji: Annotated[str, Field(description="Emoji used as reaction.")]


class IncomingContactEntry(BaseModel):
    """A single contact entry inside an incoming contacts message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[ContactName | None, Field(description="Name information of the contact.")] = None
    addresses: Annotated[Sequence[Address], Field(description="List of physical addresses.")] = []
    birthday: Annotated[str | None, Field(description="Birthday in YYYY-MM-DD format.")] = None
    emails: Annotated[Sequence[EmailEntry], Field(description="List of email addresses.")] = []
    org: Annotated[dict[str, str] | None, Field(description="Organization info.")] = None
    phones: Annotated[Sequence[PhoneEntry], Field(description="List of phone numbers.")] = []
    urls: Annotated[Sequence[UrlEntry], Field(description="List of URLs.")] = []


class ButtonReply(BaseModel):
    """Button reply payload inside an incoming interactive message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Button ID from the original message.")]
    title: Annotated[str, Field(description="Button title from the original message.")]


class ListReply(BaseModel):
    """List reply payload inside an incoming interactive message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, Field(description="Row ID selected by the user.")]
    title: Annotated[str, Field(description="Row title selected by the user.")]
    description: Annotated[str | None, Field(description="Row description, if any.")] = None


class IncomingInteractivePayload(BaseModel):
    """Payload of an incoming interactive reply (button or list)."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    type: Annotated[InteractiveReplyType, Field(description="Interactive reply type.")]
    button_reply: Annotated[
        ButtonReply | None, Field(description="Button reply data, present when type is 'button_reply'.")
    ] = None
    list_reply: Annotated[
        ListReply | None, Field(description="List reply data, present when type is 'list_reply'.")
    ] = None


class IncomingButtonObject(BaseModel):
    """Quick reply button payload from a template message response."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    text: Annotated[str, Field(description="Button text shown to the user.")]
    payload: Annotated[str, Field(description="Payload string set in the template button.")]


class IncomingErrorData(BaseModel):
    """Details object nested inside an incoming error entry."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    details: Annotated[str, Field(description="Human-readable error detail string.")]


class IncomingError(BaseModel):
    """Error entry present in unsupported/unknown message payloads."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    code: Annotated[int, Field(description="Error code.")]
    title: Annotated[str, Field(description="Short error title.")]
    message: Annotated[str, Field(description="Detailed error message.")]
    error_data: Annotated[IncomingErrorData, Field(description="Additional error details.")]
    href: Annotated[str | None, Field(description="Link to error documentation.")] = None


class ReferralWelcomeMessage(BaseModel):
    """Welcome message attached to a referral (click-to-WhatsApp ad)."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    text: Annotated[str, Field(description="Welcome message text pre-filled from the ad.")]


class ReferralObject(BaseModel):
    """Referral context present when the message originated from a click-to-WhatsApp ad."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    source_url: Annotated[str, Field(description="URL of the ad or post that triggered the message.")]
    source_id: Annotated[str, Field(description="ID of the ad or post.")]
    source_type: Annotated[Literal["ad", "post"], Field(description="Type of the referral source.")]
    body: Annotated[str, Field(description="Body text of the ad.")]
    headline: Annotated[str, Field(description="Headline of the ad.")]
    media_type: Annotated[Literal["image", "video"], Field(description="Media type featured in the ad.")]
    ctwa_clid: Annotated[str, Field(description="Click-to-WhatsApp click ID for analytics.")]
    image_url: Annotated[str | None, Field(description="URL of the ad image, if media_type is 'image'.")] = None
    video_url: Annotated[str | None, Field(description="URL of the ad video, if media_type is 'video'.")] = None
    thumbnail_url: Annotated[str | None, Field(description="Thumbnail URL of the ad media.")] = None
    welcome_message: Annotated[
        ReferralWelcomeMessage | None, Field(description="Pre-filled welcome message from the ad.")
    ] = None


class OrderProductItem(BaseModel):
    """A single product line inside an incoming order message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    product_retailer_id: Annotated[str, Field(description="Retailer-defined product ID.")]
    quantity: Annotated[int, Field(description="Quantity ordered.")]
    item_price: Annotated[float, Field(description="Unit price of the item.")]
    currency: Annotated[str, Field(description="ISO 4217 currency code.")]


class OrderObject(BaseModel):
    """Order payload of an incoming order message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    catalog_id: Annotated[str, Field(description="ID of the WhatsApp catalog.")]
    text: Annotated[str, Field(description="Optional note from the buyer.")]
    product_items: Annotated[Sequence[OrderProductItem], Field(description="List of ordered products.")]


class SystemObject(BaseModel):
    """System event payload for number-change notifications."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    body: Annotated[str, Field(description="Human-readable description of the system event.")]
    wa_id: Annotated[str | None, Field(description="New WhatsApp ID after a number change.")] = None
    type: Annotated[Literal["user_changed_number"], Field(description="System event type.")]


# ---------------------------------------------------------------------------
# Direct (non-group) message types
# ---------------------------------------------------------------------------


class IncomingTextMessage(IncomingMessageBase):
    """Incoming text message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/text
    """

    type: Annotated[Literal[MessageType.text], Field(description="Message type discriminator.")] = MessageType.text
    text: Annotated[IncomingTextObject, Field(description="Text content.")]
    referral: Annotated[
        ReferralObject | None, Field(description="Referral context when the message originated from an ad.")
    ] = None


class IncomingAudioMessage(IncomingMessageBase):
    """Incoming audio message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/audio
    """

    type: Annotated[Literal[MessageType.audio], Field(description="Message type discriminator.")] = MessageType.audio
    audio: Annotated[IncomingAudioObject, Field(description="Audio media reference.")]


class IncomingImageMessage(IncomingMessageBase):
    """Incoming image message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/image
    """

    type: Annotated[Literal[MessageType.image], Field(description="Message type discriminator.")] = MessageType.image
    image: Annotated[IncomingImageObject, Field(description="Image media reference.")]


class IncomingVideoMessage(IncomingMessageBase):
    """Incoming video message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/video
    """

    type: Annotated[Literal[MessageType.video], Field(description="Message type discriminator.")] = MessageType.video
    video: Annotated[IncomingVideoObject, Field(description="Video media reference.")]


class IncomingDocumentMessage(IncomingMessageBase):
    """Incoming document message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/document
    """

    type: Annotated[Literal[MessageType.document], Field(description="Message type discriminator.")] = (
        MessageType.document
    )
    document: Annotated[IncomingDocumentObject, Field(description="Document media reference.")]


class IncomingStickerMessage(IncomingMessageBase):
    """Incoming sticker message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/sticker
    """

    type: Annotated[Literal[MessageType.sticker], Field(description="Message type discriminator.")] = (
        MessageType.sticker
    )
    sticker: Annotated[IncomingStickerObject, Field(description="Sticker media reference.")]


class IncomingLocationMessage(IncomingMessageBase):
    """Incoming location message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/location
    """

    type: Annotated[Literal[MessageType.location], Field(description="Message type discriminator.")] = (
        MessageType.location
    )
    location: Annotated[IncomingLocationObject, Field(description="Location payload.")]


class IncomingReactionMessage(IncomingMessageBase):
    """Incoming reaction message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/reaction
    """

    type: Annotated[Literal[MessageType.reaction], Field(description="Message type discriminator.")] = (
        MessageType.reaction
    )
    reaction: Annotated[IncomingReactionObject, Field(description="Reaction payload.")]


class IncomingContactsMessage(IncomingMessageBase):
    """Incoming contacts message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/contacts
    """

    type: Annotated[Literal[MessageType.contacts], Field(description="Message type discriminator.")] = (
        MessageType.contacts
    )
    contacts: Annotated[Sequence[IncomingContactEntry], Field(min_length=1, description="List of shared contacts.")]


class IncomingInteractiveMessage(IncomingMessageBase):
    """Incoming interactive reply message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/interactive
    """

    type: Annotated[Literal[MessageType.interactive], Field(description="Message type discriminator.")] = (
        MessageType.interactive
    )
    interactive: Annotated[IncomingInteractivePayload, Field(description="Interactive reply payload.")]


class IncomingButtonMessage(IncomingMessageBase):
    """Incoming button reply to a template message received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/button
    """

    type: Annotated[Literal[MessageType.button], Field(description="Message type discriminator.")] = MessageType.button
    button: Annotated[IncomingButtonObject, Field(description="Button reply payload.")]
    context: Annotated[IncomingContext, Field(description="Context referencing the original template message.")]


class IncomingUnsupportedMessage(IncomingMessageBase):
    """Unsupported message type received via webhook.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/unsupported
    """

    type: Annotated[Literal[MessageType.unsupported], Field(description="Message type discriminator.")] = (
        MessageType.unsupported
    )
    errors: Annotated[Sequence[IncomingError], Field(description="Errors explaining why the message is unsupported.")]


class IncomingUnknownMessage(IncomingMessageBase):
    """Unknown message type received via webhook (variant of unsupported).

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/unsupported
    """

    type: Annotated[Literal[MessageType.unknown], Field(description="Message type discriminator.")] = (
        MessageType.unknown
    )
    errors: Annotated[Sequence[IncomingError], Field(description="Errors explaining why the message is unknown.")]


class IncomingOrderMessage(IncomingMessageBase):
    """Incoming order message from a WhatsApp catalog interaction.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages
    """

    type: Annotated[Literal[MessageType.order], Field(description="Message type discriminator.")] = MessageType.order
    order: Annotated[OrderObject, Field(description="Order payload with product items.")]


class IncomingSystemMessage(IncomingMessageBase):
    """Incoming system notification, e.g. user changed their phone number.

    doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages
    """

    type: Annotated[Literal[MessageType.system], Field(description="Message type discriminator.")] = MessageType.system
    system: Annotated[SystemObject, Field(description="System event payload.")]


# ---------------------------------------------------------------------------
# Group message types (GroupMixin + typed message base)
# doc: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/group
# ---------------------------------------------------------------------------


class IncomingGroupTextMessage(GroupMixin, IncomingMessageBase):
    """Incoming text message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.text], Field(description="Message type discriminator.")] = MessageType.text
    text: Annotated[IncomingTextObject, Field(description="Text content.")]


class IncomingGroupAudioMessage(GroupMixin, IncomingMessageBase):
    """Incoming audio message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.audio], Field(description="Message type discriminator.")] = MessageType.audio
    audio: Annotated[IncomingAudioObject, Field(description="Audio media reference.")]


class IncomingGroupImageMessage(GroupMixin, IncomingMessageBase):
    """Incoming image message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.image], Field(description="Message type discriminator.")] = MessageType.image
    image: Annotated[IncomingImageObject, Field(description="Image media reference.")]


class IncomingGroupVideoMessage(GroupMixin, IncomingMessageBase):
    """Incoming video message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.video], Field(description="Message type discriminator.")] = MessageType.video
    video: Annotated[IncomingVideoObject, Field(description="Video media reference.")]


class IncomingGroupDocumentMessage(GroupMixin, IncomingMessageBase):
    """Incoming document message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.document], Field(description="Message type discriminator.")] = (
        MessageType.document
    )
    document: Annotated[IncomingDocumentObject, Field(description="Document media reference.")]


class IncomingGroupStickerMessage(GroupMixin, IncomingMessageBase):
    """Incoming sticker message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.sticker], Field(description="Message type discriminator.")] = (
        MessageType.sticker
    )
    sticker: Annotated[IncomingStickerObject, Field(description="Sticker media reference.")]


class IncomingGroupLocationMessage(GroupMixin, IncomingMessageBase):
    """Incoming location message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.location], Field(description="Message type discriminator.")] = (
        MessageType.location
    )
    location: Annotated[IncomingLocationObject, Field(description="Location payload.")]


class IncomingGroupReactionMessage(GroupMixin, IncomingMessageBase):
    """Incoming reaction message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.reaction], Field(description="Message type discriminator.")] = (
        MessageType.reaction
    )
    reaction: Annotated[IncomingReactionObject, Field(description="Reaction payload.")]


class IncomingGroupInteractiveMessage(GroupMixin, IncomingMessageBase):
    """Incoming interactive reply message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.interactive], Field(description="Message type discriminator.")] = (
        MessageType.interactive
    )
    interactive: Annotated[IncomingInteractivePayload, Field(description="Interactive reply payload.")]


class IncomingGroupOrderMessage(GroupMixin, IncomingMessageBase):
    """Incoming order message received inside a WhatsApp group."""

    type: Annotated[Literal[MessageType.order], Field(description="Message type discriminator.")] = MessageType.order
    order: Annotated[OrderObject, Field(description="Order payload with product items.")]


# ---------------------------------------------------------------------------
# Discriminated unions
# ---------------------------------------------------------------------------

IncomingMessage = Annotated[
    IncomingTextMessage
    | IncomingAudioMessage
    | IncomingImageMessage
    | IncomingVideoMessage
    | IncomingDocumentMessage
    | IncomingStickerMessage
    | IncomingLocationMessage
    | IncomingContactsMessage
    | IncomingReactionMessage
    | IncomingInteractiveMessage
    | IncomingButtonMessage
    | IncomingOrderMessage
    | IncomingSystemMessage
    | IncomingUnsupportedMessage
    | IncomingUnknownMessage,
    Field(discriminator="type"),
]

IncomingGroupMessage = Annotated[
    IncomingGroupTextMessage
    | IncomingGroupAudioMessage
    | IncomingGroupImageMessage
    | IncomingGroupVideoMessage
    | IncomingGroupDocumentMessage
    | IncomingGroupStickerMessage
    | IncomingGroupLocationMessage
    | IncomingGroupReactionMessage
    | IncomingGroupInteractiveMessage
    | IncomingGroupOrderMessage,
    Field(discriminator="type"),
]
