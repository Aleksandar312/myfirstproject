import streamlit as st

from abc import ABC, abstractmethod

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Франция": ["София", "Виена", "Мюнхен", "Париж"],
    "България → Италия": ["София", "Виена", "Мюнхен", "Рим", "Милано"],
    "България → Англия": ["София", "Виена", "Мюнхен", "Лондон"]
}

city_info = {
    "София": {
        "hotel": ("Hotel Anel", 70),
        "food": ("Традиционна българска кухня", 20),
        "sight": "Катедралата Александър Невски",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/6/6c/Hotel_Anel_Sofia.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/4/48/Hotel_Anel_lobby.jpg"
        ]
    },
    "Белград": {
        "hotel": ("Hotel Moskva", 65),
        "food": ("Сръбска скара", 22),
        "sight": "Калемегдан",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/5/57/Hotel_Moskva_Belgrade.jpg"
        ]
    },
    "Виена": {
        "hotel": ("Austria Trend Hotel Savoyen", 90),
        "food": ("Виенски шницел", 30),
        "sight": "Дворецът Шьонбрун",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/7/77/Austria_Trend_Savoyen_Vienna.jpg"
        ]
    },
    "Мюнхен": {
        "hotel": ("Munich Central Hotel", 95),
        "food": ("Немска кухня", 28),
        "sight": "Мариенплац",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/2/2a/Munich_Central_Hotel.jpg"
        ]
    },
    "Париж": {
        "hotel": ("Pullman Paris Tour Eiffel", 120),
        "food": ("Френска кухня", 35),
        "sight": "Айфеловата кула",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/1/1c/Pullman_Paris_Tour_Eiffel.jpg"
        ]
    },
    "Рим": {
        "hotel": ("Hotel Quirinale", 110),
        "food": ("Италианска кухня", 32),
        "sight": "Колизеум",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/8/81/Hotel_Quirinale_Rome.jpg"
        ]
    },
    "Милано": {
        "hotel": ("Hotel Berna", 105),
        "food": ("Италианска кухня", 30),
        "sight": "Катедралата Дуомо",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/6/60/Hotel_Berna_Milano.jpg"
        ]
    },
    "Лондон": {
        "hotel": ("Park Plaza Westminster Bridge", 130),
        "food": ("Английска кухня", 35),
        "sight": "Биг Бен",
        "image_urls": [
            "https://upload.wikimedia.org/wikipedia/commons/0/02/Park_Plaza_Westminster_Bridge_London.jpg"
        ]
    }
}

DISTANCE_BETWEEN_CITIES = 300  # км (опростено)

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
days = st.slider("Брой дни за пътуването:", 1, 10, 4)
budget = st.number_input("Твоят бюджет (лв):", 300, 5000, 1500)

if st.button("Планирай пътуването 🧭"):

    cities = routes[route_choice]

    # Избор на транспорт (полиморфизъм)
    transport = Car() if transport_choice=="Кола" else Train() if transport_choice=="Влак" else Plane()

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    # ================== CITY DETAILS ==================
    st.subheader("🏙️ Спирки и предложения")

    total_food_cost = 0
    total_hotel_cost = 0

    for city in cities:
        info = city_info[city]
        st.markdown(f"### 📍 {city}")
        st.write(f"🏨 **Хотел:** {info['hotel'][0]} – {info['hotel'][1]} лв/нощ")
        st.write(f"🍽️ **Храна:** {info['food'][0]} – {info['food'][1]} лв/ден")
        st.write(f"🏛️ **Забележителност:** {info['sight']}")

        # Покажи всички изображения на хотела
        for url in info.get("image_urls", []):
            st.image(url, use_column_width=True)

        total_food_cost += info['food'][1] * days
        total_hotel_cost += info['hotel'][1] * days

    # ================== COST CALCULATION ==================
    total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(total_distance)
    total_cost = transport_cost + total_food_cost + total_hotel_cost

    # ================== RESULTS ==================
    st.subheader("💰 Разходи")
    st.write(f"{transport.name()} – транспорт: {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна: {total_food_cost:.2f} лв")
    st.write(f"🏨 Хотели: {total_hotel_cost:.2f} лв")

    st.markdown("---")
    st.write(f"## 💵 Общ бюджет: **{total_cost:.2f} лв**")

    if total_cost <= budget:
        st.success("✅ Бюджетът е достатъчен! Приятно пътуване ✨")
    else:
        st.error("❌ Бюджетът не достига. Помисли за по-евтин транспорт или по-малко дни.")
