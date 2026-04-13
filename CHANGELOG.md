# Changelog

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
