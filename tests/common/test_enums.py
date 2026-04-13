"""Tests for common enums — MessageType, Currency, Language and contact entry types."""

import json

from whatsapp_models.common.enums import (
    AddressType,
    Currency,
    EmailType,
    Language,
    MessageType,
    PhoneType,
    UrlType,
)


class TestMessageType:
    def test_all_outgoing_types_present(self):
        """All bidirectional message types are members of MessageType."""
        expected = {
            "text",
            "audio",
            "image",
            "video",
            "document",
            "sticker",
            "location",
            "contacts",
            "reaction",
            "template",
            "interactive",
        }
        assert expected.issubset({m.value for m in MessageType})

    def test_all_incoming_only_types_present(self):
        """Incoming-only types button and unsupported are members of MessageType."""
        assert {"button", "unsupported"}.issubset({m.value for m in MessageType})

    def test_is_str(self):
        """MessageType members are plain strings."""
        assert isinstance(MessageType.text, str)
        assert MessageType.text == "text"

    def test_serializes_as_plain_string(self):
        """MessageType members serialize to plain JSON strings."""
        assert json.dumps(MessageType.audio) == '"audio"'


class TestLanguage:
    def test_common_languages_present(self):
        """Common language codes are members of Language."""
        expected = {"pt_BR", "en_US", "es_ES", "es_MX", "pt_PT"}
        assert expected.issubset({lang.value for lang in Language})

    def test_is_str(self):
        """Language members are plain strings."""
        assert isinstance(Language.pt_BR, str)
        assert Language.pt_BR == "pt_BR"


class TestCurrency:
    def test_common_currencies_present(self):
        """Common currency codes are members of Currency."""
        assert {"BRL", "USD", "EUR"}.issubset({c.value for c in Currency})

    def test_is_str(self):
        """Currency members are plain strings."""
        assert isinstance(Currency.BRL, str)
        assert Currency.BRL == "BRL"


class TestContactEntryTypes:
    def test_address_type_values(self):
        """AddressType has exactly HOME and WORK."""
        assert set(AddressType) == {AddressType.HOME, AddressType.WORK}
        assert AddressType.HOME == "HOME"
        assert AddressType.WORK == "WORK"

    def test_phone_type_values(self):
        """PhoneType has exactly CELL, MAIN, IPHONE, HOME and WORK."""
        assert {t.value for t in PhoneType} == {"CELL", "MAIN", "IPHONE", "HOME", "WORK"}

    def test_email_type_values(self):
        """EmailType has exactly HOME and WORK."""
        assert set(EmailType) == {EmailType.HOME, EmailType.WORK}

    def test_url_type_values(self):
        """UrlType has exactly HOME and WORK."""
        assert set(UrlType) == {UrlType.HOME, UrlType.WORK}
