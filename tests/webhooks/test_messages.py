"""Tests for incoming webhook message models and IncomingMessage discriminated union."""

import pytest
from pydantic import TypeAdapter, ValidationError

from whatsapp_models.common.enums import MessageType
from whatsapp_models.webhooks.messages import (
    GroupMixin,
    IncomingAudioMessage,
    IncomingButtonMessage,
    IncomingContactsMessage,
    IncomingDocumentMessage,
    IncomingGroupAudioMessage,
    IncomingGroupDocumentMessage,
    IncomingGroupImageMessage,
    IncomingGroupInteractiveMessage,
    IncomingGroupLocationMessage,
    IncomingGroupMessage,
    IncomingGroupReactionMessage,
    IncomingGroupStickerMessage,
    IncomingGroupTextMessage,
    IncomingGroupVideoMessage,
    IncomingImageMessage,
    IncomingInteractiveMessage,
    IncomingLocationMessage,
    IncomingMessage,
    IncomingReactionMessage,
    IncomingStickerMessage,
    IncomingTextMessage,
    IncomingUnsupportedMessage,
    IncomingVideoMessage,
)

FROM = "5511999999999"
GROUP_ID = "120363000000000001@g.us"
BASE = {"from_": FROM, "id": "wamid.abc123", "timestamp": "1700000000"}
GROUP_BASE = {**BASE, "group_id": GROUP_ID}


class TestIncomingTextMessage:
    def test_basic(self):
        """IncomingTextMessage stores from_, id, timestamp and text body."""
        msg = IncomingTextMessage(**BASE, text={"body": "Olá!"})
        assert msg.type == MessageType.text
        assert msg.from_ == FROM
        assert msg.text.body == "Olá!"

    def test_requires_body(self):
        """IncomingTextMessage raises ValidationError when text body is missing."""
        with pytest.raises(ValidationError):
            IncomingTextMessage(**BASE, text={})

    def test_serialization_uses_from_alias(self):
        """IncomingTextMessage serializes from_ as 'from'."""
        msg = IncomingTextMessage(**BASE, text={"body": "hi"})
        data = msg.model_dump(by_alias=True)
        assert "from" in data
        assert data["from"] == FROM


class TestIncomingAudioMessage:
    def test_basic(self):
        """IncomingAudioMessage stores media id, mime_type, sha256 and voice."""
        msg = IncomingAudioMessage(
            **BASE,
            audio={
                "id": "media_id_1",
                "mime_type": "audio/ogg; codecs=opus",
                "sha256": "abc123",
                "url": "https://example.com/audio",
                "voice": False,
            },
        )
        assert msg.type == MessageType.audio
        assert msg.audio.id == "media_id_1"

    def test_requires_id(self):
        """IncomingAudioMessage raises ValidationError when audio id is missing."""
        with pytest.raises(ValidationError):
            IncomingAudioMessage(**BASE, audio={})


class TestIncomingImageMessage:
    def test_basic(self):
        """IncomingImageMessage stores media id, mime_type and sha256."""
        msg = IncomingImageMessage(
            **BASE,
            image={"id": "img_id", "mime_type": "image/jpeg", "sha256": "abc123", "url": "https://example.com/image"},
        )
        assert msg.type == MessageType.image
        assert msg.image.id == "img_id"

    def test_caption_optional(self):
        """IncomingImageMessage.image.caption is optional."""
        msg = IncomingImageMessage(
            **BASE,
            image={"id": "img_id", "mime_type": "image/jpeg", "sha256": "abc123", "url": "https://example.com/image"},
        )
        assert msg.image.caption is None

    def test_with_caption(self):
        """IncomingImageMessage stores optional caption."""
        msg = IncomingImageMessage(
            **BASE,
            image={
                "id": "img_id",
                "mime_type": "image/jpeg",
                "sha256": "abc123",
                "url": "https://example.com/image",
                "caption": "foto",
            },
        )
        assert msg.image.caption == "foto"


class TestIncomingVideoMessage:
    def test_basic(self):
        """IncomingVideoMessage stores media id, mime_type and sha256."""
        msg = IncomingVideoMessage(
            **BASE,
            video={"id": "vid_id", "mime_type": "video/mp4", "sha256": "abc123", "url": "https://example.com/video"},
        )
        assert msg.type == MessageType.video
        assert msg.video.id == "vid_id"


