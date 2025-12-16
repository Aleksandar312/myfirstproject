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

# Реални хотели + снимки
city_info = {
    "София": {
        "hotel": "Hotel Anel",
        "price": 90,
        "image": "https://www.hotelanel.com/images/gallery/hotel-anel-sofia.jpg",
        "sight": "Катедралата Александър Невски"
    },
    "Белград": {
        "hotel": "Hotel Moskva",
        "price": 85,
        "image": "https://www.hotelmoskva.rs/images/gallery/hotel-moskva-belgrade.jpg",
        "sight": "Калемегдан"
    },
    "Виена": {
        "hotel": "Austria Trend Hotel Savoyen",
        "price": 110,
        "image": "https://www.austria-trend.at/fileadmin/user_upload/Hotels/Savoyen/hotel-savoyen-vienna.jpg",
        "sight": "Дворецът Шьонбрун"
    },
    "Мюнхен": {
        "hotel": "Maritim Hotel München",
        "price": 105,
        "image": "https://www.maritim.com/fileadmin/user_upload/hotels/muenchen/exterior.jpg",
        "sight": "Мариенплац"
    },
    "Париж": {
        "hotel": "Hôtel Pullman Paris Tour Eiffel",
        "price": 140,
        "image": "https://www.pullmanpariseiffel.com/wp-content/uploads/sites/61/2021/06/pullman-paris-eiffel-tower.jpg",
        "sight": "Айфеловата кула"
    },
    "Рим": {
        "hotel": "Hotel Quirinale",
        "price": 120,
        "image": "https://www.hotelquirinale.it/images/gallery/hotel-quirinale-rome.jpg",
        "sight": "Колизеумът"
    },
    "Милано": {
        "hotel": "Hotel Berna",
        "price": 110,
        "image": "https://www.hotelberna.com/images/gallery/hotel-berna-milan.jpg",
        "sight": "Катедралата Дуомо"
    },
    "Лондон": {
        "hotel": "Park Plaza Westminster Bridge",
        "price": 150,
        "image": "https://www.parkplaza.com/parkplazawestminsterbridge/images/gallery/exterior.jpg",
        "sight": "Биг Бен"
    },
    "Скопие": {
        "hotel": "Hotel Alexandar Square",
        "price": 75,
        "image": "https://www.alexandarsquare.com/images/gallery/hotel.jpg",
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

    # ================== MAP (само точки) ==================
    map_data = [{"lat": city_coordinates[c][0], "lon": city_coordinates[c][1]} for c in cities]
    st.map(pd.DataFrame(map_data))

    # ================== HOTELS ==================
    total_hotel_cost = 0
    total_food_cost = 0
    hotel_breakdown = {}

    multiplier = HOTEL_MULTIPLIER[hotel_type]

    st.subheader("🏨 Хотелски обяви")

    for city in cities:
        info = city_info[city]
        price_per_night = info["price"] * multiplier
        hotel_total = price_per_night * days

        st.markdown(f"### 📍 {city}")
        st.image(info["image"], caption=info["hotel"], use_container_width=True)
        st.write(f"🏨 **{info['hotel']}** ({hotel_type})")
        st.write(f"💲 {price_per_night:.2f} лв / нощ")
        st.write(f"🏛️ Забележителност: {info['sight']}")

        hotel_breakdown[city] = hotel_total
        total_hotel_cost += hotel_total
        total_food_cost += 25 * days

    total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(total_distance)
    total_cost = transport_cost + total_food_cost + total_hotel_cost

    # ================== RESULTS ==================
    st.subheader("💰 Разходи")
    st.write(f"{transport.name()} – {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна: {total_food_cost:.2f} лв")
    st.write(f"🏨 Хотели: {total_hotel_cost:.2f} лв")

    st.subheader("🏨 Хотели по градове")
    for city, cost in hotel_breakdown.items():
        st.write(f"{city}: **{cost:.2f} лв**")

    st.markdown("---")
    st.write(f"## 💵 Общо: **{total_cost:.2f} лв**")

    diff = budget - total_cost
    if diff >= 0:
        st.success(f"✅ Остават ти **{diff:.2f} лв**")
    else:
        st.error(f"❌ Не достигат **{abs(diff):.2f} лв**")
