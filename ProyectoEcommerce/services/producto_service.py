from typing import List, Optional
from models.producto import Producto
from repositories.producto_repository import ProductoRepository
from repositories.categoria_repository import CategoriaRepository


class ProductoService:
    ESTADOS_VALIDOS = ["Disponible", "Agotado", "Inactivo"]

    def __init__(self, producto_repository: Optional[ProductoRepository] = None, categoria_repository: Optional[CategoriaRepository] = None):
        self.producto_repository = producto_repository or ProductoRepository()
        self.categoria_repository = categoria_repository or CategoriaRepository()

    def listar_productos(self, solo_disponibles: bool = False) -> List[Producto]:
        productos = self.producto_repository.find_all()
        if solo_disponibles:
            productos = [p for p in productos if p.estado == "Disponible" and p.stock > 0]
        return productos

    def obtener_producto(self, id_producto: str) -> Optional[Producto]:
        return self.producto_repository.find_by_id(id_producto)

    def buscar_productos(self, texto: str = "", categoria: str = "Todas", marca: str = "Todas", precio_maximo: Optional[float] = None) -> List[Producto]:
        productos = self.listar_productos()
        texto = texto.strip().lower()
        if texto:
            productos = [p for p in productos if texto in p.nombre.lower() or texto in p.descripcion.lower()]
        if categoria and categoria != "Todas":
            productos = [p for p in productos if p.categoria.lower() == categoria.lower() or p.id_categoria == categoria]
        if marca and marca != "Todas":
            productos = [p for p in productos if p.marca.lower() == marca.lower()]
        if precio_maximo is not None:
            productos = [p for p in productos if p.precio <= float(precio_maximo)]
        return productos

    def crear_producto(self, nombre: str, id_categoria: str, marca: str, precio: float, stock: int, stock_minimo: int, descripcion: str = "", estado: str = "Disponible") -> Producto:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del producto es obligatorio.")
        categoria = self.categoria_repository.find_by_id(id_categoria)
        if not categoria or categoria.estado != "Activa":
            raise ValueError("Debes seleccionar una categoría activa.")
        precio = float(precio)
        stock = int(stock)
        stock_minimo = int(stock_minimo)
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado del producto no es válido.")
        if stock == 0:
            estado = "Agotado"
        producto = Producto(
            nombre=nombre,
            id_categoria=id_categoria,
            categoria=categoria.nombre,
            marca=marca.strip(),
            precio=precio,
            stock=stock,
            stock_minimo=stock_minimo,
            descripcion=descripcion.strip(),
            estado=estado,
        )
        return self.producto_repository.save(producto)

    def actualizar_producto(self, id_producto: str, nombre: str, id_categoria: str, marca: str, precio: float, stock: int, stock_minimo: int, descripcion: str, estado: str) -> Producto:
        producto = self._obtener_o_error(id_producto)
        categoria = self.categoria_repository.find_by_id(id_categoria)
        if not categoria or categoria.estado != "Activa":
            raise ValueError("Debes seleccionar una categoría activa.")
        if not nombre.strip():
            raise ValueError("El nombre del producto es obligatorio.")
        precio = float(precio)
        stock = int(stock)
        stock_minimo = int(stock_minimo)
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado del producto no es válido.")
        if stock == 0:
            estado = "Agotado"
        producto.nombre = nombre.strip()
        producto.id_categoria = id_categoria
        producto.categoria = categoria.nombre
        producto.marca = marca.strip()
        producto.precio = precio
        producto.stock = stock
        producto.stock_minimo = stock_minimo
        producto.descripcion = descripcion.strip()
        producto.estado = estado
        return self.producto_repository.save(producto)

    def descontar_stock(self, id_producto: str, cantidad: int) -> Producto:
        producto = self._obtener_o_error(id_producto)
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if producto.estado != "Disponible":
            raise ValueError("El producto no está disponible.")
        if producto.stock < cantidad:
            raise ValueError("No hay stock suficiente.")
        producto.stock -= cantidad
        if producto.stock == 0:
            producto.estado = "Agotado"
        return self.producto_repository.save(producto)

    def aumentar_stock(self, id_producto: str, cantidad: int) -> Producto:
        producto = self._obtener_o_error(id_producto)
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        producto.stock += cantidad
        if producto.stock > 0 and producto.estado == "Agotado":
            producto.estado = "Disponible"
        return self.producto_repository.save(producto)

    def eliminar_producto(self, id_producto: str) -> bool:
        return self.producto_repository.delete(id_producto)

    def productos_bajo_stock(self) -> List[Producto]:
        return [p for p in self.listar_productos() if p.stock <= p.stock_minimo and p.estado != "Inactivo"]

    def _obtener_o_error(self, id_producto: str) -> Producto:
        producto = self.producto_repository.find_by_id(id_producto)
        if not producto:
            raise ValueError("No existe un producto con ese ID.")
        return producto
