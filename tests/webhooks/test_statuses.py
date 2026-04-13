"""Tests for MessageStatus and DeliveryStatus enum."""

import pytest
from pydantic import ValidationError

from whatsapp_models.webhooks.statuses import DeliveryStatus, MessageStatus

RECIPIENT = "5511999999999"


class TestDeliveryStatus:
    def test_values(self):
        """DeliveryStatus enum covers sent, delivered, read and failed."""
        assert DeliveryStatus.sent == "sent"
        assert DeliveryStatus.delivered == "delivered"
        assert DeliveryStatus.read == "read"
        assert DeliveryStatus.failed == "failed"


class TestMessageStatus:
    def test_basic(self):
        """MessageStatus stores id, status, timestamp and recipient_id."""
        status = MessageStatus(
            id="wamid.abc123",
            status=DeliveryStatus.delivered,
            timestamp="1700000000",
            recipient_id=RECIPIENT,
        )
        assert status.id == "wamid.abc123"
        assert status.status == DeliveryStatus.delivered
        assert status.timestamp == "1700000000"
        assert status.recipient_id == RECIPIENT

    def test_errors_optional(self):
        """MessageStatus.errors defaults to None or empty when omitted."""
        status = MessageStatus(
            id="wamid.abc123",
            status=DeliveryStatus.sent,
            timestamp="1700000000",
            recipient_id=RECIPIENT,
        )
        assert status.errors == []

    def test_with_errors(self):
        """MessageStatus accepts a list of WebhookError objects."""
        status = MessageStatus(
            id="wamid.abc123",
            status=DeliveryStatus.failed,
            timestamp="1700000000",
            recipient_id=RECIPIENT,
            errors=[{"code": 131047, "title": "Re-engagement message"}],
        )
        assert len(status.errors) == 1
        assert status.errors[0].code == 131047

    def test_requires_id_status_timestamp_recipient(self):
        """MessageStatus raises ValidationError when required fields are missing."""
        with pytest.raises(ValidationError):
            MessageStatus(id="wamid.abc123", status=DeliveryStatus.sent)
