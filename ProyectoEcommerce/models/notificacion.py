from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Notificacion(SerializableMixin):
    id_notificacion: str = ""
    id_usuario: str = ""
    titulo: str = ""
    mensaje: str = ""
    tipo: str = "Sistema"  # Sistema / Pedido / Pago / Inventario / Reseña
    leida: bool = False
    fecha: str = field(default_factory=now_iso)
