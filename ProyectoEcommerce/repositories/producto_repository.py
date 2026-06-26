from typing import List
from models.producto import Producto
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class ProductoRepository(JsonRepository[Producto]):
    def __init__(self):
        super().__init__(DATA_DIR / "productos.json", Producto, "id_producto")

    def find_by_categoria(self, id_categoria: str) -> List[Producto]:
        return [p for p in self.find_all() if p.id_categoria == id_categoria]
