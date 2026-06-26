import tkinter as tk
from tkinter import ttk

PRIMARY = "#2563eb"
PRIMARY_DARK = "#1e40af"
ACCENT = "#16a34a"
DANGER = "#dc2626"
WARNING = "#f59e0b"
BG = "#eef2f7"
CARD = "#ffffff"
TEXT = "#111827"
MUTED = "#6b7280"
SIDEBAR = "#111827"
SIDEBAR_HOVER = "#1f2937"


def setup_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Main.TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD, relief="flat")
    style.configure("Sidebar.TFrame", background=SIDEBAR)
    style.configure("TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 10))
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
    style.configure("Header.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 24, "bold"))
    style.configure("Title.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 18, "bold"))
    style.configure("SidebarTitle.TLabel", background=SIDEBAR, foreground="white", font=("Segoe UI", 17, "bold"))
    style.configure("SidebarSub.TLabel", background=SIDEBAR, foreground="#cbd5e1", font=("Segoe UI", 9))
    style.configure("Field.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 10, "bold"))
    style.configure("TEntry", padding=7)
    style.configure("TCombobox", padding=6)
    style.configure("TButton", padding=8, font=("Segoe UI", 10, "bold"), background="#e5e7eb", foreground=TEXT, borderwidth=0)
    style.map("TButton", background=[("active", "#d1d5db")])
    style.configure("Primary.TButton", background=PRIMARY, foreground="white")
    style.map("Primary.TButton", background=[("active", PRIMARY_DARK)])
    style.configure("Success.TButton", background=ACCENT, foreground="white")
    style.map("Success.TButton", background=[("active", "#15803d")])
    style.configure("Danger.TButton", background=DANGER, foreground="white")
    style.map("Danger.TButton", background=[("active", "#991b1b")])
    style.configure("Nav.TButton", background=SIDEBAR, foreground="white", anchor="w", padding=11, borderwidth=0, font=("Segoe UI", 10, "bold"))
    style.map("Nav.TButton", background=[("active", SIDEBAR_HOVER)])
    style.configure("Treeview", background=CARD, foreground=TEXT, rowheight=29, fieldbackground=CARD, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", background="#e5e7eb", foreground=TEXT, font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", PRIMARY)], foreground=[("selected", "white")])


def page(parent, title: str, subtitle: str):
    frame = ttk.Frame(parent, style="Main.TFrame")
    frame.pack(fill="both", expand=True, padx=24, pady=20)
    ttk.Label(frame, text=title, style="Header.TLabel").pack(anchor="w")
    ttk.Label(frame, text=subtitle, style="Muted.TLabel").pack(anchor="w", pady=(0, 16))
    return frame


def card(parent, padding=16):
    c = ttk.Frame(parent, style="Card.TFrame", padding=padding)
    return c


def money(value):
    try:
        return f"₡{float(value):,.2f}"
    except Exception:
        return "₡0.00"


def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)


def selected_values(tree):
    selected = tree.selection()
    if not selected:
        return None
    return tree.item(selected[0], "values")
