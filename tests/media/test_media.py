"""Tests for media upload and reference models."""

import pytest
from pydantic import ValidationError

from whatsapp_models.media.media import MediaObject, MediaUploadResponse


class TestMediaUploadResponse:
    def test_basic(self):
        """MediaUploadResponse stores the media id returned by the upload API."""
        resp = MediaUploadResponse(id="media_id_abc")
        assert resp.id == "media_id_abc"

    def test_requires_id(self):
        """MediaUploadResponse raises ValidationError when id is missing."""
        with pytest.raises(ValidationError):
            MediaUploadResponse()


class TestMediaObject:
    def test_with_id(self):
        """MediaObject accepts a media ID reference."""
        obj = MediaObject(id="media_id_abc")
        assert obj.id == "media_id_abc"
        assert obj.link is None

    def test_with_link(self):
        """MediaObject accepts a hosted media URL."""
        obj = MediaObject(link="https://example.com/file.pdf")
        assert obj.link == "https://example.com/file.pdf"
        assert obj.id is None

    def test_requires_id_or_link(self):
        """MediaObject raises ValidationError when neither id nor link is provided."""
        with pytest.raises(ValidationError):
            MediaObject()

    def test_caption_optional(self):
        """MediaObject.caption is optional."""
        obj = MediaObject(id="media_id_abc")
        assert obj.caption is None

    def test_filename_optional(self):
        """MediaObject.filename is optional."""
        obj = MediaObject(id="media_id_abc")
        assert obj.filename is None

    def test_with_caption_and_filename(self):
        """MediaObject stores optional caption and filename."""
        obj = MediaObject(id="media_id_abc", caption="Relatório", filename="relatorio.pdf")
        assert obj.caption == "Relatório"
        assert obj.filename == "relatorio.pdf"
