"""Tests for contact message sub-types: Address, PhoneEntry, EmailEntry, UrlEntry."""

from whatsapp_models.common.enums import AddressType, EmailType, PhoneType, UrlType
from whatsapp_models.messages.contacts import Address, EmailEntry, PhoneEntry, UrlEntry


class TestAddress:
    def test_all_fields(self):
        """Address accepts all fields populated."""
        addr = Address(
            street="Rua das Flores, 123",
            city="São Paulo",
            state="SP",
            zip="01310-100",
            country="Brazil",
            country_code="BR",
            type=AddressType.WORK,
        )
        assert addr.street == "Rua das Flores, 123"
        assert addr.country_code == "BR"
        assert addr.type == AddressType.WORK

    def test_all_fields_optional(self):
        """Address can be instantiated with no fields."""
        addr = Address()
        assert addr.street is None
        assert addr.city is None
        assert addr.type is None

    def test_serializes_type_as_string(self):
        """Address.type serializes to a plain string."""
        addr = Address(type=AddressType.HOME)
        assert addr.model_dump()["type"] == "HOME"


class TestPhoneEntry:
    def test_required_phone(self):
        """PhoneEntry stores phone and type correctly."""
        entry = PhoneEntry(phone="+5511999999999", type=PhoneType.CELL)
        assert entry.phone == "+5511999999999"
        assert entry.type == PhoneType.CELL
        assert entry.wa_id is None

    def test_with_wa_id(self):
        """PhoneEntry stores optional wa_id."""
        entry = PhoneEntry(phone="+5511999999999", type=PhoneType.CELL, wa_id="5511999999999")
        assert entry.wa_id == "5511999999999"

    def test_phone_optional(self):
        """PhoneEntry can be instantiated with no fields."""
        entry = PhoneEntry()
        assert entry.phone is None

    def test_serializes_type_as_string(self):
        """PhoneEntry.type serializes to a plain string."""
        entry = PhoneEntry(phone="+1234", type=PhoneType.WORK)
        assert entry.model_dump()["type"] == "WORK"


class TestEmailEntry:
    def test_basic(self):
        """EmailEntry stores email and type correctly."""
        entry = EmailEntry(email="user@example.com", type=EmailType.HOME)
        assert entry.email == "user@example.com"
        assert entry.type == EmailType.HOME

    def test_all_optional(self):
        """EmailEntry can be instantiated with no fields."""
        entry = EmailEntry()
        assert entry.email is None

    def test_serializes_type_as_string(self):
        """EmailEntry.type serializes to a plain string."""
        entry = EmailEntry(email="x@x.com", type=EmailType.WORK)
        assert entry.model_dump()["type"] == "WORK"


class TestUrlEntry:
    def test_basic(self):
        """UrlEntry stores url and type correctly."""
        entry = UrlEntry(url="https://example.com", type=UrlType.WORK)
        assert entry.url == "https://example.com"
        assert entry.type == UrlType.WORK

    def test_all_optional(self):
        """UrlEntry can be instantiated with no fields."""
        entry = UrlEntry()
        assert entry.url is None
