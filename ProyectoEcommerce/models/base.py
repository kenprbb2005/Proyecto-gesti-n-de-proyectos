from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class SerializableMixin:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