class TestIncomingDocumentMessage:
    def test_basic(self):
        """IncomingDocumentMessage stores media id, mime_type, sha256 and filename."""
        msg = IncomingDocumentMessage(
            **BASE,
            document={
                "id": "doc_id",
                "mime_type": "application/pdf",
                "sha256": "abc123",
                "url": "https://example.com/doc",
                "filename": "relatorio.pdf",
            },
        )
        assert msg.type == MessageType.document
        assert msg.document.filename == "relatorio.pdf"

    def test_requires_filename(self):
        """IncomingDocumentMessage raises ValidationError when filename is missing."""
        with pytest.raises(ValidationError):
            IncomingDocumentMessage(**BASE, document={"id": "doc_id", "mime_type": "application/pdf", "sha256": "x"})


class TestIncomingStickerMessage:
    def test_basic(self):
        """IncomingStickerMessage stores media id, mime_type, sha256 and animated."""
        msg = IncomingStickerMessage(
            **BASE,
            sticker={
                "id": "stk_id",
                "mime_type": "image/webp",
                "sha256": "abc123",
                "url": "https://example.com/sticker",
                "animated": False,
            },
        )
        assert msg.type == MessageType.sticker
        assert msg.sticker.id == "stk_id"

    def test_requires_animated(self):
        """IncomingStickerMessage raises ValidationError when animated is missing."""
        with pytest.raises(ValidationError):
            IncomingStickerMessage(**BASE, sticker={"id": "stk_id", "mime_type": "image/webp", "sha256": "x"})


class TestIncomingLocationMessage:
    def test_basic(self):
        """IncomingLocationMessage stores latitude, longitude, name and address."""
        msg = IncomingLocationMessage(
            **BASE,
            location={"latitude": -23.5505, "longitude": -46.6333, "name": "SP", "address": "Centro"},
        )
        assert msg.type == MessageType.location
        assert msg.location.latitude == -23.5505

    def test_requires_name_and_address(self):
        """IncomingLocationMessage raises ValidationError when name or address is missing."""
        with pytest.raises(ValidationError):
            IncomingLocationMessage(**BASE, location={"latitude": 0.0, "longitude": 0.0})

    def test_requires_lat_lng(self):
        """IncomingLocationMessage raises ValidationError when coordinates are missing."""
        with pytest.raises(ValidationError):
            IncomingLocationMessage(**BASE, location={})


class TestIncomingReactionMessage:
    def test_basic(self):
        """IncomingReactionMessage stores message_id and emoji."""
        msg = IncomingReactionMessage(**BASE, reaction={"message_id": "wamid.orig", "emoji": "👍"})
        assert msg.type == MessageType.reaction
        assert msg.reaction.emoji == "👍"

    def test_requires_message_id_and_emoji(self):
        """IncomingReactionMessage raises ValidationError when emoji is missing."""
        with pytest.raises(ValidationError):
            IncomingReactionMessage(**BASE, reaction={"message_id": "wamid.orig"})


class TestIncomingContactsMessage:
    def test_basic(self):
        """IncomingContactsMessage stores a list of contacts."""
        msg = IncomingContactsMessage(
            **BASE,
            contacts=[{"name": {"formatted_name": "João"}}],
        )
        assert msg.type == MessageType.contacts
        assert msg.contacts[0].name.formatted_name == "João"

    def test_requires_contacts(self):
        """IncomingContactsMessage raises ValidationError when contacts list is empty."""
        with pytest.raises(ValidationError):
            IncomingContactsMessage(**BASE, contacts=[])


class TestIncomingInteractiveMessage:
    def test_button_reply(self):
        """IncomingInteractiveMessage with button_reply stores button id and title."""
        msg = IncomingInteractiveMessage(
            **BASE,
            interactive={"type": "button_reply", "button_reply": {"id": "btn1", "title": "Sim"}},
        )
        assert msg.type == MessageType.interactive
        assert msg.interactive.button_reply.id == "btn1"

    def test_list_reply(self):
        """IncomingInteractiveMessage with list_reply stores row id, title and description."""
        msg = IncomingInteractiveMessage(
            **BASE,
            interactive={
                "type": "list_reply",
                "list_reply": {"id": "row1", "title": "Item 1", "description": "Desc"},
            },
        )
        assert msg.interactive.list_reply.id == "row1"


