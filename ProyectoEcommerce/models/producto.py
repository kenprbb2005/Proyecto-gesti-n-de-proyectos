from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Producto(SerializableMixin):
    id_producto: str = ""
    nombre: str = ""
    id_categoria: str = ""
    categoria: str = ""
    marca: str = ""
    precio: float = 0.0
    stock: int = 0
    stock_minimo: int = 5
    descripcion: str = ""
    estado: str = "Disponible"  # Disponible / Agotado / Inactivo
    fecha_creacion: str = field(default_factory=now_iso)
