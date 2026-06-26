from typing import List, Optional
from models.inventario import InventarioMovimiento
from repositories.inventario_repository import InventarioRepository
from services.producto_service import ProductoService




class InventarioService:
    TIPOS_VALIDOS = ["Entrada", "Salida", "Ajuste"]

    def __init__(self, inventario_repository: Optional[InventarioRepository] = None, producto_service: Optional[ProductoService] = None):
        self.inventario_repository = inventario_repository or InventarioRepository()
        self.producto_service = producto_service or ProductoService()

    def listar_movimientos(self) -> List[InventarioMovimiento]:
        return sorted(self.inventario_repository.find_all(), key=lambda m: m.fecha, reverse=True)

    def registrar_movimiento(self, id_producto: str, tipo: str, cantidad: int, motivo: str) -> InventarioMovimiento:
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError("El tipo de movimiento no es válido.")
        producto = self.producto_service.obtener_producto(id_producto)
        if not producto:
            raise ValueError("El producto indicado no existe.")
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        stock_anterior = producto.stock
        if tipo == "Entrada":
            producto = self.producto_service.aumentar_stock(id_producto, cantidad)
        elif tipo == "Salida":
            producto = self.producto_service.descontar_stock(id_producto, cantidad)
        else:
            # Ajuste: la cantidad representa el nuevo stock final.
            if cantidad < 0:
                raise ValueError("El ajuste no puede dejar stock negativo.")
            producto.stock = cantidad
            producto.estado = "Agotado" if producto.stock == 0 else "Disponible"
            self.producto_service.producto_repository.save(producto)
        movimiento = InventarioMovimiento(
            id_producto=id_producto,
            tipo=tipo,
            cantidad=cantidad,
            motivo=motivo.strip(),
            stock_anterior=stock_anterior,
            stock_nuevo=producto.stock,
        )
        return self.inventario_repository.save(movimiento)

    def eliminar_movimiento(self, id_movimiento: str) -> bool:
        return self.inventario_repository.delete(id_movimiento)
