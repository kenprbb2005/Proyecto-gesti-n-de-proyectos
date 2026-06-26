from copy import deepcopy
from typing import List, Optional

from models.carrito import Carrito
from models.base import now_iso
from repositories.carrito_repository import CarritoRepository
from services.producto_service import ProductoService


class CarritoService:
    """Reglas de negocio del carrito de compras.

    El carrito permite tener varios productos agregados, pero no todos tienen que
    comprarse en la misma operación. Cada item tiene el campo `seleccionado`:
    - True: se incluye en el pedido/compra.
    - False: queda guardado en el carrito para comprarlo después.
    """

    def __init__(
        self,
        carrito_repository: Optional[CarritoRepository] = None,
        producto_service: Optional[ProductoService] = None,
    ):
        self.carrito_repository = carrito_repository or CarritoRepository()
        self.producto_service = producto_service or ProductoService()

    def obtener_carrito_activo(self, id_usuario: str) -> Carrito:
        carrito = self.carrito_repository.find_activo_by_usuario(id_usuario)
        if not carrito:
            return self.carrito_repository.save(Carrito(id_usuario=id_usuario))
        return self._normalizar_y_guardar(carrito)

    def agregar_producto(self, id_usuario: str, id_producto: str, cantidad: int = 1) -> Carrito:
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        producto = self.producto_service.obtener_producto(id_producto)
        if not producto:
            raise ValueError("El producto no existe.")
        if producto.estado != "Disponible" or producto.stock <= 0:
            raise ValueError("El producto no está disponible.")

        carrito = self.obtener_carrito_activo(id_usuario)
        items = list(carrito.items)
        existente = None

        for item in items:
            if item["id_producto"] == id_producto:
                existente = item
                break

        cantidad_actual = int(existente.get("cantidad", 0)) if existente else 0
        if cantidad_actual + cantidad > producto.stock:
            raise ValueError("No puedes agregar más unidades que el stock disponible.")

        if existente:
            existente["cantidad"] = cantidad_actual + cantidad
            existente["precio_unitario"] = float(producto.precio)
            existente["nombre"] = producto.nombre
            existente["subtotal"] = round(existente["cantidad"] * existente["precio_unitario"], 2)
            existente["seleccionado"] = True
        else:
            items.append({
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "cantidad": cantidad,
                "precio_unitario": float(producto.precio),
                "subtotal": round(cantidad * float(producto.precio), 2),
                "seleccionado": True,
            })

        carrito.items = items
        carrito.estado = "Activo"
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def actualizar_cantidad(self, id_usuario: str, id_producto: str, cantidad: int) -> Carrito:
        cantidad = int(cantidad)
        carrito = self.obtener_carrito_activo(id_usuario)
        producto = self.producto_service.obtener_producto(id_producto)

        if not producto:
            raise ValueError("El producto no existe.")
        if cantidad <= 0:
            return self.eliminar_producto(id_usuario, id_producto)
        if cantidad > producto.stock:
            raise ValueError("La cantidad supera el stock disponible.")

        encontrado = False
        for item in carrito.items:
            if item["id_producto"] == id_producto:
                item["cantidad"] = cantidad
                item["precio_unitario"] = float(producto.precio)
                item["nombre"] = producto.nombre
                item["subtotal"] = round(cantidad * item["precio_unitario"], 2)
                encontrado = True
                break

        if not encontrado:
            raise ValueError("El producto no está en el carrito.")

        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def seleccionar_producto(self, id_usuario: str, id_producto: str, seleccionado: bool) -> Carrito:
        carrito = self.obtener_carrito_activo(id_usuario)
        encontrado = False

        for item in carrito.items:
            if item["id_producto"] == id_producto:
                item["seleccionado"] = bool(seleccionado)
                encontrado = True
                break

        if not encontrado:
            raise ValueError("El producto no está en el carrito.")

        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def alternar_seleccion_producto(self, id_usuario: str, id_producto: str) -> Carrito:
        carrito = self.obtener_carrito_activo(id_usuario)
        encontrado = False

        for item in carrito.items:
            if item["id_producto"] == id_producto:
                item["seleccionado"] = not bool(item.get("seleccionado", True))
                encontrado = True
                break

        if not encontrado:
            raise ValueError("El producto no está en el carrito.")

        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def seleccionar_todos(self, id_usuario: str, seleccionado: bool = True) -> Carrito:
        carrito = self.obtener_carrito_activo(id_usuario)
        for item in carrito.items:
            item["seleccionado"] = bool(seleccionado)
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def obtener_items_seleccionados(self, carrito: Carrito) -> List[dict]:
        return [deepcopy(item) for item in carrito.items if bool(item.get("seleccionado", True))]

    def eliminar_producto(self, id_usuario: str, id_producto: str) -> Carrito:
        carrito = self.obtener_carrito_activo(id_usuario)
        carrito.items = [item for item in carrito.items if item["id_producto"] != id_producto]
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def vaciar(self, id_usuario: str) -> Carrito:
        carrito = self.obtener_carrito_activo(id_usuario)
        carrito.items = []
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def totalizar(self, carrito: Carrito, solo_seleccionados: bool = False) -> dict:
        items = self.obtener_items_seleccionados(carrito) if solo_seleccionados else carrito.items
        subtotal = round(sum(float(item.get("subtotal", 0)) for item in items), 2)
        impuesto = round(subtotal * 0.13, 2)
        return {
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total_parcial": round(subtotal + impuesto, 2),
            "cantidad_items": len(items),
        }

    def finalizar_items_comprados(self, id_carrito: str, ids_productos_comprados: List[str]) -> Carrito:
        """Quita del carrito los productos comprados y deja los demás activos."""
        carrito = self.carrito_repository.find_by_id(id_carrito)
        if not carrito:
            raise ValueError("No existe el carrito.")

        ids = {str(id_producto) for id_producto in ids_productos_comprados}
        carrito.items = [item for item in carrito.items if str(item.get("id_producto")) not in ids]
        carrito.estado = "Activo" if carrito.items else "Convertido"
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def marcar_convertido(self, id_carrito: str) -> Carrito:
        carrito = self.carrito_repository.find_by_id(id_carrito)
        if not carrito:
            raise ValueError("No existe el carrito.")
        carrito.estado = "Convertido"
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def restaurar_items(self, id_usuario: str, items_a_restaurar: List[dict]) -> Carrito:
        """Devuelve items al carrito activo, usado cuando falla un pago simulado."""
        carrito = self.obtener_carrito_activo(id_usuario)

        for item_restaurado in items_a_restaurar:
            id_producto = item_restaurado.get("id_producto")
            if not id_producto:
                continue

            existente = None
            for item in carrito.items:
                if item.get("id_producto") == id_producto:
                    existente = item
                    break

            cantidad_restaurada = int(item_restaurado.get("cantidad", 1))
            precio_unitario = float(item_restaurado.get("precio_unitario", 0))
            nombre = item_restaurado.get("nombre", "Producto")

            if existente:
                existente["cantidad"] = int(existente.get("cantidad", 0)) + cantidad_restaurada
                existente["precio_unitario"] = precio_unitario
                existente["nombre"] = nombre
                existente["subtotal"] = round(existente["cantidad"] * precio_unitario, 2)
                existente["seleccionado"] = True
            else:
                carrito.items.append({
                    "id_producto": id_producto,
                    "nombre": nombre,
                    "cantidad": cantidad_restaurada,
                    "precio_unitario": precio_unitario,
                    "subtotal": round(cantidad_restaurada * precio_unitario, 2),
                    "seleccionado": True,
                })

        carrito.estado = "Activo"
        carrito.fecha_actualizacion = now_iso()
        return self.carrito_repository.save(carrito)

    def _normalizar_y_guardar(self, carrito: Carrito) -> Carrito:
        cambiado = False
        for item in carrito.items:
            if "seleccionado" not in item:
                item["seleccionado"] = True
                cambiado = True
            cantidad = int(item.get("cantidad", 1))
            precio = float(item.get("precio_unitario", 0))
            subtotal = round(cantidad * precio, 2)
            if item.get("subtotal") != subtotal:
                item["subtotal"] = subtotal
                cambiado = True
        if cambiado:
            carrito.fecha_actualizacion = now_iso()
            return self.carrito_repository.save(carrito)
        return carrito
