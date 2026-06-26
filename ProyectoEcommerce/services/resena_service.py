from typing import List, Optional
from models.resena import Resena
from repositories.resena_repository import ResenaRepository
from services.pedido_service import PedidoService
from services.historial_service import HistorialService
from services.notificacion_service import NotificacionService


class ResenaService:
    ESTADOS_VALIDOS = ["Publicada", "Pendiente", "Oculta", "Eliminada"]

    def __init__(
        self,
        resena_repository: Optional[ResenaRepository] = None,
        pedido_service: Optional[PedidoService] = None,
        historial_service: Optional[HistorialService] = None,
        notificacion_service: Optional[NotificacionService] = None,
    ):
        self.resena_repository = resena_repository or ResenaRepository()
        self.pedido_service = pedido_service or PedidoService()
        self.historial_service = historial_service or HistorialService()
        self.notificacion_service = notificacion_service or NotificacionService()

    def listar_resenas(self) -> List[Resena]:
        return sorted(self.resena_repository.find_all(), key=lambda r: r.fecha, reverse=True)

    def listar_por_producto(self, id_producto: str) -> List[Resena]:
        return [r for r in self.resena_repository.find_by_producto(id_producto) if r.estado == "Publicada"]

    def crear_resena(self, id_usuario: str, id_producto: str, calificacion: int, comentario: str) -> Resena:
        calificacion = int(calificacion)
        if calificacion < 1 or calificacion > 5:
            raise ValueError("La calificación debe estar entre 1 y 5.")
        if len(comentario.strip()) < 5:
            raise ValueError("El comentario debe tener al menos 5 caracteres.")
        if self.resena_repository.find_by_usuario_producto(id_usuario, id_producto):
            raise ValueError("Ya existe una reseña de este usuario para ese producto.")

        # Regla de negocio: solo puede reseñar si el producto aparece en un pedido entregado.
        pedidos = self.pedido_service.listar_por_usuario(id_usuario)
        comprado_entregado = any(
            pedido.estado == "Entregado" and any(item["id_producto"] == id_producto for item in pedido.items)
            for pedido in pedidos
        )
        if not comprado_entregado:
            raise ValueError("Solo puedes reseñar productos comprados y entregados.")

        resena = Resena(id_usuario=id_usuario, id_producto=id_producto, calificacion=calificacion, comentario=comentario.strip(), estado="Publicada")
        resena = self.resena_repository.save(resena)
        self.historial_service.registrar(id_usuario, "Reseña", f"Se publicó una reseña del producto {id_producto}.")
        self.notificacion_service.crear(id_usuario, "Reseña publicada", "Tu reseña fue publicada correctamente.", "Reseña")
        return resena

    def crear_resena_admin(self, id_usuario: str, id_producto: str, calificacion: int, comentario: str, estado: str = "Publicada") -> Resena:
        # Para que el admin pueda cargar datos de prueba sin exigir pedido entregado.
        calificacion = int(calificacion)
        if calificacion < 1 or calificacion > 5:
            raise ValueError("La calificación debe estar entre 1 y 5.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado de la reseña no es válido.")
        resena = Resena(id_usuario=id_usuario, id_producto=id_producto, calificacion=calificacion, comentario=comentario.strip(), estado=estado)
        return self.resena_repository.save(resena)

    def moderar(self, id_resena: str, estado: str) -> Resena:
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado de la reseña no es válido.")
        resena = self.resena_repository.find_by_id(id_resena)
        if not resena:
            raise ValueError("No existe la reseña seleccionada.")
        resena.estado = estado
        return self.resena_repository.save(resena)

    def eliminar_resena(self, id_resena: str) -> bool:
        resena = self.resena_repository.find_by_id(id_resena)
        if not resena:
            raise ValueError("No existe la reseña seleccionada.")
        resena.estado = "Eliminada"
        self.resena_repository.save(resena)
        return True
