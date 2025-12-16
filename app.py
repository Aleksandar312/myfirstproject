import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import random

# ================== IMAGE GENERATOR ==================

def generate_hotel_image(city, hotel_name, seed):
    random.seed(seed)
    img = Image.new("RGB", (800, 450), (
        random.randint(100, 180),
        random.randint(100, 180),
        random.randint(100, 180)
    ))
    draw = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 26)
    except:
        font_big = font_small = ImageFont.load_default()

    draw.text((30, 40), hotel_name, fill="white", font=font_big)
    draw.text((30, 100), f"📍 {city}", fill="white", font=font_small)
    draw.text((30, 160), "Luxury Hotel Experience", fill="white", font=font_small)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Франция": ["София", "Белград", "Виена", "Париж"],
    "България → Италия": ["София", "Скопие", "Рим", "Милано"],
    "България → Австрия": ["София", "Белград", "Виена"],
    "България → Англия": ["София", "Виена", "Париж", "Лондон"]
}

city_info = {
    "София": ("Hotel Anel", 90, "Катедралата Александър Невски"),
    "Белград": ("Hotel Moskva", 85, "Калемегдан"),
    "Виена": ("Hotel Savoyen", 110, "Дворецът Шьонбрун"),
    "Мюнхен": ("Maritim Hotel", 105, "Мариенплац"),
    "Париж": ("Pullman Paris", 140, "Айфеловата кула"),
    "Рим": ("Hotel Quirinale", 120, "Колизеумът"),
    "Милано": ("Hotel Berna", 110, "Катедралата Дуомо"),
    "Лондон": ("Park Plaza Westminster", 150, "Биг Бен"),
    "Скопие": ("Hotel Alexandar Square", 75, "Каменният мост")
}

city_coordinates = {
    "София": (42.6977, 23.3219),
    "Белград": (44.7866, 20.4489),
    "Виена": (48.2082, 16.3738),
    "Мюнхен": (48.1351, 11.5820),
    "Париж": (48.8566, 2.3522),
    "Рим": (41.9028, 12.4964),
    "Милано": (45.4642, 9.1900),
    "Лондон": (51.5074, -0.1278),
    "Скопие": (41.9973, 21.4280)
}

HOTEL_MULTIPLIER = {
    "Евтин": 0.8,
    "Стандартен": 1.0,
    "Луксозен": 1.5
}

DISTANCE_BETWEEN_CITIES = 300

# ================== OOP ==================

class Transport(ABC):
    def __init__(self, price_per_km):
        self.price_per_km = price_per_km

    @abstractmethod
    def name(self):
        pass

    def travel_cost(self, distance):
        return distance * self.price_per_km

class Car(Transport):
    def __init__(self):
        super().__init__(0.25)
    def name(self):
        return "🚗 Кола"

class Train(Transport):
    def __init__(self):
        super().__init__(0.18)
    def name(self):
        return "🚆 Влак"

class Plane(Transport):
    def __init__(self):
        super().__init__(0.45)
    def name(self):
        return "✈️ Самолет"

# ================== UI ==================

st.title("🌍 Интерактивен туристически планер")

route_choice = st.selectbox("Избери маршрут:", list(routes.keys()))
transport_choice = st.selectbox("Превозно средство:", ["Кола", "Влак", "Самолет"])
hotel_type = st.selectbox("Тип хотел:", ["Евтин", "Стандартен", "Луксозен"])
days = st.slider("Брой дни:", 1, 10, 4)
budget = st.number_input("Бюджет (лв):", 300, 5000, 1500)

if st.button("Планирай пътуването 🧭"):
    cities = routes[route_choice]
    transport = Car() if transport_choice == "Кола" else Train() if transport_choice == "Влак" else Plane()

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    st.map(pd.DataFrame([{"lat": city_coordinates[c][0], "lon": city_coordinates[c][1]} for c in cities]))

    multiplier = HOTEL_MULTIPLIER[hotel_type]
    total_hotel_cost = total_food_cost = 0
    hotel_breakdown = {}

    st.subheader("🏨 Хотелски обяви")

    for city in cities:
        hotel, base_price, sight = city_info[city]
        price = base_price * multiplier
        total = price * days

        st.markdown(f"### 📍 {city}")
        cols = st.columns(3)

        for i, col in enumerate(cols):
            with col:
                img = generate_hotel_image(city, hotel, i)
                st.image(img, use_container_width=True)

        st.write(f"🏨 **{hotel}** ({hotel_type})")
        st.write(f"⭐ Рейтинг: {'⭐' * 4}☆")
        st.write(f"💲 {price:.2f} лв / нощ")
        st.write(f"🏛️ {sight}")
        st.button(f"Резервирай в {hotel}", key=city)

        hotel_breakdown[city] = total
        total_hotel_cost += total
        total_food_cost += 25 * days

    transport_cost = transport.travel_cost(DISTANCE_BETWEEN_CITIES * (len(cities) - 1))
    total_cost = transport_cost + total_food_cost + total_hotel_cost

    st.subheader("💰 Разходи")
    st.write(f"{transport.name()}: {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна: {total_food_cost:.2f} лв")
    st.write(f"🏨 Хотели: {total_hotel_cost:.2f} лв")

    st.subheader("🏨 Разбивка по градове")
    for city, cost in hotel_breakdown.items():
        st.write(f"{city}: **{cost:.2f} лв**")

    st.markdown("---")
    st.write(f"## 💵 Общо: **{total_cost:.2f} лв**")

    diff = budget - total_cost
    if diff >= 0:
        st.success(f"✅ Остават ти **{diff:.2f} лв**")
    else:
        st.error(f"❌ Не достигат **{abs(diff):.2f} лв**")
