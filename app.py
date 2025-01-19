from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json

# Funkcja do przetwarzania opisów
def przetworz_opis_debug(json_opis):
    try:
        data = json.loads(json_opis)
        teksty = []
        for section in data.get("sections", []):
            for item in section.get("items", []):
                if item.get("type") == "TEXT":
                    soup = BeautifulSoup(item["content"], "html.parser")
                    czysty_tekst = soup.get_text(separator="\n")
                    teksty.append(czysty_tekst)
        return "\n\n".join(tekstów)
    except Exception as e:
        st.error(f"Błąd podczas przetwarzania opisu: {e}")
        return ""

# Wczytaj dane z pliku
@st.cache_data
def wczytaj_dane():
    data = pd.read_csv("1.csv")
    # Usuń ewentualne spacje w nazwach kolumn
    data.columns = data.columns.str.strip()
    # Upewnij się, że kolumna "ID oferty" ma typ tekstowy
    if "ID oferty" in data.columns:
        data["ID oferty"] = data["ID oferty"].astype(str).str.strip()
    else:
        st.error("Kolumna 'ID oferty' nie istnieje w danych.")
    return data

# Wybierz ID oferty do analizy
id_oferty = st.sidebar.text_input("Podaj ID oferty do analizy", value="11132647668")

# Wczytaj dane
data = wczytaj_dane()

# Znajdź pozycję na podstawie ID oferty
if "ID oferty" in data.columns:
    wybrana_pozycja = data[data["ID oferty"] == id_oferty]
    if not wybrana_pozycja.empty:
        st.write(f"Znaleziono ofertę o ID: {id_oferty}")
        st.write(wybrana_pozycja)

        # Przetwórz opis oferty
        if "Opis oferty" in wybrana_pozycja.columns:
            opis = wybrana_pozycja["Opis oferty"].iloc[0]
            przetworzony_opis = przetworz_opis_debug(opis)
            st.write("Przetworzony opis:")
            st.text(przetworzony_opis)
        else:
            st.error("Kolumna 'Opis oferty' nie istnieje w danych.")
    else:
        st.error(f"Nie znaleziono pozycji o ID oferty {id_oferty}.")
else:
    st.error("Kolumna 'ID oferty' nie istnieje w danych.")
