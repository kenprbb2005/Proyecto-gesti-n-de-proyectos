from dataclasses import dataclass, field
from typing import List, Dict, Any
from models.base import SerializableMixin, now_iso


@dataclass
class ItemCarrito(SerializableMixin):
    id_producto: str = ""
    nombre: str = ""
    cantidad: int = 1
    precio_unitario: float = 0.0

    @property
    def subtotal(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
        }


@dataclass
class Carrito(SerializableMixin):
    id_carrito: str = ""
    id_usuario: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    estado: str = "Activo"  # Activo / Convertido / Cancelado
    fecha_creacion: str = field(default_factory=now_iso)
    fecha_actualizacion: str = field(default_factory=now_iso)
