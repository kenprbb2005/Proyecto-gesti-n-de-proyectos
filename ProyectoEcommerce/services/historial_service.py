from typing import List, Optional
from models.historial import Historial
from repositories.historial_repository import HistorialRepository


class HistorialService:
    def __init__(self, historial_repository: Optional[HistorialRepository] = None):
        self.historial_repository = historial_repository or HistorialRepository()

    def registrar(self, id_usuario: str, accion: str, descripcion: str, id_pedido: str = "") -> Historial:
        historial = Historial(
            id_usuario=id_usuario,
            id_pedido=id_pedido,
            accion=accion.strip(),
            descripcion=descripcion.strip(),
        )
        return self.historial_repository.save(historial)

    def listar(self) -> List[Historial]:
        return sorted(self.historial_repository.find_all(), key=lambda h: h.fecha, reverse=True)

    def listar_por_usuario(self, id_usuario: str) -> List[Historial]:
        return sorted(self.historial_repository.find_by_usuario(id_usuario), key=lambda h: h.fecha, reverse=True)

    def eliminar(self, id_historial: str) -> bool:
        return self.historial_repository.delete(id_historial)