class TestIncomingButtonMessage:
    def test_basic(self):
        """IncomingButtonMessage stores text, payload and required context."""
        msg = IncomingButtonMessage(
            **BASE,
            context={"id": "wamid.orig"},
            button={"text": "Confirmar", "payload": "confirm_payload"},
        )
        assert msg.type == MessageType.button
        assert msg.button.text == "Confirmar"
        assert msg.button.payload == "confirm_payload"
        assert msg.context.id == "wamid.orig"


class TestIncomingUnsupportedMessage:
    def test_basic(self):
        """IncomingUnsupportedMessage has type 'unsupported' with required errors list."""
        msg = IncomingUnsupportedMessage(
            **BASE,
            errors=[{"code": 131051, "title": "Unsupported", "message": "msg", "error_data": {"details": "d"}}],
        )
        assert msg.type == MessageType.unsupported
        assert len(msg.errors) == 1


class TestGroupMixin:
    def test_group_text_message_has_group_id(self):
        """IncomingGroupTextMessage carries group_id from GroupMixin."""
        msg = IncomingGroupTextMessage(**GROUP_BASE, text={"body": "oi grupo"})
        assert isinstance(msg, GroupMixin)
        assert msg.group_id == GROUP_ID

    def test_requires_group_id(self):
        """IncomingGroupTextMessage raises ValidationError when group_id is missing."""
        with pytest.raises(ValidationError):
            IncomingGroupTextMessage(**BASE, text={"body": "oi"})


class TestIncomingGroupMessages:
    def test_group_text(self):
        """IncomingGroupTextMessage stores type text and text body."""
        msg = IncomingGroupTextMessage(**GROUP_BASE, text={"body": "mensagem no grupo"})
        assert msg.type == MessageType.text
        assert msg.text.body == "mensagem no grupo"
        assert msg.group_id == GROUP_ID

    def test_group_audio(self):
        """IncomingGroupAudioMessage stores type audio and media id."""
        msg = IncomingGroupAudioMessage(
            **GROUP_BASE,
            audio={"id": "m1", "mime_type": "audio/ogg", "sha256": "x", "url": "https://example.com/a", "voice": False},
        )
        assert msg.type == MessageType.audio
        assert msg.audio.id == "m1"

    def test_group_image(self):
        """IncomingGroupImageMessage stores type image and media id."""
        msg = IncomingGroupImageMessage(
            **GROUP_BASE, image={"id": "m2", "mime_type": "image/jpeg", "sha256": "x", "url": "https://example.com/i"}
        )
        assert msg.type == MessageType.image

    def test_group_video(self):
        """IncomingGroupVideoMessage stores type video and media id."""
        msg = IncomingGroupVideoMessage(
            **GROUP_BASE, video={"id": "m3", "mime_type": "video/mp4", "sha256": "x", "url": "https://example.com/v"}
        )
        assert msg.type == MessageType.video

    def test_group_document(self):
        """IncomingGroupDocumentMessage stores type document and filename."""
        msg = IncomingGroupDocumentMessage(
            **GROUP_BASE,
            document={
                "id": "m4",
                "mime_type": "application/pdf",
                "sha256": "x",
                "url": "https://example.com/d",
                "filename": "f.pdf",
            },
        )
        assert msg.type == MessageType.document
        assert msg.document.filename == "f.pdf"

    def test_group_sticker(self):
        """IncomingGroupStickerMessage stores type sticker and media id."""
        msg = IncomingGroupStickerMessage(
            **GROUP_BASE,
            sticker={
                "id": "m5",
                "mime_type": "image/webp",
                "sha256": "x",
                "url": "https://example.com/s",
                "animated": False,
            },
        )
        assert msg.type == MessageType.sticker

    def test_group_location(self):
        """IncomingGroupLocationMessage stores type location and coordinates."""
        msg = IncomingGroupLocationMessage(
            **GROUP_BASE, location={"latitude": -23.5, "longitude": -46.6, "name": "SP", "address": "Centro"}
        )
        assert msg.type == MessageType.location
        assert msg.location.latitude == -23.5

    def test_group_reaction(self):
        """IncomingGroupReactionMessage stores type reaction and emoji."""
        msg = IncomingGroupReactionMessage(**GROUP_BASE, reaction={"message_id": "wamid.x", "emoji": "🔥"})
        assert msg.type == MessageType.reaction
        assert msg.reaction.emoji == "🔥"

    def test_group_interactive(self):
        """IncomingGroupInteractiveMessage stores type interactive and button reply."""
        msg = IncomingGroupInteractiveMessage(
            **GROUP_BASE,
            interactive={"type": "button_reply", "button_reply": {"id": "b1", "title": "Ok"}},
        )
        assert msg.type == MessageType.interactive
        assert msg.interactive.button_reply.id == "b1"


