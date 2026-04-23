# Changelog

## v0.2.5

### Added

- All previously unexported public models and enums are now accessible from the top-level `whatsapp_models` package and their respective sub-package `__init__.py` files
- Common enums (`AddressType`, `Currency`, `EmailType`, `Language`, `MessageType`, `PhoneType`, `UrlType`) exported from top-level
- All interactive sub-types (`InteractiveBody`, `InteractiveHeader`, `InteractiveFooter`, `ReplyButton`, `ReplyButtonsAction`, `ListRow`, `ListSection`, `ListAction`, `CtaUrlParameters`, `CtaUrlAction`, `FlowParameters`, `FlowAction`, `LocationRequestAction`, `CallPermissionRequestAction`, `CallPermissionRequestInteractive`, `ProductSection`, `ProductAction`, `ProductInteractive`, `ProductListAction`, `ProductListInteractive`)
- Outgoing media hierarchy (`OutgoingMediaObject`, `CaptionedMediaObject`, `DocumentObject`) exported; `messages/media.py::MediaObject` renamed to `OutgoingMediaObject` to distinguish from `media/media.py::MediaObject`
- Template parameter and component types (`TemplateParameter`, `TemplateSendComponent`, `DocumentParameter`, `ImageParameter`, `VideoParameter`, `TextParameter`, `CurrencyParameter`, `CurrencyObject`, `DateTimeParameter`, `DateTimeObject`, `ButtonParameter`, `ButtonPayloadParameter`, `ButtonTextParameter`)
- All incoming webhook payload types (`IncomingMediaObject`, `IncomingAudioObject`, `IncomingImageObject`, `IncomingVideoObject`, `IncomingDocumentObject`, `IncomingStickerObject`, `IncomingLocationObject`, `IncomingReactionObject`, `IncomingContactEntry`, `IncomingTextObject`, `IncomingMessageBase`, `IncomingContext`, `InteractiveReplyType`, `ButtonReply`, `ListReply`, `IncomingInteractivePayload`, `IncomingButtonObject`, `IncomingErrorData`, `IncomingError`, `ReferralWelcomeMessage`, `ReferralObject`, `OrderProductItem`, `OrderObject`, `SystemObject`)
- Additional webhook message types (`IncomingOrderMessage`, `IncomingSystemMessage`, `IncomingUnknownMessage`) and group message variants (`GroupMixin`, `IncomingGroupTextMessage`, `IncomingGroupAudioMessage`, `IncomingGroupImageMessage`, `IncomingGroupVideoMessage`, `IncomingGroupDocumentMessage`, `IncomingGroupStickerMessage`, `IncomingGroupLocationMessage`, `IncomingGroupReactionMessage`, `IncomingGroupInteractiveMessage`)
- Status sub-models (`ConversationOrigin`, `Conversation`, `Pricing`) and notification sub-models (`ChangeField`, `GroupParticipant`, `GroupEventType`, `GroupEvent`, `NotificationContactProfile`, `NotificationContact`)
- `MessageContext` (outgoing reply context) and `MessageContext` exported from `messages` package

### Fixed

- `TemplateSendComponent.index` type corrected from `str | None` to `int | None`

## v0.2.4

### Added

- `IncomingMediaObject` — base class for incoming media payload objects with shared fields `id`, `mime_type`, `sha256`, and `url`
- `url` required field on `IncomingAudioObject`, `IncomingImageObject`, `IncomingVideoObject`, `IncomingDocumentObject`, `IncomingStickerObject`

## v0.2.3

### Added

- `NotificationContactProfile` — model for the `profile` field inside a webhook contact entry (`name: str`)
- `NotificationContact` — typed model for entries in `Value.contacts` (`wa_id`, `user_id`, `profile`), replacing `dict[str, Any]`

## v0.2.2

### Changed

- Replace `list[...]` with `Sequence[...]` on all Pydantic model fields for covariance and immutability

## v0.2.1

### Added

- `parameter_name` optional field on all template send parameter types (`TextParameter`, `CurrencyParameter`, `DateTimeParameter`, `DocumentParameter`, `ImageParameter`, `VideoParameter`) — supports named-variable templates as documented by the WhatsApp Business API

## v0.2.0

### Added

- `AudioMediaObject` — subclass of `MediaObject` with `voice: bool = False` for sending WhatsApp PTT (push-to-talk) voice messages
- `ButtonType.VOICE_CALL` — new template button type for voice call actions
- `MessageStatusUpdate` — model for marking an incoming message as read (`status: "read"`)
- `TypingIndicatorContent` — optional typing indicator payload to include with a read receipt

## v0.1.0 — Initial Release

First public release of `whatsapp-models`, a fully-typed Pydantic v2 library for the WhatsApp Business API (v23.0).

### Outgoing messages (`whatsapp_models.messages`)

- **Text** — plain text messages
- **Media** — audio, image, video, document, sticker (with `id` or `link`)
- **Location** — latitude/longitude with name and address
- **Reaction** — emoji reactions to existing messages
- **Contacts** — vCard-style contact sharing
- **Interactive** — reply buttons, list, CTA URL, flow, location request, call permission request, single product, product list
- **Template** — parameterised template messages with typed parameter union (`text`, `currency`, `date_time`, `document`, `image`, `video`) and button parameters (`payload`, `text`)
- `OutgoingMessage` — discriminated union of all outgoing types

### Incoming webhooks (`whatsapp_models.webhooks`)

- **Messages** — text, audio, image, video, document, sticker, location, reaction, contacts, interactive (button reply / list reply), button, order, system, unsupported, unknown
- **Group messages** — all direct message types extended with `group_id` via `GroupMixin`
- **Statuses** — delivery status updates with `Conversation` and `Pricing` metadata
- **Notification envelope** — `WebhookNotification → Entry → Change → Value` with group lifecycle events (`GroupEvent`)
- **Errors** — `WebhookError` with optional `href` documentation link

### Template management (`whatsapp_models.message_templates`)

- `CreateTemplateRequest` / `TemplateResponse` — create and inspect templates
- Components — `HeaderComponent`, `BodyComponent`, `FooterComponent`, `ButtonsComponent`
- Buttons — `QuickReplyButton`, `UrlButton`, `PhoneNumberButton`, `OtpButton`

### Phone numbers (`whatsapp_models.phone_numbers`)

- `PhoneNumber` with `QualityRating`, `ThroughputLevel`, `MessagingLimitTier`

### Media upload (`whatsapp_models.media`)

- `MediaObject` / `MediaUploadResponse`
