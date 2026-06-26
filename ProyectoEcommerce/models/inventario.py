from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class InventarioMovimiento(SerializableMixin):
    id_movimiento: str = ""
    id_producto: str = ""
    tipo: str = "Entrada"  # Entrada / Salida / Ajuste
    cantidad: int = 0
    motivo: str = ""
    stock_anterior: int = 0
    stock_nuevo: int = 0
    fecha: str = field(default_factory=now_iso)
