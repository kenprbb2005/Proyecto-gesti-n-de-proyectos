from typing import Optional
from models.usuario import Usuario
from services.usuario_service import UsuarioService


class AuthService:
    def __init__(self, usuario_service: Optional[UsuarioService] = None):
        self.usuario_service = usuario_service or UsuarioService()

    def login(self, correo: str, contrasena: str) -> Usuario:
        correo = correo.strip().lower()
        usuario = self.usuario_service.usuario_repository.find_by_correo(correo)
        if not usuario or usuario.contrasena != contrasena:
            raise ValueError("Correo o contraseña incorrectos.")
        if usuario.estado == "Bloqueado":
            raise ValueError("La cuenta está bloqueada. Contacta al administrador.")
        if usuario.estado != "Activo":
            raise ValueError("La cuenta no está activa.")
        return usuario

    def registro_cliente(self, nombre: str, correo: str, contrasena: str) -> Usuario:
        return self.usuario_service.registrar_usuario(nombre, correo, contrasena, rol="Cliente", estado="Activo")

    def recuperar_contrasena(self, correo: str) -> str:
        usuario = self.usuario_service.usuario_repository.find_by_correo(correo.strip().lower())
        if not usuario:
            raise ValueError("No existe una cuenta con ese correo.")
        return f"Recuperación simulada enviada a {usuario.correo}. Contraseña actual: {usuario.contrasena}"
