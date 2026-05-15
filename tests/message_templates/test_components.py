"""Tests for template component models and their discriminated union."""

import pytest
from pydantic import TypeAdapter, ValidationError

from whatsapp_models.message_templates.components import (
    BodyComponent,
    ButtonsComponent,
    FooterComponent,
    HeaderComponent,
    QuickReplyButton,
    TemplateComponent,
    UrlButton,
)
from whatsapp_models.message_templates.enums import HeaderFormat


class TestHeaderComponent:
    def test_text_header(self) -> None:
        """HeaderComponent accepts TEXT format with a text field."""
        comp = HeaderComponent(format=HeaderFormat.TEXT, text="Olá {{1}}!")
        assert comp.type == "HEADER"
        assert comp.format == HeaderFormat.TEXT
        assert comp.text == "Olá {{1}}!"

    def test_image_header(self) -> None:
        """HeaderComponent accepts IMAGE format with an example."""
        comp = HeaderComponent(
            format=HeaderFormat.IMAGE,
            example={"header_handle": ["https://example.com/img.jpg"]},
        )
        assert comp.format == HeaderFormat.IMAGE

    def test_requires_format(self) -> None:
        """HeaderComponent raises ValidationError when format is missing."""
        with pytest.raises(ValidationError):
            HeaderComponent.model_validate({})

    def test_serializes_type_as_string(self) -> None:
        """HeaderComponent serializes type as plain string 'HEADER'."""
        comp = HeaderComponent(format=HeaderFormat.TEXT, text="Hi")
        assert comp.model_dump()["type"] == "HEADER"


class TestBodyComponent:
    def test_basic(self) -> None:
        """BodyComponent stores text and optional example correctly."""
        comp = BodyComponent(text="Seu pedido {{1}} foi confirmado.")
        assert comp.type == "BODY"
        assert comp.text == "Seu pedido {{1}} foi confirmado."

    def test_with_example(self) -> None:
        """BodyComponent accepts optional text variable examples."""
        comp = BodyComponent(text="Olá {{1}}!", example={"body_text": [["João"]]})
        assert comp.example == {"body_text": [["João"]]}

    def test_requires_text(self) -> None:
        """BodyComponent raises ValidationError when text is missing."""
        with pytest.raises(ValidationError):
            BodyComponent.model_validate({})

    def test_serializes_type_as_string(self) -> None:
        """BodyComponent serializes type as plain string 'BODY'."""
        assert BodyComponent(text="hi").model_dump()["type"] == "BODY"


class TestFooterComponent:
    def test_basic(self) -> None:
        """FooterComponent stores text correctly."""
        comp = FooterComponent(text="Não responda esta mensagem.")
        assert comp.type == "FOOTER"
        assert comp.text == "Não responda esta mensagem."

    def test_requires_text(self) -> None:
        """FooterComponent raises ValidationError when text is missing."""
        with pytest.raises(ValidationError):
            FooterComponent.model_validate({})

    def test_serializes_type_as_string(self) -> None:
        """FooterComponent serializes type as plain string 'FOOTER'."""
        assert FooterComponent(text="footer").model_dump()["type"] == "FOOTER"


class TestButtonsComponent:
    def test_quick_reply_button(self) -> None:
        """ButtonsComponent accepts QUICK_REPLY buttons."""
        comp = ButtonsComponent.model_validate({"buttons": [{"type": "QUICK_REPLY", "text": "Cancelar"}]})
        assert comp.type == "BUTTONS"
        assert isinstance(comp.buttons[0], QuickReplyButton)
        assert comp.buttons[0].text == "Cancelar"

    def test_url_button(self) -> None:
        """ButtonsComponent accepts URL buttons."""
        comp = ButtonsComponent.model_validate(
            {"buttons": [{"type": "URL", "text": "Ver pedido", "url": "https://example.com/{{1}}"}]}
        )
        assert isinstance(comp.buttons[0], UrlButton)
        assert comp.buttons[0].url == "https://example.com/{{1}}"

    def test_mixed_buttons(self) -> None:
        """ButtonsComponent accepts a mix of button types."""
        comp = ButtonsComponent.model_validate(
            {
                "buttons": [
                    {"type": "QUICK_REPLY", "text": "Sim"},
                    {"type": "URL", "text": "Ver", "url": "https://example.com"},
                ]
            }
        )
        assert len(comp.buttons) == 2

    def test_requires_at_least_one_button(self) -> None:
        """ButtonsComponent raises ValidationError when buttons list is empty."""
        with pytest.raises(ValidationError):
            ButtonsComponent(buttons=[])

    def test_serializes_type_as_string(self) -> None:
        """ButtonsComponent serializes type as plain string 'BUTTONS'."""
        comp = ButtonsComponent.model_validate({"buttons": [{"type": "QUICK_REPLY", "text": "Ok"}]})
        assert comp.model_dump()["type"] == "BUTTONS"


class TestTemplateComponentUnion:
    adapter: TypeAdapter[TemplateComponent] = TypeAdapter(TemplateComponent)

    def test_resolves_header(self) -> None:
        """TemplateComponent discriminator resolves type='HEADER' to HeaderComponent."""
        comp = self.adapter.validate_python({"type": "HEADER", "format": "TEXT", "text": "Hi"})
        assert isinstance(comp, HeaderComponent)

    def test_resolves_body(self) -> None:
        """TemplateComponent discriminator resolves type='BODY' to BodyComponent."""
        comp = self.adapter.validate_python({"type": "BODY", "text": "Hello {{1}}"})
        assert isinstance(comp, BodyComponent)

    def test_resolves_footer(self) -> None:
        """TemplateComponent discriminator resolves type='FOOTER' to FooterComponent."""
        comp = self.adapter.validate_python({"type": "FOOTER", "text": "footer"})
        assert isinstance(comp, FooterComponent)

    def test_resolves_buttons(self) -> None:
        """TemplateComponent discriminator resolves type='BUTTONS' to ButtonsComponent."""
        comp = self.adapter.validate_python({"type": "BUTTONS", "buttons": [{"type": "QUICK_REPLY", "text": "Ok"}]})
        assert isinstance(comp, ButtonsComponent)

    def test_invalid_type_raises(self) -> None:
        """TemplateComponent raises ValidationError for unknown type values."""
        with pytest.raises(ValidationError):
            self.adapter.validate_python({"type": "UNKNOWN"})
