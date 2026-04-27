import flet as ft
import json
import os

# Имя файла для хранения данных
DATA_FILE = "data.json"

def main(page: ft.Page):
    page.title = "My Food"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.scroll = "auto"
    page.bgcolor = "#1a1a1a"

    # --- ФУНКЦИИ РАБОТЫ С ФАЙЛОМ ---
    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except:
                return {"cal": 0, "p": 0, "f": 0, "c": 0}
        return {"cal": 0, "p": 0, "f": 0, "c": 0}

    def save_data():
        with open(DATA_FILE, "w") as f:
            json.dump(total, f)

    # Загружаем данные при старте
    total = load_data()

    products = {
        "chicken": {"cal": 150, "p": 25, "f": 10, "c": 2, "img": "Food/Chicken.png"},
        "rice": {"cal": 370, "p": 8, "f": 1, "c": 85, "img": "Food/Rice.png"},
        "pasta": {"cal": 350, "p": 12, "f": 2, "c": 70, "img": "Food/Pasta.png"},
        "buckwheat": {"cal": 350, "p": 13, "f": 2, "c": 70, "img": "Food/Buckwheat.png"},
        "tuna": {"cal": 100, "p": 25, "f": 3, "c": 0, "img": "Food/Tuna.png"},
        "yoghurt": {"cal": 670, "p": 28, "f": 26, "c": 70, "img": "Food/Yoghurt.png"}
    }

    # Виджеты
    result_text = ft.Text(
        f"Kcal: {int(total['cal'])}  P: {int(total['p'])}  F: {int(total['f'])}  C: {int(total['c'])}",
        size=18, weight="bold", color="#4CAF50"
    )
    
    grams_input = ft.TextField(
        label="Сколько грамм?", 
        value="100", 
        width=200, 
        text_align="center",
        color="#ffffff",
        border_color="#444444"
    )

    def add_food(name):
        try:
            g = float(grams_input.value)
            p_data = products[name]
            total["cal"] += p_data["cal"] * g / 100
            total["p"] += p_data["p"] * g / 100
            total["f"] += p_data["f"] * g / 100
            total["c"] += p_data["c"] * g / 100
            
            result_text.value = f"Kcal: {int(total['cal'])}  P: {int(total['p'])}  F: {int(total['f'])}  C: {int(total['c'])}"
            save_data() # Сохраняем в файл
            page.update()
        except:
            grams_input.error_text = "Ошибка"
            page.update()

    def reset_data(e):
        for key in total: total[key] = 0
        result_text.value = "Kcal: 0  P: 0  F: 0  C: 0"
        save_data() # Обнуляем файл
        page.update()

    grid = ft.ResponsiveRow()

    for p_name, p_info in products.items():
        grid.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Image(src=p_info["img"], width=80, height=80, border_radius=10),
                    ft.Text(p_name.capitalize(), weight="bold", color="#ffffff", size=12),
                ], horizontal_alignment="center", spacing=5),
                on_click=lambda e, n=p_name: add_food(n),
                padding=10,
                col={"xs": 4, "sm": 4},
                border=ft.border.all(1, "#444444"),
                border_radius=15,
            )
        )

    page.add(
        ft.Column([
            ft.Text("My Food Calculator", size=25, weight="bold", color="#ffffff"),
            grams_input,
            result_text,
            ft.ElevatedButton("Сбросить прогресс", on_click=reset_data, bgcolor="#b22222", color="#ffffff"),
            ft.Divider(color="#333333"),
            grid
        ], horizontal_alignment="center", spacing=20)
    )

ft.app(target=main, assets_dir="assets")