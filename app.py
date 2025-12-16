import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Франция": ["София", "Белград", "Виена", "Париж"],
    "България → Италия": ["София", "Скопие", "Рим", "Милано"],
    "България → Австрия": ["София", "Белград", "Виена"],
    "България → Англия": ["София", "Виена", "Париж", "Лондон"]
}

city_info = {
    "София": {
        "hotel": ("Hotel Sofia Center", 70),
        "food": ("Традиционна българска кухня", 20),
        "sight": "Катедралата Александър Невски"
    },
    "Белград": {
        "hotel": ("Belgrade Inn", 65),
        "food": ("Сръбска скара", 22),
        "sight": "Калемегдан"
    },
    "Виена": {
        "hotel": ("Vienna City Hotel", 90),
        "food": ("Виенски шницел", 30),
        "sight": "Дворецът Шьонбрун"
    },
    "Мюнхен": {
        "hotel": ("Munich Central Hotel", 95),
        "food": ("Немска кухня", 28),
        "sight": "Мариенплац"
    },
    "Париж": {
        "hotel": ("Paris Central Hotel", 110),
        "food": ("Френска кухня", 35),
        "sight": "Айфеловата кула"
    },
    "Рим": {
        "hotel": ("Rome Historic Hotel", 100),
        "food": ("Италианска паста", 32),
        "sight": "Колизеумът"
    },
    "Милано": {
        "hotel": ("Milano City Hotel", 105),
        "food": ("Пица и ризото", 30),
        "sight": "Катедралата Дуомо"
    },
    "Лондон": {
        "hotel": ("London Bridge Hotel", 120),
        "food": ("Британска кухня", 40),
        "sight": "Биг Бен"
    },
    "Скопие": {
        "hotel": ("Skopje Plaza", 60),
        "food": ("Балканска кухня", 20),
        "sight": "Каменният мост"
    }
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

    # Избор на транспорт
    if transport_choice == "Кола":
        transport = Car()
    elif transport_choice == "Влак":
        transport = Train()
    else:
        transport = Plane()

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    # ================== MAP ==================
    st.subheader("🗺️ Карта на маршрута")

    map_data = []
    for city in cities:
        lat, lon = city_coordinates[city]
        map_data.append({"lat": lat, "lon": lon})

    df = pd.DataFrame(map_data)
    st.map(df)

    # ================== CITY DETAILS ==================
    st.subheader("🏙️ Спирки и предложения")

    total_food_cost = 0
    total_hotel_cost = 0
    hotel_costs_per_city = {}

    for city in cities:
        info = city_info[city]

        st.markdown(f"### 📍 {city}")
        st.write(f"🏨 **Хотел:** {info['hotel'][0]} – {info['hotel'][1]} лв/нощ")
        st.write(f"🍽️ **Храна:** {info['food'][0]} – {info['food'][1]} лв/ден")
        st.write(f"🏛️ **Забележителност:** {info['sight']}")

        hotel_total = info['hotel'][1] * days
        hotel_costs_per_city[city] = hotel_total

        total_food_cost += info['food'][1] * days
        total_hotel_cost += hotel_total

    # ================== COST CALCULATION ==================
    total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(total_distance)
    total_cost = transport_cost + total_food_cost + total_hotel_cost

    # ================== RESULTS ==================
    st.subheader("💰 Разходи")
    st.write(f"{transport.name()} – транспорт: {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна: {total_food_cost:.2f} лв")
    st.write(f"🏨 Хотели (общо): {total_hotel_cost:.2f} лв")

    st.subheader("🏨 Разходи за хотели по градове")
    for city, cost in hotel_costs_per_city.items():
        st.write(f"📍 {city}: **{cost:.2f} лв**")

    st.markdown("---")
    st.write(f"## 💵 Общ бюджет за пътуването: **{total_cost:.2f} лв**")

    difference = budget - total_cost
    if difference >= 0:
        st.success(f"💚 Остават ти **{difference:.2f} лв** след пътуването.")
    else:
        st.error(f"🔴 Не достигат **{abs(difference):.2f} лв** за това пътуване.")
