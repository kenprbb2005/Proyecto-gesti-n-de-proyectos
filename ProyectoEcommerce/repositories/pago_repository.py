from typing import List, Optional
from models.pago import Pago
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class PagoRepository(JsonRepository[Pago]):
    def __init__(self):
        super().__init__(DATA_DIR / "pagos.json", Pago, "id_pago")

    def find_by_pedido(self, id_pedido: str) -> List[Pago]:
        return [p for p in self.find_all() if p.id_pedido == id_pedido]

    def find_aprobado_by_pedido(self, id_pedido: str) -> Optional[Pago]:
        for pago in self.find_by_pedido(id_pedido):
            if pago.estado == "Aprobado":
                return pago
        return None
