from typing import Optional
from models.usuario import Usuario
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class UsuarioRepository(JsonRepository[Usuario]):
    def __init__(self):
        super().__init__(DATA_DIR / "usuarios.json", Usuario, "id_usuario")

    def find_by_correo(self, correo: str) -> Optional[Usuario]:
        correo = correo.strip().lower()
        for usuario in self.find_all():
            if usuario.correo.lower() == correo:
                return usuario
        return None
