import re
from typing import List, Optional
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    ROLES_VALIDOS = ["Administrador", "Cliente", "Vendedor", "Soporte"]
    ESTADOS_VALIDOS = ["Activo", "Inactivo", "Bloqueado"]

    def __init__(self, usuario_repository: Optional[UsuarioRepository] = None):
        self.usuario_repository = usuario_repository or UsuarioRepository()

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuario_repository.find_all()

    def obtener_usuario(self, id_usuario: str) -> Optional[Usuario]:
        return self.usuario_repository.find_by_id(id_usuario)

    def buscar(self, texto: str) -> List[Usuario]:
        texto = texto.strip().lower()
        usuarios = self.listar_usuarios()
        if not texto:
            return usuarios
        return [u for u in usuarios if texto in u.nombre.lower() or texto in u.correo.lower() or texto in u.rol.lower()]

    def registrar_usuario(self, nombre: str, correo: str, contrasena: str, rol: str = "Cliente", estado: str = "Activo") -> Usuario:
        nombre = nombre.strip()
        correo = correo.strip().lower()
        contrasena = contrasena.strip()
        rol = rol or "Cliente"
        estado = estado or "Activo"

        if not nombre:
            raise ValueError("El nombre del usuario es obligatorio.")
        if not self._correo_valido(correo):
            raise ValueError("El correo electrónico no tiene un formato válido.")
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        if rol not in self.ROLES_VALIDOS:
            raise ValueError("El rol indicado no es válido.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado indicado no es válido.")
        if self.usuario_repository.find_by_correo(correo):
            raise ValueError("Ya existe un usuario registrado con ese correo.")

        usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena, rol=rol, estado=estado)
        return self.usuario_repository.save(usuario)

    def actualizar_usuario(self, id_usuario: str, nombre: str, correo: str, rol: str, estado: str, contrasena: str = "") -> Usuario:
        usuario = self._obtener_o_error(id_usuario)
        nombre = nombre.strip()
        correo = correo.strip().lower()
        if not nombre:
            raise ValueError("El nombre del usuario es obligatorio.")
        if not self._correo_valido(correo):
            raise ValueError("El correo electrónico no tiene un formato válido.")
        if rol not in self.ROLES_VALIDOS:
            raise ValueError("El rol indicado no es válido.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado indicado no es válido.")
        otro = self.usuario_repository.find_by_correo(correo)
        if otro and otro.id_usuario != id_usuario:
            raise ValueError("Ese correo ya está registrado por otro usuario.")
        if contrasena and len(contrasena.strip()) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.rol = rol
        usuario.estado = estado
        if contrasena.strip():
            usuario.contrasena = contrasena.strip()
        return self.usuario_repository.save(usuario)

    def cambiar_estado(self, id_usuario: str) -> Usuario:
        usuario = self._obtener_o_error(id_usuario)
        usuario.estado = "Inactivo" if usuario.estado == "Activo" else "Activo"
        return self.usuario_repository.save(usuario)

    def bloquear_usuario(self, id_usuario: str) -> Usuario:
        usuario = self._obtener_o_error(id_usuario)
        usuario.estado = "Bloqueado"
        return self.usuario_repository.save(usuario)

    def eliminar_usuario(self, id_usuario: str) -> bool:
        usuario = self._obtener_o_error(id_usuario)
        if usuario.rol == "Administrador":
            administradores = [u for u in self.listar_usuarios() if u.rol == "Administrador" and u.estado == "Activo"]
            if len(administradores) <= 1:
                raise ValueError("No se puede eliminar el único administrador activo del sistema.")
        return self.usuario_repository.delete(id_usuario)

    def _obtener_o_error(self, id_usuario: str) -> Usuario:
        usuario = self.usuario_repository.find_by_id(id_usuario)
        if not usuario:
            raise ValueError("No existe un usuario con ese ID.")
        return usuario

    @staticmethod
    def _correo_valido(correo: str) -> bool:
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo))
