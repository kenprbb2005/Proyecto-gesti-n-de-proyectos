from typing import List
from models.inventario import InventarioMovimiento
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class InventarioRepository(JsonRepository[InventarioMovimiento]):
    def __init__(self):
        super().__init__(DATA_DIR / "inventario.json", InventarioMovimiento, "id_movimiento")

    def find_by_producto(self, id_producto: str) -> List[InventarioMovimiento]:
        return [m for m in self.find_all() if m.id_producto == id_producto]
