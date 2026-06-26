from dataclasses import dataclass, field
from models.base import SerializableMixin, now_iso


@dataclass
class Usuario(SerializableMixin):
    id_usuario: str = ""
    nombre: str = ""
    correo: str = ""
    contrasena: str = ""
    rol: str = "Cliente"  # Administrador / Cliente / Vendedor / Soporte
    estado: str = "Activo"  # Activo / Inactivo / Bloqueado
    fecha_registro: str = field(default_factory=now_iso)
