""" Call validation code """

import logging
import unicodedata
from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

from frictionless import Control
from validata_core.helpers import detect_encoding

log = logging.getLogger(__name__)


class ValidataResource(ABC):
    """A resource to validate: url or uploaded file"""

    def __init__(self, type_):
        self.type = type_

    # TODO: merge with validata_core.helpers.prepare_resource!
    @abstractmethod
    def build_stream_args(self):
        """return (source, option_dict)"""
        pass


class URLValidataResource(ValidataResource):
    """URL resource"""

    def __init__(self, url):
        """Built from URL"""
        super().__init__("url")
        self.url = url
        self.filename = Path(urlparse(url).path).name

    def build_stream_args(self):
        """URL implementation"""
        return (self.url, {"control": Control(detect_encoding=detect_encoding) })


class UploadedFileValidataResource(ValidataResource):
    """Uploaded file resource"""

    def __init__(self, filename, bytes_content):
        """Built from file name and content"""
        super().__init__("file")
        self.filename = filename
        self.content = bytes_content


    def build_stream_args(self):
        """Uploaded file implementation"""

        def detect_format_from_file_extension(filename: str):
            ext = Path(filename).suffix.lower()
            if ext in (".csv", ".tsv", ".ods", ".xls", ".xlsx"):
                return ext[1:]
            return None

        format = detect_format_from_file_extension(self.filename)
        options = { "format": format }
        if format in {'csv', 'tsv'}:
            scheme = 'text'
            encoding = detect_encoding(self.content)
            source = self.content.decode(encoding)
            options["encoding"] = encoding
        else:
            scheme = "filelike"
            source = BytesIO(self.content)
        options["scheme"] = scheme

        return (source, options)


def strip_accents(s):
    """Remove accents from string, used to sort normalized strings"""
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )
