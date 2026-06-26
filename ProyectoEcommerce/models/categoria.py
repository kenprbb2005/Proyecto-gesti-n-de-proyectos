from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Categoria(SerializableMixin):
    id_categoria: str = ""
    nombre: str = ""
    descripcion: str = ""
    estado: str = "Activa"  # Activa / Inactiva
    fecha_creacion: str = field(default_factory=now_iso)
