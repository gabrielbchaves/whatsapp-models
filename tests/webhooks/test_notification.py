"""Tests for the WebhookNotification envelope and its nested structures."""

import pytest
from pydantic import ValidationError

from whatsapp_models.webhooks.messages import IncomingGroupTextMessage, IncomingTextMessage
from whatsapp_models.webhooks.notification import (
    Entry,
    MessagesChange,
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
    def test_basic(self) -> None:
        """Metadata stores display_phone_number and phone_number_id."""
        m = Metadata(**METADATA)
        assert m.display_phone_number == "15550001234"
        assert m.phone_number_id == "pn_id_1"

    def test_requires_both_fields(self) -> None:
        """Metadata raises ValidationError when any required field is missing."""
        with pytest.raises(ValidationError):
            Metadata.model_validate({"display_phone_number": "15550001234"})


class TestValue:
    def test_minimal(self) -> None:
        """Value can be constructed with only messaging_product and metadata."""
        v = Value.model_validate(BASE_VALUE)
        assert v.messaging_product == "whatsapp"
        assert v.contacts == []
        assert v.messages == []
        assert v.statuses == []
        assert v.errors == []

    def test_requires_messaging_product(self) -> None:
        """Value raises ValidationError when messaging_product is missing."""
        with pytest.raises(ValidationError):
            Value.model_validate({"metadata": METADATA})


class TestChange:
    def test_basic(self) -> None:
        """MessagesChange stores field name and a Value."""
        c = MessagesChange.model_validate({"field": "messages", "value": BASE_VALUE})
        assert c.field == "messages"
        assert c.value.metadata.phone_number_id == "pn_id_1"


class TestEntry:
    def test_basic(self) -> None:
        """Entry stores id and a list of Change objects."""
        e = Entry.model_validate(
            {
                "id": "waba_id_1",
                "changes": [{"field": "messages", "value": BASE_VALUE}],
            }
        )
        assert e.id == "waba_id_1"
        assert len(e.changes) == 1
        assert e.changes[0].field == "messages"


class TestWebhookNotification:
    def test_basic(self) -> None:
        """WebhookNotification stores object type and entry list."""
        notif = WebhookNotification.model_validate(
            {
                "object": "whatsapp_business_account",
                "entry": [
                    {
                        "id": "waba_id_1",
                        "changes": [{"field": "messages", "value": BASE_VALUE}],
                    }
                ],
            }
        )
        assert notif.object == "whatsapp_business_account"
        assert len(notif.entry) == 1
        change_value = notif.entry[0].changes[0].value
        assert isinstance(change_value, Value)
        assert change_value.messaging_product == "whatsapp"

    def test_requires_object_and_entry(self) -> None:
        """WebhookNotification raises ValidationError when object is missing."""
        with pytest.raises(ValidationError):
            WebhookNotification.model_validate({"entry": []})

    def test_parses_direct_message_in_value(self) -> None:
        """Value.messages resolves a direct text message to IncomingTextMessage."""
        value = Value.model_validate(
            {
                **BASE_VALUE,
                "messages": [
                    {
                        "from": "5511999999999",
                        "id": "wamid.x",
                        "timestamp": "1700000000",
                        "type": "text",
                        "text": {"body": "oi"},
                    }
                ],
            }
        )
        assert isinstance(value.messages[0], IncomingTextMessage)

    def test_parses_group_message_in_value(self) -> None:
        """Value.messages resolves a group text message to IncomingGroupTextMessage."""
        value = Value.model_validate(
            {
                **BASE_VALUE,
                "messages": [
                    {
                        "from": "5511999999999",
                        "group_id": "120363000000000001@g.us",
                        "id": "wamid.x",
                        "timestamp": "1700000000",
                        "type": "text",
                        "text": {"body": "oi grupo"},
                    }
                ],
            }
        )
        assert isinstance(value.messages[0], IncomingGroupTextMessage)
        assert value.messages[0].group_id == "120363000000000001@g.us"
