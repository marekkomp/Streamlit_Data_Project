import streamlit as st
import pandas as pd

# Wczytywanie danych
try:
    # Wczytaj plik CSV (upewnij się, że nazwa pliku się zgadza)
    data = pd.read_csv("1.csv")

    st.title("Aplikacja do filtrowania danych")
    st.write("Poniżej znajdują się dane z pliku z interaktywnymi filtrami.")

    # Filtr dla kolumny "Status oferty"
    status_options = data["Status oferty"].dropna().unique()  # Unikalne wartości w kolumnie
    selected_status = st.sidebar.multiselect("Wybierz status oferty", status_options, default=status_options)

    # Filtr dla kolumny "Kategoria główna"
    category_options = data["Kategoria główna"].dropna().unique()
    selected_category = st.sidebar.multiselect("Wybierz kategorię główną", category_options, default=category_options)

    # Filtr dla kolumny "Liczba sztuk"
    min_sztuk, max_sztuk = st.sidebar.slider(
        "Wybierz zakres liczby sztuk",
        int(data["Liczba sztuk"].min()),
        int(data["Liczba sztuk"].max()),
        (int(data["Liczba sztuk"].min()), int(data["Liczba sztuk"].max()))
    )

    # Filtrowanie danych
    filtered_data = data[
        (data["Status oferty"].isin(selected_status)) &
        (data["Kategoria główna"].isin(selected_category)) &
        (data["Liczba sztuk"] >= min_sztuk) &
        (data["Liczba sztuk"] <= max_sztuk)
    ]

    # Wyświetlanie przefiltrowanych danych
    st.dataframe(filtered_data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except KeyError as e:
    st.error(f"Brakuje kolumny w danych: {e}")

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
