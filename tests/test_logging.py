import logging

import pytest

from software360.common.logging import configure_logging


def test_configure_logging_uses_structured_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configured: dict[str, object] = {}

    def fake_basic_config(**kwargs: object) -> None:
        configured.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

    configure_logging(logging.DEBUG)

    assert configured == {
        "level": logging.DEBUG,
        "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
    }
