from typing import List
from models.pedido import Pedido
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class PedidoRepository(JsonRepository[Pedido]):
    def __init__(self):
        super().__init__(DATA_DIR / "pedidos.json", Pedido, "id_pedido")

    def find_by_usuario(self, id_usuario: str) -> List[Pedido]:
        return [p for p in self.find_all() if p.id_usuario == id_usuario]
