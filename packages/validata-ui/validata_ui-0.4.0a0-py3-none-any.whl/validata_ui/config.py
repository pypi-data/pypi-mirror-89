import json
import logging
import os
import sys
from pathlib import Path

import requests
import toml
from dotenv import load_dotenv

log = logging.getLogger(__name__)

load_dotenv()


def without_trailing_slash(url):
    return url[:-1] if url.endswith("/") else url


LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
numeric_log_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_log_level, int):
    log.error("Invalid log level: {}".format(LOG_LEVEL))
logging.basicConfig(
    format="%(levelname)s:%(name)s:%(message)s",
    level=numeric_log_level,
    stream=sys.stderr,  # script outputs data
)

SECRET_KEY = os.environ.get("SECRET_KEY") or None

SHIELDS_IO_BASE_URL = os.environ.get("SHIELDS_IO_BASE_URL") or None
if SHIELDS_IO_BASE_URL:
    SHIELDS_IO_BASE_URL = without_trailing_slash(SHIELDS_IO_BASE_URL)

HOMEPAGE_CONFIG_FILE = os.environ.get("HOMEPAGE_CONFIG_FILE") or None
HOMEPAGE_CONFIG = None
if HOMEPAGE_CONFIG_FILE:
    HOMEPAGE_CONFIG_FILE = Path(HOMEPAGE_CONFIG_FILE)
    with HOMEPAGE_CONFIG_FILE.open() as fd:
        try:
            HOMEPAGE_CONFIG = json.load(fd)
        except ValueError as exc:
            raise ValueError(
                f"Could not load homepage config JSON file {HOMEPAGE_CONFIG_FILE}"
            ) from exc

MATOMO_BASE_URL = os.getenv("MATOMO_BASE_URL") or None
if MATOMO_BASE_URL:
    MATOMO_BASE_URL = without_trailing_slash(MATOMO_BASE_URL)
MATOMO_SITE_ID = os.getenv("MATOMO_SITE_ID") or None
if MATOMO_SITE_ID:
    MATOMO_SITE_ID = int(MATOMO_SITE_ID)

SENTRY_DSN = os.environ.get("SENTRY_DSN")
