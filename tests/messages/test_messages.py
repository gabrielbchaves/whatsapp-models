"""Tests for all outgoing message models."""

import pytest
from pydantic import TypeAdapter, ValidationError

from whatsapp_models.common.enums import MessageType
from whatsapp_models.messages.base import MessagingProduct, RecipientType
from whatsapp_models.messages.contacts import ContactsMessage
from whatsapp_models.messages.interactive import (
    CtaUrlInteractive,
    FlowInteractive,
    InteractiveMessage,
    ListInteractive,
    LocationRequestInteractive,
    ReplyButtonsInteractive,
)
from whatsapp_models.messages.location import LocationMessage
from whatsapp_models.messages.media import (
    AudioMediaObject,
    AudioMessage,
    DocumentMessage,
    ImageMessage,
    StickerMessage,
    VideoMessage,
)
from whatsapp_models.messages.reaction import ReactionMessage
from whatsapp_models.messages.status import MessageStatusUpdate, TypingIndicatorContent
from whatsapp_models.messages.template import TemplateMessage
from whatsapp_models.messages.text import TextMessage
from whatsapp_models.messages.unions import OutgoingMessage

RECIPIENT = "+5511999999999"
BASE = {"messaging_product": "whatsapp", "to": RECIPIENT}


class TestTextMessage:
    def test_basic(self):
        """TextMessage stores type, to, and text body correctly."""
        msg = TextMessage(**BASE, text={"body": "Olá!"})
        assert msg.type == MessageType.text
        assert msg.to == RECIPIENT
        assert msg.text.body == "Olá!"

    def test_preview_url_default_false(self):
        """TextMessage.text.preview_url defaults to False."""
        msg = TextMessage(**BASE, text={"body": "https://example.com"})
        assert msg.text.preview_url is False

    def test_missing_body_raises(self):
        """TextMessage raises ValidationError when text body is missing."""
        with pytest.raises(ValidationError):
            TextMessage(**BASE, text={})

    def test_messaging_product_fixed(self):
        """TextMessage.messaging_product is always 'whatsapp'."""
        msg = TextMessage(**BASE, text={"body": "hi"})
        assert msg.messaging_product == MessagingProduct.whatsapp

    def test_recipient_type_default(self):
        """TextMessage.recipient_type defaults to 'individual'."""
        msg = TextMessage(**BASE, text={"body": "hi"})
        assert msg.recipient_type == RecipientType.individual

    def test_serialization(self):
        """TextMessage serializes type as plain string."""
        msg = TextMessage(**BASE, text={"body": "hi"})
        data = msg.model_dump()
        assert data["type"] == "text"
        assert data["text"]["body"] == "hi"


class TestAudioMessage:
    def test_with_id(self):
        """AudioMessage accepts a media ID and sets link to None."""
        msg = AudioMessage(**BASE, audio={"id": "abc123"})
        assert msg.type == MessageType.audio
        assert msg.audio.id == "abc123"
        assert msg.audio.link is None

    def test_with_link(self):
        """AudioMessage accepts a media link URL."""
        msg = AudioMessage(**BASE, audio={"link": "https://example.com/audio.mp3"})
        assert msg.audio.link == "https://example.com/audio.mp3"

    def test_requires_id_or_link(self):
        """AudioMessage raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            AudioMessage(**BASE, audio={})

    def test_audio_field_is_audio_media_object(self):
        """AudioMessage.audio is an AudioMediaObject instance."""
        msg = AudioMessage(**BASE, audio={"id": "abc123"})
        assert isinstance(msg.audio, AudioMediaObject)

    def test_voice_defaults_false(self):
        """AudioMessage.audio.voice defaults to False."""
        msg = AudioMessage(**BASE, audio={"id": "abc123"})
        assert msg.audio.voice is False

    def test_voice_true(self):
        """AudioMessage.audio.voice can be set to True for PTT messages."""
        msg = AudioMessage(**BASE, audio={"id": "abc123", "voice": True})
        assert msg.audio.voice is True


class TestImageMessage:
    def test_with_id_and_caption(self):
        """ImageMessage accepts a media ID and optional caption."""
        msg = ImageMessage(**BASE, image={"id": "img1", "caption": "foto"})
        assert msg.type == MessageType.image
        assert msg.image.caption == "foto"

    def test_with_link(self):
        """ImageMessage accepts a media link URL."""
        msg = ImageMessage(**BASE, image={"link": "https://example.com/img.jpg"})
        assert msg.image.link == "https://example.com/img.jpg"

    def test_requires_id_or_link(self):
        """ImageMessage raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            ImageMessage(**BASE, image={})


class TestVideoMessage:
    def test_with_id(self):
        """VideoMessage accepts a media ID."""
        msg = VideoMessage(**BASE, video={"id": "vid1"})
        assert msg.type == MessageType.video

    def test_requires_id_or_link(self):
        """VideoMessage raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            VideoMessage(**BASE, video={})


class TestDocumentMessage:
    def test_with_id_and_filename(self):
        """DocumentMessage accepts a media ID and optional filename."""
        msg = DocumentMessage(**BASE, document={"id": "doc1", "filename": "relatorio.pdf"})
        assert msg.type == MessageType.document
        assert msg.document.filename == "relatorio.pdf"

    def test_requires_id_or_link(self):
        """DocumentMessage raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            DocumentMessage(**BASE, document={})