class TestIncomingGroupMessageUnion:
    adapter = TypeAdapter(IncomingGroupMessage)

    def test_resolves_text(self):
        """IncomingGroupMessage discriminator resolves type='text' to IncomingGroupTextMessage."""
        msg = self.adapter.validate_python({**GROUP_BASE, "type": "text", "text": {"body": "oi"}})
        assert isinstance(msg, IncomingGroupTextMessage)
        assert msg.group_id == GROUP_ID

    def test_resolves_image(self):
        """IncomingGroupMessage discriminator resolves type='image' to IncomingGroupImageMessage."""
        msg = self.adapter.validate_python(
            {
                **GROUP_BASE,
                "type": "image",
                "image": {"id": "m1", "mime_type": "image/jpeg", "sha256": "x", "url": "https://example.com/i"},
            }
        )
        assert isinstance(msg, IncomingGroupImageMessage)

    def test_invalid_type_raises(self):
        """IncomingGroupMessage raises ValidationError for unknown type values."""
        with pytest.raises(ValidationError):
            self.adapter.validate_python({**GROUP_BASE, "type": "unknown_type"})


class TestIncomingMessageUnion:
    adapter = TypeAdapter(IncomingMessage)

    def test_resolves_text(self):
        """IncomingMessage discriminator resolves type='text' to IncomingTextMessage."""
        msg = self.adapter.validate_python({**BASE, "type": "text", "text": {"body": "oi"}})
        assert isinstance(msg, IncomingTextMessage)

    def test_resolves_audio(self):
        """IncomingMessage discriminator resolves type='audio' to IncomingAudioMessage."""
        msg = self.adapter.validate_python(
            {
                **BASE,
                "type": "audio",
                "audio": {
                    "id": "m1",
                    "mime_type": "audio/ogg",
                    "sha256": "x",
                    "url": "https://example.com/a",
                    "voice": False,
                },
            }
        )
        assert isinstance(msg, IncomingAudioMessage)

    def test_resolves_image(self):
        """IncomingMessage discriminator resolves type='image' to IncomingImageMessage."""
        msg = self.adapter.validate_python(
            {
                **BASE,
                "type": "image",
                "image": {"id": "m1", "mime_type": "image/jpeg", "sha256": "x", "url": "https://example.com/i"},
            }
        )
        assert isinstance(msg, IncomingImageMessage)

    def test_resolves_location(self):
        """IncomingMessage discriminator resolves type='location' to IncomingLocationMessage."""
        msg = self.adapter.validate_python(
            {**BASE, "type": "location", "location": {"latitude": 0.0, "longitude": 0.0, "name": "N", "address": "A"}}
        )
        assert isinstance(msg, IncomingLocationMessage)

    def test_resolves_reaction(self):
        """IncomingMessage discriminator resolves type='reaction' to IncomingReactionMessage."""
        msg = self.adapter.validate_python(
            {**BASE, "type": "reaction", "reaction": {"message_id": "wamid.x", "emoji": "❤️"}}
        )
        assert isinstance(msg, IncomingReactionMessage)

    def test_resolves_button(self):
        """IncomingMessage discriminator resolves type='button' to IncomingButtonMessage."""
        msg = self.adapter.validate_python(
            {**BASE, "type": "button", "context": {"id": "wamid.orig"}, "button": {"text": "Ok", "payload": "ok"}}
        )
        assert isinstance(msg, IncomingButtonMessage)

    def test_resolves_unsupported(self):
        """IncomingMessage discriminator resolves type='unsupported' to IncomingUnsupportedMessage."""
        msg = self.adapter.validate_python(
            {
                **BASE,
                "type": "unsupported",
                "errors": [{"code": 1, "title": "T", "message": "M", "error_data": {"details": "D"}}],
            }
        )
        assert isinstance(msg, IncomingUnsupportedMessage)

    def test_invalid_type_raises(self):
        """IncomingMessage raises ValidationError for unknown type values."""
        with pytest.raises(ValidationError):
            self.adapter.validate_python({**BASE, "type": "unknown_type"})
