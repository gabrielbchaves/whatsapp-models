"""Tests for phone number models."""

import pytest
from pydantic import ValidationError

from whatsapp_models.phone_numbers.phone_number import (
    PhoneNumber,
    PhoneNumberList,
    PhoneNumberRegistration,
    QualityRating,
    ThroughputLevel,
)


class TestQualityRating:
    def test_values(self) -> None:
        """QualityRating enum covers GREEN, YELLOW, RED and NA."""
        assert QualityRating.GREEN == "GREEN"
        assert QualityRating.YELLOW == "YELLOW"
        assert QualityRating.RED == "RED"
        assert QualityRating.NA == "NA"


class TestThroughputLevel:
    def test_values(self) -> None:
        """ThroughputLevel enum covers STANDARD, HIGH and NOT_APPLICABLE."""
        assert ThroughputLevel.STANDARD == "STANDARD"
        assert ThroughputLevel.HIGH == "HIGH"
        assert ThroughputLevel.NOT_APPLICABLE == "NOT_APPLICABLE"


class TestPhoneNumber:
    def test_basic(self) -> None:
        """PhoneNumber stores id, display_phone_number and verified_name."""
        pn = PhoneNumber(
            id="pn_id_1",
            display_phone_number="+55 11 99999-9999",
            verified_name="Empresa Teste",
        )
        assert pn.id == "pn_id_1"
        assert pn.display_phone_number == "+55 11 99999-9999"
        assert pn.verified_name == "Empresa Teste"

    def test_optional_fields_default_none(self) -> None:
        """PhoneNumber optional fields default to None when omitted."""
        pn = PhoneNumber(
            id="pn_id_1",
            display_phone_number="+55 11 99999-9999",
            verified_name="Empresa Teste",
        )
        assert pn.quality_rating is None
        assert pn.platform_type is None
        assert pn.throughput is None

    def test_with_quality_rating(self) -> None:
        """PhoneNumber stores quality_rating when provided."""
        pn = PhoneNumber(
            id="pn_id_1",
            display_phone_number="+55 11 99999-9999",
            verified_name="Empresa Teste",
            quality_rating=QualityRating.GREEN,
        )
        assert pn.quality_rating == QualityRating.GREEN

    def test_with_throughput(self) -> None:
        """PhoneNumber stores throughput level when provided."""
        pn = PhoneNumber(
            id="pn_id_1",
            display_phone_number="+55 11 99999-9999",
            verified_name="Empresa Teste",
            throughput=ThroughputLevel.HIGH,
        )
        assert pn.throughput == ThroughputLevel.HIGH

    def test_requires_id_display_verified(self) -> None:
        """PhoneNumber raises ValidationError when required fields are missing."""
        with pytest.raises(ValidationError):
            PhoneNumber.model_validate({"id": "pn_id_1", "display_phone_number": "+55 11 99999-9999"})

    def test_serializes_quality_rating_as_string(self) -> None:
        """PhoneNumber serializes quality_rating as a plain string."""
        pn = PhoneNumber(
            id="pn_id_1",
            display_phone_number="+55 11 99999-9999",
            verified_name="Empresa Teste",
            quality_rating=QualityRating.YELLOW,
        )
        assert pn.model_dump()["quality_rating"] == "YELLOW"


class TestPhoneNumberRegistration:
    def test_basic(self) -> None:
        """PhoneNumberRegistration stores pin for number registration."""
        reg = PhoneNumberRegistration(pin="123456")
        assert reg.pin == "123456"

    def test_requires_pin(self) -> None:
        """PhoneNumberRegistration raises ValidationError when pin is missing."""
        with pytest.raises(ValidationError):
            PhoneNumberRegistration.model_validate({})


class TestPhoneNumberList:
    def test_basic(self) -> None:
        """PhoneNumberList stores a list of PhoneNumber objects."""
        pl = PhoneNumberList.model_validate(
            {
                "data": [
                    {
                        "id": "pn_id_1",
                        "display_phone_number": "+55 11 99999-9999",
                        "verified_name": "Empresa A",
                    },
                    {
                        "id": "pn_id_2",
                        "display_phone_number": "+55 21 88888-8888",
                        "verified_name": "Empresa B",
                    },
                ]
            }
        )
        assert len(pl.data) == 2
        assert pl.data[0].id == "pn_id_1"

    def test_empty_list(self) -> None:
        """PhoneNumberList accepts an empty data list."""
        pl = PhoneNumberList(data=[])
        assert pl.data == []

    def test_paging_optional(self) -> None:
        """PhoneNumberList.paging is optional."""
        pl = PhoneNumberList(data=[])
        assert pl.paging is None
