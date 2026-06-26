from typing import Optional
from models.categoria import Categoria
from repositories.json_repository import JsonRepository
from repositories.paths import DATA_DIR


class CategoriaRepository(JsonRepository[Categoria]):
    def __init__(self):
        super().__init__(DATA_DIR / "categorias.json", Categoria, "id_categoria")

    def find_by_nombre(self, nombre: str) -> Optional[Categoria]:
        nombre = nombre.strip().lower()
        for categoria in self.find_all():
            if categoria.nombre.lower() == nombre:
                return categoria
        return None
