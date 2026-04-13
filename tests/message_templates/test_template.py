"""Tests for CreateTemplateRequest and TemplateResponse models."""

import pytest
from pydantic import ValidationError

from whatsapp_models.message_templates.enums import TemplateCategory, TemplateStatus
from whatsapp_models.message_templates.template import CreateTemplateRequest, TemplateResponse


class TestCreateTemplateRequest:
    def test_minimal(self):
        """CreateTemplateRequest accepts minimal required fields."""
        req = CreateTemplateRequest(
            name="hello_world",
            language="pt_BR",
            category=TemplateCategory.UTILITY,
        )
        assert req.name == "hello_world"
        assert req.language == "pt_BR"
        assert req.category == TemplateCategory.UTILITY
        assert req.components == []

    def test_with_components(self):
        """CreateTemplateRequest stores a list of template components."""
        req = CreateTemplateRequest(
            name="order_confirm",
            language="pt_BR",
            category=TemplateCategory.UTILITY,
            components=[
                {"type": "BODY", "text": "Pedido {{1}} confirmado."},
                {"type": "FOOTER", "text": "Dúvidas? Fale conosco."},
            ],
        )
        assert len(req.components) == 2

    def test_requires_name(self):
        """CreateTemplateRequest raises ValidationError when name is missing."""
        with pytest.raises(ValidationError):
            CreateTemplateRequest(language="pt_BR", category=TemplateCategory.UTILITY)

    def test_requires_language(self):
        """CreateTemplateRequest raises ValidationError when language is missing."""
        with pytest.raises(ValidationError):
            CreateTemplateRequest(name="hello", category=TemplateCategory.UTILITY)

    def test_requires_category(self):
        """CreateTemplateRequest raises ValidationError when category is missing."""
        with pytest.raises(ValidationError):
            CreateTemplateRequest(name="hello", language="pt_BR")

    def test_serialization(self):
        """CreateTemplateRequest serializes category as plain string."""
        req = CreateTemplateRequest(name="t", language="pt_BR", category=TemplateCategory.MARKETING)
        assert req.model_dump()["category"] == "MARKETING"


class TestTemplateResponse:
    def test_basic(self):
        """TemplateResponse parses API creation response correctly."""
        resp = TemplateResponse(id="tpl_123", status=TemplateStatus.PENDING, category=TemplateCategory.UTILITY)
        assert resp.id == "tpl_123"
        assert resp.status == TemplateStatus.PENDING

    def test_requires_id_and_status(self):
        """TemplateResponse raises ValidationError when id or status is missing."""
        with pytest.raises(ValidationError):
            TemplateResponse(status=TemplateStatus.APPROVED)

    def test_serializes_status_as_string(self):
        """TemplateResponse serializes status as plain string."""
        resp = TemplateResponse(id="x", status=TemplateStatus.APPROVED, category=TemplateCategory.UTILITY)
        assert resp.model_dump()["status"] == "APPROVED"
