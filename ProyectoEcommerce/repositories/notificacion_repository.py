from typing import List
from models.notificacion import Notificacion
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class NotificacionRepository(JsonRepository[Notificacion]):
    def __init__(self):
        super().__init__(DATA_DIR / "notificaciones.json", Notificacion, "id_notificacion")

    def find_by_usuario(self, id_usuario: str) -> List[Notificacion]:
        return [n for n in self.find_all() if n.id_usuario == id_usuario]
