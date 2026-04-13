"""Tests for the WebhookNotification envelope and its nested structures."""

import pytest
from pydantic import ValidationError

from whatsapp_models.webhooks.messages import IncomingGroupTextMessage, IncomingTextMessage
from whatsapp_models.webhooks.notification import (
    Change,
    Entry,
    Metadata,
    Value,
    WebhookNotification,
)

METADATA = {"display_phone_number": "15550001234", "phone_number_id": "pn_id_1"}
BASE_VALUE = {
    "messaging_product": "whatsapp",
    "metadata": METADATA,
}


class TestMetadata:
    def test_basic(self):
        """Metadata stores display_phone_number and phone_number_id."""
        m = Metadata(**METADATA)
        assert m.display_phone_number == "15550001234"
        assert m.phone_number_id == "pn_id_1"

    def test_requires_both_fields(self):
        """Metadata raises ValidationError when any required field is missing."""
        with pytest.raises(ValidationError):
            Metadata(display_phone_number="15550001234")


class TestValue:
    def test_minimal(self):
        """Value can be constructed with only messaging_product and metadata."""
        v = Value(**BASE_VALUE)
        assert v.messaging_product == "whatsapp"
        assert v.contacts == []
        assert v.messages == []
        assert v.statuses == []
        assert v.errors == []

    def test_requires_messaging_product(self):
        """Value raises ValidationError when messaging_product is missing."""
        with pytest.raises(ValidationError):
            Value(metadata=METADATA)


class TestChange:
    def test_basic(self):
        """Change stores field name and a Value."""
        c = Change(field="messages", value=BASE_VALUE)
        assert c.field == "messages"
        assert c.value.metadata.phone_number_id == "pn_id_1"


class TestEntry:
    def test_basic(self):
        """Entry stores id and a list of Change objects."""
        e = Entry(
            id="waba_id_1",
            changes=[{"field": "messages", "value": BASE_VALUE}],
        )
        assert e.id == "waba_id_1"
        assert len(e.changes) == 1
        assert e.changes[0].field == "messages"


class TestWebhookNotification:
    def test_basic(self):
        """WebhookNotification stores object type and entry list."""
        notif = WebhookNotification(
            object="whatsapp_business_account",
            entry=[
                {
                    "id": "waba_id_1",
                    "changes": [{"field": "messages", "value": BASE_VALUE}],
                }
            ],
        )
        assert notif.object == "whatsapp_business_account"
        assert len(notif.entry) == 1
        assert notif.entry[0].changes[0].value.messaging_product == "whatsapp"

    def test_requires_object_and_entry(self):
        """WebhookNotification raises ValidationError when object is missing."""
        with pytest.raises(ValidationError):
            WebhookNotification(entry=[])

    def test_parses_direct_message_in_value(self):
        """Value.messages resolves a direct text message to IncomingTextMessage."""
        value = Value(
            **BASE_VALUE,
            messages=[
                {
                    "from": "5511999999999",
                    "id": "wamid.x",
                    "timestamp": "1700000000",
                    "type": "text",
                    "text": {"body": "oi"},
                }
            ],
        )
        assert isinstance(value.messages[0], IncomingTextMessage)

    def test_parses_group_message_in_value(self):
        """Value.messages resolves a group text message to IncomingGroupTextMessage."""
        value = Value(
            **BASE_VALUE,
            messages=[
                {
                    "from": "5511999999999",
                    "group_id": "120363000000000001@g.us",
                    "id": "wamid.x",
                    "timestamp": "1700000000",
                    "type": "text",
                    "text": {"body": "oi grupo"},
                }
            ],
        )
        assert isinstance(value.messages[0], IncomingGroupTextMessage)
        assert value.messages[0].group_id == "120363000000000001@g.us"