class TestStickerMessage:
    def test_with_id(self):
        """StickerMessage accepts a media ID."""
        msg = StickerMessage(**BASE, sticker={"id": "stk1"})
        assert msg.type == MessageType.sticker

    def test_requires_id_or_link(self):
        """StickerMessage raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            StickerMessage(**BASE, sticker={})


class TestLocationMessage:
    def test_basic(self):
        """LocationMessage stores latitude, longitude, name and address."""
        msg = LocationMessage(
            **BASE,
            location={"latitude": -23.5505, "longitude": -46.6333, "name": "SP", "address": "Centro"},
        )
        assert msg.type == MessageType.location
        assert msg.location.latitude == -23.5505
        assert msg.location.longitude == -46.6333

    def test_requires_name_and_address(self):
        """LocationMessage raises ValidationError when name or address is missing."""
        with pytest.raises(ValidationError):
            LocationMessage(**BASE, location={"latitude": 0.0, "longitude": 0.0})

    def test_requires_lat_lng(self):
        """LocationMessage raises ValidationError when coordinates are missing."""
        with pytest.raises(ValidationError):
            LocationMessage(**BASE, location={})


class TestReactionMessage:
    def test_basic(self):
        """ReactionMessage stores message_id and emoji correctly."""
        msg = ReactionMessage(**BASE, reaction={"message_id": "wamid.abc", "emoji": "👍"})
        assert msg.type == MessageType.reaction
        assert msg.reaction.emoji == "👍"

    def test_requires_message_id_and_emoji(self):
        """ReactionMessage raises ValidationError when emoji is missing."""
        with pytest.raises(ValidationError):
            ReactionMessage(**BASE, reaction={"message_id": "wamid.abc"})


class TestContactsMessage:
    def test_basic(self):
        """ContactsMessage stores a list of contacts correctly."""
        contact = {
            "name": {"formatted_name": "João Silva", "first_name": "João"},
            "phones": [{"phone": "+5511999999999", "type": "CELL"}],
        }
        msg = ContactsMessage(**BASE, contacts=[contact])
        assert msg.type == MessageType.contacts
        assert msg.contacts[0].name.formatted_name == "João Silva"

    def test_requires_at_least_one_contact(self):
        """ContactsMessage raises ValidationError when contacts list is empty."""
        with pytest.raises(ValidationError):
            ContactsMessage(**BASE, contacts=[])


class TestTemplateMessage:
    def test_basic(self):
        """TemplateMessage stores template name and language correctly."""
        msg = TemplateMessage(
            **BASE,
            template={"name": "hello_world", "language": {"code": "pt_BR"}},
        )
        assert msg.type == MessageType.template
        assert msg.template.name == "hello_world"
        assert msg.template.language.code == "pt_BR"

    def test_requires_name_and_language(self):
        """TemplateMessage raises ValidationError when language is missing."""
        with pytest.raises(ValidationError):
            TemplateMessage(**BASE, template={"name": "hello_world"})


class TestInteractiveReplyButtonsMessage:
    def test_basic(self):
        """InteractiveMessage resolves to ReplyButtonsInteractive when type is 'button'."""
        msg = InteractiveMessage(
            **BASE,
            interactive={
                "type": "button",
                "body": {"text": "Escolha uma opção:"},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "btn1", "title": "Sim"}},
                        {"type": "reply", "reply": {"id": "btn2", "title": "Não"}},
                    ]
                },
            },
        )
        assert msg.type == MessageType.interactive
        assert isinstance(msg.interactive, ReplyButtonsInteractive)
        assert len(msg.interactive.action.buttons) == 2

    def test_max_three_buttons(self):
        """InteractiveMessage raises ValidationError when more than 3 buttons are provided."""
        with pytest.raises(ValidationError):
            InteractiveMessage(
                **BASE,
                interactive={
                    "type": "button",
                    "body": {"text": "Escolha:"},
                    "action": {
                        "buttons": [{"type": "reply", "reply": {"id": f"btn{i}", "title": f"Op {i}"}} for i in range(4)]
                    },
                },
            )


class TestInteractiveListMessage:
    def test_basic(self):
        """InteractiveMessage resolves to ListInteractive when type is 'list'."""
        msg = InteractiveMessage(
            **BASE,
            interactive={
                "type": "list",
                "body": {"text": "Escolha um item:"},
                "action": {
                    "button": "Ver opções",
                    "sections": [{"title": "Seção 1", "rows": [{"id": "row1", "title": "Item 1"}]}],
                },
            },
        )
        assert isinstance(msg.interactive, ListInteractive)
        assert msg.interactive.action.sections[0].rows[0].id == "row1"


class TestInteractiveCtaUrlMessage:
    def test_basic(self):
        """InteractiveMessage resolves to CtaUrlInteractive when type is 'cta_url'."""
        msg = InteractiveMessage(
            **BASE,
            interactive={
                "type": "cta_url",
                "body": {"text": "Acesse nosso site"},
                "action": {
                    "name": "cta_url",
                    "parameters": {"display_text": "Acessar", "url": "https://example.com"},
                },
            },
        )
        assert isinstance(msg.interactive, CtaUrlInteractive)
        assert msg.interactive.action.parameters.url == "https://example.com"


class TestInteractiveFlowMessage:
    def test_basic(self):
        """InteractiveMessage resolves to FlowInteractive when type is 'flow'."""
        msg = InteractiveMessage(
            **BASE,
            interactive={
                "type": "flow",
                "body": {"text": "Preencha o formulário"},
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_token": "token123",
                        "flow_id": "flow_abc",
                        "flow_cta": "Abrir",
                        "flow_action": "navigate",
                    },
                },
            },
        )
        assert isinstance(msg.interactive, FlowInteractive)
        assert msg.interactive.action.parameters.flow_id == "flow_abc"


class TestInteractiveLocationRequestMessage:
    def test_basic(self):
        """InteractiveMessage resolves to LocationRequestInteractive when type is 'location_request_message'."""
        msg = InteractiveMessage(
            **BASE,
            interactive={
                "type": "location_request_message",
                "body": {"text": "Compartilhe sua localização"},
                "action": {"name": "send_location"},
            },
        )
        assert isinstance(msg.interactive, LocationRequestInteractive)


class TestOutgoingMessageUnion:
    adapter = TypeAdapter(OutgoingMessage)

    def test_resolves_text(self):
        """OutgoingMessage discriminator resolves type='text' to TextMessage."""
        msg = self.adapter.validate_python({**BASE, "type": "text", "text": {"body": "oi"}})
        assert isinstance(msg, TextMessage)

    def test_resolves_audio(self):
        """OutgoingMessage discriminator resolves type='audio' to AudioMessage."""
        msg = self.adapter.validate_python({**BASE, "type": "audio", "audio": {"id": "abc"}})
        assert isinstance(msg, AudioMessage)

    def test_resolves_image(self):
        """OutgoingMessage discriminator resolves type='image' to ImageMessage."""
        msg = self.adapter.validate_python({**BASE, "type": "image", "image": {"id": "abc"}})
        assert isinstance(msg, ImageMessage)

    def test_resolves_location(self):
        """OutgoingMessage discriminator resolves type='location' to LocationMessage."""
        msg = self.adapter.validate_python(
            {**BASE, "type": "location", "location": {"latitude": 0.0, "longitude": 0.0, "name": "N", "address": "A"}}
        )
        assert isinstance(msg, LocationMessage)

    def test_resolves_reaction(self):
        """OutgoingMessage discriminator resolves type='reaction' to ReactionMessage."""
        msg = self.adapter.validate_python(
            {**BASE, "type": "reaction", "reaction": {"message_id": "wamid.x", "emoji": "❤️"}}
        )
        assert isinstance(msg, ReactionMessage)

    def test_resolves_interactive(self):
        """OutgoingMessage discriminator resolves type='interactive' to InteractiveMessage with nested sub-type."""
        msg = self.adapter.validate_python(
            {
                **BASE,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": "Escolha:"},
                    "action": {"buttons": [{"type": "reply", "reply": {"id": "b1", "title": "Ok"}}]},
                },
            }
        )
        assert isinstance(msg, InteractiveMessage)
        assert isinstance(msg.interactive, ReplyButtonsInteractive)

    def test_invalid_type_raises(self):
        """OutgoingMessage raises ValidationError for unknown type values."""
        with pytest.raises(ValidationError):
            self.adapter.validate_python({**BASE, "type": "unknown", "text": {"body": "hi"}})


class TestMessageStatusUpdate:
    def test_basic(self):
        """MessageStatusUpdate stores message_id with read status and whatsapp product."""
        update = MessageStatusUpdate(message_id="wamid.abc123")
        assert update.status == "read"
        assert update.messaging_product == "whatsapp"
        assert update.message_id == "wamid.abc123"
        assert update.typing_indicator is None

    def test_with_typing_indicator(self):
        """MessageStatusUpdate accepts an optional TypingIndicatorContent."""
        update = MessageStatusUpdate(message_id="wamid.abc123", typing_indicator=TypingIndicatorContent())
        assert update.typing_indicator is not None
        assert update.typing_indicator.type == "text"

    def test_typing_indicator_type_fixed(self):
        """TypingIndicatorContent.type is always 'text'."""
        content = TypingIndicatorContent()
        assert content.type == "text"

    def test_serialization(self):
        """MessageStatusUpdate serializes correctly for the API call."""
        update = MessageStatusUpdate(message_id="wamid.abc123", typing_indicator=TypingIndicatorContent())
        data = update.model_dump(exclude_none=False)
        assert data["status"] == "read"
        assert data["message_id"] == "wamid.abc123"
        assert data["typing_indicator"]["type"] == "text"
