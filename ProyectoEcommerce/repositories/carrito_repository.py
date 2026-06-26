from typing import Optional
from models.carrito import Carrito
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class CarritoRepository(JsonRepository[Carrito]):
    def __init__(self):
        super().__init__(DATA_DIR / "carritos.json", Carrito, "id_carrito")

    def find_activo_by_usuario(self, id_usuario: str) -> Optional[Carrito]:
        for carrito in self.find_all():
            if carrito.id_usuario == id_usuario and carrito.estado == "Activo":
                return carrito
        return None
