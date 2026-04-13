"""Tests for WebhookError model."""

import pytest
from pydantic import ValidationError

from whatsapp_models.webhooks.errors import WebhookError


class TestWebhookError:
    def test_basic(self):
        """WebhookError stores code, title, message and error_data."""
        err = WebhookError(
            code=131047,
            title="Re-engagement message",
            message="Message failed to send because more than 24 hours have passed.",
            error_data={"details": "some detail"},
        )
        assert err.code == 131047
        assert err.title == "Re-engagement message"
        assert err.error_data == {"details": "some detail"}

    def test_optional_fields(self):
        """WebhookError can be constructed with only code and title."""
        err = WebhookError(code=131047, title="Some error")
        assert err.message is None
        assert err.error_data is None

    def test_requires_code_and_title(self):
        """WebhookError raises ValidationError when code is missing."""
        with pytest.raises(ValidationError):
            WebhookError(title="Some error")
