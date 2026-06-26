from tkinter import messagebox


def get_selected_values(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selección requerida", "Selecciona un registro de la tabla.")
        return None
    return tree.item(selected[0], "values")


def parse_combo_id(value: str) -> str:
    if not value:
        return ""
    return value.split(" | ", 1)[0].strip()
