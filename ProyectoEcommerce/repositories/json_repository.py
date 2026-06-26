import json
import uuid
from dataclasses import fields
from pathlib import Path
from typing import Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


class JsonRepository(Generic[T]):
    """Repositorio genérico para persistencia en archivos JSON."""

    def __init__(self, file_path: Path, model_class: Type[T], id_field: str):
        self.file_path = Path(file_path)
        self.model_class = model_class
        self.id_field = id_field
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _read_raw(self) -> List[dict]:
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_raw(self, data: List[dict]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _to_model(self, item: dict) -> T:
        valid_fields = {f.name for f in fields(self.model_class)}
        clean = {k: v for k, v in item.items() if k in valid_fields}
        return self.model_class(**clean)

    def find_all(self) -> List[T]:
        return [self._to_model(item) for item in self._read_raw()]

    def find_by_id(self, item_id: str) -> Optional[T]:
        item_id = str(item_id).strip()
        for item in self._read_raw():
            if str(item.get(self.id_field)) == item_id:
                return self._to_model(item)
        return None

    def exists(self, item_id: str) -> bool:
        return self.find_by_id(item_id) is not None

    def save(self, obj: T) -> T:
        data = self._read_raw()
        obj_dict = obj.to_dict() if hasattr(obj, "to_dict") else obj.__dict__

        if not obj_dict.get(self.id_field):
            obj_dict[self.id_field] = self._generate_id()
            setattr(obj, self.id_field, obj_dict[self.id_field])

        updated = False
        for i, item in enumerate(data):
            if item.get(self.id_field) == obj_dict.get(self.id_field):
                data[i] = obj_dict
                updated = True
                break
        if not updated:
            data.append(obj_dict)
        self._write_raw(data)
        return obj

    def delete(self, item_id: str) -> bool:
        data = self._read_raw()
        new_data = [item for item in data if str(item.get(self.id_field)) != str(item_id)]
        self._write_raw(new_data)
        return len(new_data) != len(data)

    @staticmethod
    def _generate_id() -> str:
        return uuid.uuid4().hex[:10].upper()
