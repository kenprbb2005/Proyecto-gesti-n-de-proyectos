from typing import List, Optional
from models.notificacion import Notificacion
from repositories.notificacion_repository import NotificacionRepository



class NotificacionService:
    def __init__(self, notificacion_repository: Optional[NotificacionRepository] = None):
        self.notificacion_repository = notificacion_repository or NotificacionRepository()

    def crear(self, id_usuario: str, titulo: str, mensaje: str, tipo: str = "Sistema") -> Notificacion:
        if not id_usuario:
            raise ValueError("La notificación debe estar asociada a un usuario.")
        if not titulo.strip():
            raise ValueError("El título de la notificación es obligatorio.")
        notificacion = Notificacion(
            id_usuario=id_usuario,
            titulo=titulo.strip(),
            mensaje=mensaje.strip(),
            tipo=tipo,
        )
        return self.notificacion_repository.save(notificacion)

    def listar(self) -> List[Notificacion]:
        return sorted(self.notificacion_repository.find_all(), key=lambda n: n.fecha, reverse=True)

    def listar_por_usuario(self, id_usuario: str, solo_no_leidas: bool = False) -> List[Notificacion]:
        notificaciones = self.notificacion_repository.find_by_usuario(id_usuario)
        if solo_no_leidas:
            notificaciones = [n for n in notificaciones if not n.leida]
        return sorted(notificaciones, key=lambda n: n.fecha, reverse=True)

    def marcar_leida(self, id_notificacion: str) -> Notificacion:
        notificacion = self.notificacion_repository.find_by_id(id_notificacion)
        if not notificacion:
            raise ValueError("No existe la notificación seleccionada.")
        notificacion.leida = True
        return self.notificacion_repository.save(notificacion)

    def eliminar(self, id_notificacion: str) -> bool:
        return self.notificacion_repository.delete(id_notificacion)
