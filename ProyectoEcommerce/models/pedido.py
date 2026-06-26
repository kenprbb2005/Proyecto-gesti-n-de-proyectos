from dataclasses import dataclass, field
from typing import List, Dict, Any
from models.base import SerializableMixin, now_iso


@dataclass
class Pedido(SerializableMixin):
    id_pedido: str = ""
    id_usuario: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    subtotal: float = 0.0
    impuesto: float = 0.0
    envio: float = 0.0
    total: float = 0.0
    canton_envio: str = ""
    direccion_envio: str = ""
    estado: str = "Pendiente"  # Pendiente / Pagado / Preparando / Enviado / Entregado / Cancelado
    fecha_creacion: str = field(default_factory=now_iso)
    fecha_actualizacion: str = field(default_factory=now_iso)
