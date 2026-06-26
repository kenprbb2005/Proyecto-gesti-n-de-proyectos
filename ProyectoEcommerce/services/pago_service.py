from typing import List, Optional
from models.pago import Pago
from repositories.pago_repository import PagoRepository
from services.pedido_service import PedidoService
from services.historial_service import HistorialService
from services.notificacion_service import NotificacionService


class PagoService:
    METODOS_VALIDOS = ["Tarjeta", "SINPE Móvil", "Transferencia", "Efectivo"]

    def __init__(
        self,
        pago_repository: Optional[PagoRepository] = None,
        pedido_service: Optional[PedidoService] = None,
        historial_service: Optional[HistorialService] = None,
        notificacion_service: Optional[NotificacionService] = None,
    ):
        self.pago_repository = pago_repository or PagoRepository()
        self.pedido_service = pedido_service or PedidoService()
        self.historial_service = historial_service or HistorialService()
        self.notificacion_service = notificacion_service or NotificacionService()

    def listar_pagos(self) -> List[Pago]:
        return sorted(self.pago_repository.find_all(), key=lambda p: p.fecha_pago, reverse=True)

    def buscar_por_pedido(self, id_pedido: str) -> List[Pago]:
        return self.pago_repository.find_by_pedido(id_pedido)

    def procesar_pago(self, id_pedido: str, metodo: str, monto: float, referencia: str = "") -> Pago:
        pedido = self.pedido_service.obtener(id_pedido)
        if not pedido:
            raise ValueError("El pedido no existe.")
        if pedido.estado in ["Cancelado", "Entregado"]:
            raise ValueError("No se puede pagar un pedido cancelado o entregado.")
        if self.pago_repository.find_aprobado_by_pedido(id_pedido):
            raise ValueError("Este pedido ya tiene un pago aprobado.")
        if metodo not in self.METODOS_VALIDOS:
            raise ValueError("El método de pago no es válido.")
        monto = float(monto)
        if round(monto, 2) != round(float(pedido.total), 2):
            raise ValueError("El monto pagado debe ser exactamente igual al total del pedido.")

        estado = "Aprobado"
        mensaje = "Pago simulado aprobado correctamente."
        # Simulación simple: referencias terminadas en 0000 se rechazan.
        if referencia.strip().endswith("0000"):
            estado = "Rechazado"
            mensaje = "Pago simulado rechazado por referencia inválida."

        pago = Pago(
            id_pedido=id_pedido,
            id_usuario=pedido.id_usuario,
            metodo=metodo,
            monto=monto,
            estado=estado,
            referencia=referencia.strip(),
            mensaje=mensaje,
        )
        pago = self.pago_repository.save(pago)
        if estado == "Aprobado":
            self.pedido_service.cambiar_estado(id_pedido, "Pagado")
        self.historial_service.registrar(pedido.id_usuario, "Pago", f"Pago {estado.lower()} para el pedido {id_pedido}.", id_pedido)
        self.notificacion_service.crear(pedido.id_usuario, f"Pago {estado.lower()}", mensaje, "Pago")
        return pago

    def anular_pago(self, id_pago: str) -> Pago:
        pago = self.pago_repository.find_by_id(id_pago)
        if not pago:
            raise ValueError("No existe el pago seleccionado.")
        if pago.estado != "Aprobado":
            raise ValueError("Solo se pueden anular pagos aprobados.")
        pago.estado = "Anulado"
        pago.mensaje = "Pago anulado administrativamente."
        pago = self.pago_repository.save(pago)
        self.historial_service.registrar(pago.id_usuario, "Pago anulado", f"Se anuló el pago {pago.id_pago}.", pago.id_pedido)
        return pago

    def eliminar_pago(self, id_pago: str) -> bool:
        pago = self.pago_repository.find_by_id(id_pago)
        if pago and pago.estado == "Aprobado":
            raise ValueError("No se puede eliminar un pago aprobado. Anúlalo primero.")
        return self.pago_repository.delete(id_pago)
