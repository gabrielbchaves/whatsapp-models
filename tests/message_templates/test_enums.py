"""Tests for message_templates enums: TemplateCategory, TemplateStatus, ButtonType, HeaderFormat."""

from whatsapp_models.message_templates.enums import (
    ButtonType,
    ComponentType,
    HeaderFormat,
    TemplateCategory,
    TemplateStatus,
)


class TestTemplateCategory:
    def test_all_categories_present(self) -> None:
        """TemplateCategory has MARKETING, UTILITY and AUTHENTICATION."""
        assert {c.value for c in TemplateCategory} == {"MARKETING", "UTILITY", "AUTHENTICATION"}

    def test_is_str(self) -> None:
        """TemplateCategory members are plain strings."""
        assert TemplateCategory.MARKETING == "MARKETING"


class TestTemplateStatus:
    def test_common_statuses_present(self) -> None:
        """TemplateStatus has at least APPROVED, PENDING and REJECTED."""
        assert {"APPROVED", "PENDING", "REJECTED"}.issubset({s.value for s in TemplateStatus})

    def test_is_str(self) -> None:
        """TemplateStatus members are plain strings."""
        assert TemplateStatus.APPROVED == "APPROVED"


class TestButtonType:
    def test_all_button_types_present(self) -> None:
        """ButtonType has QUICK_REPLY, URL, PHONE_NUMBER, OTP, FLOW, CATALOG and MPM."""
        expected = {"QUICK_REPLY", "URL", "PHONE_NUMBER", "OTP", "FLOW", "CATALOG", "MPM"}
        assert expected.issubset({b.value for b in ButtonType})

    def test_is_str(self) -> None:
        """ButtonType members are plain strings."""
        assert ButtonType.QUICK_REPLY == "QUICK_REPLY"


class TestHeaderFormat:
    def test_all_formats_present(self) -> None:
        """HeaderFormat has TEXT, IMAGE, VIDEO, DOCUMENT and LOCATION."""
        assert {f.value for f in HeaderFormat} == {"TEXT", "IMAGE", "VIDEO", "DOCUMENT", "LOCATION"}

    def test_is_str(self) -> None:
        """HeaderFormat members are plain strings."""
        assert HeaderFormat.TEXT == "TEXT"


class TestComponentType:
    def test_all_types_present(self) -> None:
        """ComponentType has HEADER, BODY, FOOTER and BUTTONS."""
        assert {t.value for t in ComponentType} == {"HEADER", "BODY", "FOOTER", "BUTTONS"}

    def test_is_str(self) -> None:
        """ComponentType members are plain strings."""
        assert ComponentType.HEADER == "HEADER"
