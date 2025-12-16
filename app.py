import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd
import pydeck as pdk

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Франция": ["София", "Белград", "Виена", "Париж"],
    "България → Италия": ["София", "Скопие", "Рим", "Милано"],
    "България → Австрия": ["София", "Белград", "Виена"],
    "България → Англия": ["София", "Виена", "Париж", "Лондон"]
}

# Базова (стандартна) цена
city_info = {
    "София": ("Hotel Sofia Center", 70, "Катедралата Александър Невски"),
    "Белград": ("Belgrade Inn", 65, "Калемегдан"),
    "Виена": ("Vienna City Hotel", 90, "Дворецът Шьонбрун"),
    "Мюнхен": ("Munich Central Hotel", 95, "Мариенплац"),
    "Париж": ("Paris Central Hotel", 110, "Айфеловата кула"),
    "Рим": ("Rome Historic Hotel", 100, "Колизеумът"),
    "Милано": ("Milano City Hotel", 105, "Катедралата Дуомо"),
    "Лондон": ("London Bridge Hotel", 120, "Биг Бен"),
    "Скопие": ("Skopje Plaza", 60, "Каменният мост")
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

# Множители за хотел
HOTEL_TYPE_MULTIPLIER = {
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
days = st.slider("Брой дни за пътуването:", 1, 10, 4)
budget = st.number_input("Твоят бюджет (лв):", 300, 5000, 1500)

if st.button("Планирай пътуването 🧭"):
    cities = routes[route_choice]

    transport = Car() if transport_choice == "Кола" else Train() if transport_choice == "Влак" else Plane()

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    # ================== MAP WITH LINE ==================

    points = []
    lines = []

    for city in cities:
        lat, lon = city_coordinates[city]
        points.append({"lat": lat, "lon": lon})

    for i in range(len(cities) - 1):
        start = city_coordinates[cities[i]]
        end = city_coordinates[cities[i + 1]]
        lines.append({
            "start": [start[1], start[0]],
            "end": [end[1], end[0]]
        })

    layer_points = pdk.Layer(
        "ScatterplotLayer",
        points,
        get_position="[lon, lat]",
        get_radius=80000,
        get_color=[200, 30, 0],
        pickable=True,
    )

    layer_lines = pdk.Layer(
        "LineLayer",
        lines,
        get_source_position="start",
        get_target_position="end",
        get_color=[0, 0, 200],
        get_width=5,
    )

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
        initial_view_state=pdk.ViewState(
            latitude=points[0]["lat"],
            longitude=points[0]["lon"],
            zoom=4,
        ),
        layers=[layer_points, layer_lines],
    ))

    # ================== CITY DETAILS ==================

    total_food_cost = 0
    total_hotel_cost = 0
    hotel_costs_per_city = {}

    multiplier = HOTEL_TYPE_MULTIPLIER[hotel_type]

    st.subheader("🏙️ Спирки и разходи")

    for city in cities:
        hotel_name, base_price, sight = city_info[city]
        adjusted_price = base_price * multiplier
        hotel_total = adjusted_price * days

        st.markdown(f"### 📍 {city}")
        st.write(f"🏨 {hotel_name} ({hotel_type}) – {adjusted_price:.2f} лв/нощ")
        st.write(f"🏛️ {sight}")

        hotel_costs_per_city[city] = hotel_total
        total_hotel_cost += hotel_total
        total_food_cost += 25 * days  # средна храна

    total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(total_distance)
    total_cost = transport_cost + total_food_cost + total_hotel_cost

    # ================== RESULTS ==================

    st.subheader("💰 Разходи")
    st.write(f"{transport.name()} – {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна: {total_food_cost:.2f} лв")
    st.write(f"🏨 Хотели: {total_hotel_cost:.2f} лв")

    st.subheader("🏨 Хотели по градове")
    for city, cost in hotel_costs_per_city.items():
        st.write(f"{city}: **{cost:.2f} лв**")

    st.markdown("---")
    st.write(f"## 💵 Общо: **{total_cost:.2f} лв**")

    diff = budget - total_cost
    if diff >= 0:
        st.success(f"✅ Остават ти **{diff:.2f} лв**")
    else:
        st.error(f"❌ Не достигат **{abs(diff):.2f} лв**")
