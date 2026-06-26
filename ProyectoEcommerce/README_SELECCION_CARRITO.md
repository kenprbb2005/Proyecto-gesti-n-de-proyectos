# Corrección: selección de productos en el carrito

Esta versión corrige el módulo **Carrito de compras** para que el usuario pueda elegir cuáles productos comprar.

## Cambios principales

- Se agregó columna **Comprar** en la tabla del carrito.
- Cada producto puede estar marcado como `✓ Sí` o `— No`.
- Doble clic sobre un producto alterna su estado de compra.
- Botones nuevos:
  - **Marcar seleccionado**
  - **Quitar seleccionado**
  - **Marcar todos**
  - **Quitar todos**
- El resumen calcula subtotal, IVA, envío y total solo con productos marcados.
- El botón **Comprar productos marcados** compra únicamente los productos marcados.
- El botón **Crear pedido con productos marcados** crea pedido solo con esos productos.
- Los productos no marcados permanecen en el carrito.
- Si el pago simulado falla, el sistema cancela el pedido, restaura stock y devuelve los productos al carrito.

## Flujo de prueba

1. Ejecutar:

```bash
python main.py
```

2. Iniciar sesión:

```txt
cliente@demo.com
cliente123
```

3. Ir al catálogo.
4. Agregar varios productos al carrito.
5. Ir a **Carrito de compras**.
6. Quitar la marca de los productos que no quieres comprar ahora.
7. Escribir dirección exacta.
8. Presionar **Comprar productos marcados**.

## Regla de negocio importante

Solo se compran los productos cuyo campo `seleccionado` esté en `True` dentro de `data/carritos.json`.
