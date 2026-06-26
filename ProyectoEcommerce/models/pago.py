from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Pago(SerializableMixin):
    id_pago: str = ""
    id_pedido: str = ""
    id_usuario: str = ""
    metodo: str = "Tarjeta"  # Tarjeta / SINPE Móvil / Transferencia / Efectivo
    monto: float = 0.0
    estado: str = "Pendiente"  # Pendiente / Aprobado / Rechazado / Anulado
    referencia: str = ""
    mensaje: str = ""
    fecha_pago: str = field(default_factory=now_iso)
