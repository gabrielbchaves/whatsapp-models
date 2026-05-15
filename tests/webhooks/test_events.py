"""Tests for webhook event models: AccountUpdateEvent and HistoryEvent."""

import pytest
from pydantic import ValidationError

from whatsapp_models.webhooks.events import AccountUpdateEvent, HistoryEvent


class TestAccountUpdateEvent:
    def test_basic(self) -> None:
        """AccountUpdateEvent stores phone_number and event type."""
        event = AccountUpdateEvent(
            phone_number="15550001234",
            event="ACCOUNT_UPDATE",
        )
        assert event.phone_number == "15550001234"
        assert event.event == "ACCOUNT_UPDATE"

    def test_ban_info_optional(self) -> None:
        """AccountUpdateEvent.ban_info is optional."""
        event = AccountUpdateEvent(phone_number="15550001234", event="ACCOUNT_UPDATE")
        assert event.ban_info is None

    def test_with_ban_info(self) -> None:
        """AccountUpdateEvent stores ban_info when provided."""
        event = AccountUpdateEvent(
            phone_number="15550001234",
            event="ACCOUNT_UPDATE",
            ban_info={"waba_ban_state": "SCHEDULE_FOR_DISABLE", "waba_ban_date": "2024-01-01"},
        )
        assert event.ban_info is not None

    def test_requires_phone_and_event(self) -> None:
        """AccountUpdateEvent raises ValidationError when phone_number is missing."""
        with pytest.raises(ValidationError):
            AccountUpdateEvent.model_validate({"event": "ACCOUNT_UPDATE"})


class TestHistoryEvent:
    def test_basic(self) -> None:
        """HistoryEvent stores type and id."""
        event = HistoryEvent(type="phone_number_history", id="pn_id_1")
        assert event.type == "phone_number_history"
        assert event.id == "pn_id_1"

    def test_requires_type(self) -> None:
        """HistoryEvent raises ValidationError when type is missing."""
        with pytest.raises(ValidationError):
            HistoryEvent.model_validate({"id": "pn_id_1"})
