import streamlit as st
import pandas as pd
import re
from html import unescape

# Funkcja do usuwania znaczników HTML
def clean_html(raw_html):
    clean_text = re.sub(r'<.*?>', '', raw_html)  # Usuwa znaczniki HTML
    return unescape(clean_text)  # Dekoduje encje HTML

# Wczytywanie danych
try:
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")

    st.title("Aplikacja do filtrowania i przetwarzania danych")
    st.write("Filtrujemy dane i przekształcamy opis oferty na czytelny tekst.")

    # Filtr dla kolumny "Status oferty"
    status_options = data["Status oferty"].dropna().unique()
    selected_status = st.sidebar.multiselect("Wybierz status oferty", status_options, default=status_options)

    # Filtr dla kolumny "Kategoria główna"
    category_options = data["Kategoria główna"].dropna().unique()
    selected_category = st.sidebar.multiselect("Wybierz kategorię główną", category_options, default=category_options)

    # Filtr dla kolumny "Liczba sztuk"
    min_sztuk = st.sidebar.number_input("Minimalna liczba sztuk", min_value=0, value=int(data["Liczba sztuk"].min()))
    max_sztuk = st.sidebar.number_input("Maksymalna liczba sztuk", min_value=0, value=int(data["Liczba sztuk"].max()))

    # Filtrowanie danych
    filtered_data = data[
        (data["Status oferty"].isin(selected_status)) &
        (data["Kategoria główna"].isin(selected_category)) &
        (data["Liczba sztuk"] >= min_sztuk) &
        (data["Liczba sztuk"] <= max_sztuk)
    ]

    # Przekształcanie opisów w przefiltrowanych danych
    if "Opis oferty" in filtered_data.columns:
        filtered_data["Opis oferty"] = filtered_data["Opis oferty"].fillna("").apply(clean_html)

    # Wyświetlanie przefiltrowanych danych
    st.dataframe(filtered_data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except KeyError as e:
    st.error(f"Brakuje kolumny w danych: {e}")

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
