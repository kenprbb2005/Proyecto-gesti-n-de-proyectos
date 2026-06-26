from typing import List, Optional
from models.resena import Resena
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class ResenaRepository(JsonRepository[Resena]):
    def __init__(self):
        super().__init__(DATA_DIR / "resenas.json", Resena, "id_resena")

    def find_by_producto(self, id_producto: str) -> List[Resena]:
        return [r for r in self.find_all() if r.id_producto == id_producto]

    def find_by_usuario_producto(self, id_usuario: str, id_producto: str) -> Optional[Resena]:
        for r in self.find_all():
            if r.id_usuario == id_usuario and r.id_producto == id_producto and r.estado != "Eliminada":
                return r
        return None
