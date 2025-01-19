from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json

# Funkcja do przetwarzania opisów z poprawionym formatowaniem
def przetworz_opis(json_opis):
    try:
        data = json.loads(json_opis)
        teksty = []
        for section in data.get("sections", []):
            for item in section.get("items", []):
                if item.get("type") == "TEXT":
                    soup = BeautifulSoup(item["content"], "html.parser")

                    # Zamień znaczniki <li> na myślniki z nową linią
                    for li in soup.find_all("li"):
                        li.insert_before("\n- ")
                        li.insert_after("\n")
                    
                    # Zamień znaczniki <h2>, <h3>, itp., na nagłówki z przerwami
                    for header in soup.find_all(["h1", "h2", "h3", "h4"]):
                        header.insert_before("\n\n")
                        header.insert_after("\n\n")
                    
                    # Dodaj przerwy dla akapitów <p>
                    for p in soup.find_all("p"):
                        p.insert_before("\n")
                        p.insert_after("\n")

                    # Usuń pozostałe znaczniki HTML, zachowując separator "\n"
                    czysty_tekst = soup.get_text(separator="\n")
                    teksty.append(czysty_tekst)

        return "\n".join(teksty)
    except Exception as e:
        return f"Błąd podczas przetwarzania opisu: {e}"

# Wczytaj dane z pliku
@st.cache_data
def wczytaj_dane():
    data = pd.read_csv("1.csv")
    data.columns = data.columns.str.strip()  # Usuń spacje w nazwach kolumn
    if "ID oferty" in data.columns:
        data["ID oferty"] = data["ID oferty"].astype(str).str.strip()  # Upewnij się, że ID jest tekstowe
    return data

# Wybór ID oferty do analizy
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
            przetworzony_opis = przetworz_opis(opis)
            st.write("Przetworzony opis:")
            st.text(przetworzony_opis)
        else:
            st.error("Kolumna 'Opis oferty' nie istnieje w danych.")
    else:
        st.error(f"Nie znaleziono pozycji o ID oferty {id_oferty}.")
else:
    st.error("Kolumna 'ID oferty' nie istnieje w danych.")
