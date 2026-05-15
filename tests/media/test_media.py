"""Tests for media upload and reference models."""

import pytest
from pydantic import ValidationError

from whatsapp_models.media.media import MediaObject, MediaUploadResponse


class TestMediaUploadResponse:
    def test_basic(self) -> None:
        """MediaUploadResponse stores the media id returned by the upload API."""
        resp = MediaUploadResponse(id="media_id_abc")
        assert resp.id == "media_id_abc"

    def test_requires_id(self) -> None:
        """MediaUploadResponse raises ValidationError when id is missing."""
        with pytest.raises(ValidationError):
            MediaUploadResponse.model_validate({})


class TestMediaObject:
    def test_with_id(self) -> None:
        """MediaObject accepts a media ID reference."""
        obj = MediaObject(id="media_id_abc")
        assert obj.id == "media_id_abc"
        assert obj.link is None

    def test_with_link(self) -> None:
        """MediaObject accepts a hosted media URL."""
        obj = MediaObject(link="https://example.com/file.pdf")
        assert obj.link == "https://example.com/file.pdf"
        assert obj.id is None

    def test_requires_id_or_link(self) -> None:
        """MediaObject raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            MediaObject.model_validate({})

    def test_caption_optional(self) -> None:
        """MediaObject.caption is optional."""
        obj = MediaObject(id="media_id_abc")
        assert obj.caption is None

    def test_filename_optional(self) -> None:
        """MediaObject.filename is optional."""
        obj = MediaObject(id="media_id_abc")
        assert obj.filename is None

    def test_with_caption_and_filename(self) -> None:
        """MediaObject stores optional caption and filename."""
        obj = MediaObject(id="media_id_abc", caption="Relatório", filename="relatorio.pdf")
        assert obj.caption == "Relatório"
        assert obj.filename == "relatorio.pdf"
