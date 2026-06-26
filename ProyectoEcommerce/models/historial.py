from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Historial(SerializableMixin):
    id_historial: str = ""
    id_usuario: str = ""
    id_pedido: str = ""
    accion: str = ""
    descripcion: str = ""
    fecha: str = field(default_factory=now_iso)
