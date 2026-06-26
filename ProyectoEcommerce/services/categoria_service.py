from typing import List, Optional
from models.categoria import Categoria
from repositories.categoria_repository import CategoriaRepository
from repositories.producto_repository import ProductoRepository


class CategoriaService:
    ESTADOS_VALIDOS = ["Activa", "Inactiva"]

    def __init__(self, categoria_repository: Optional[CategoriaRepository] = None, producto_repository: Optional[ProductoRepository] = None):
        self.categoria_repository = categoria_repository or CategoriaRepository()
        self.producto_repository = producto_repository or ProductoRepository()

    def listar(self, solo_activas: bool = False) -> List[Categoria]:
        categorias = self.categoria_repository.find_all()
        if solo_activas:
            categorias = [c for c in categorias if c.estado == "Activa"]
        return categorias

    def obtener(self, id_categoria: str) -> Optional[Categoria]:
        return self.categoria_repository.find_by_id(id_categoria)

    def buscar(self, texto: str) -> List[Categoria]:
        texto = texto.strip().lower()
        categorias = self.listar()
        if not texto:
            return categorias
        return [c for c in categorias if texto in c.nombre.lower() or texto in c.descripcion.lower()]

    def crear(self, nombre: str, descripcion: str = "", estado: str = "Activa") -> Categoria:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado de la categoría no es válido.")
        if self.categoria_repository.find_by_nombre(nombre):
            raise ValueError("Ya existe una categoría con ese nombre.")
        return self.categoria_repository.save(Categoria(nombre=nombre, descripcion=descripcion.strip(), estado=estado))

    def actualizar(self, id_categoria: str, nombre: str, descripcion: str, estado: str) -> Categoria:
        categoria = self._obtener_o_error(id_categoria)
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado de la categoría no es válido.")
        otra = self.categoria_repository.find_by_nombre(nombre)
        if otra and otra.id_categoria != id_categoria:
            raise ValueError("Ya existe otra categoría con ese nombre.")
        categoria.nombre = nombre
        categoria.descripcion = descripcion.strip()
        categoria.estado = estado
        return self.categoria_repository.save(categoria)

    def eliminar(self, id_categoria: str) -> bool:
        categoria = self._obtener_o_error(id_categoria)
        productos = self.producto_repository.find_by_categoria(id_categoria)
        if productos:
            raise ValueError("No se puede eliminar una categoría con productos asociados. Desactívala mejor.")
        return self.categoria_repository.delete(categoria.id_categoria)

    def _obtener_o_error(self, id_categoria: str) -> Categoria:
        categoria = self.categoria_repository.find_by_id(id_categoria)
        if not categoria:
            raise ValueError("No existe una categoría con ese ID.")
        return categoria
