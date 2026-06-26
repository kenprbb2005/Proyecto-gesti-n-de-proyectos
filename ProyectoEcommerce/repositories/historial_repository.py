from typing import List
from models.historial import Historial
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class HistorialRepository(JsonRepository[Historial]):
    def __init__(self):
        super().__init__(DATA_DIR / "historial.json", Historial, "id_historial")

    def find_by_usuario(self, id_usuario: str) -> List[Historial]:
        return [h for h in self.find_all() if h.id_usuario == id_usuario]
