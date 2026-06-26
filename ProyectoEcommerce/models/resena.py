from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Resena(SerializableMixin):
    id_resena: str = ""
    id_usuario: str = ""
    id_producto: str = ""
    calificacion: int = 5
    comentario: str = ""
    estado: str = "Publicada"  # Publicada / Pendiente / Oculta / Eliminada
    fecha: str = field(default_factory=now_iso)
