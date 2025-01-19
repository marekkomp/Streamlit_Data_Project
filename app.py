from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json

# Funkcja do przetwarzania opisów
def przetworz_opis(json_opis):
    try:
        # Załaduj JSON
        data = json.loads(json_opis)
        
        # Wyciągnij wszystkie pola "content" z sekcji
        teksty = []
        for section in data.get("sections", []):
            for item in section.get("items", []):
                if item.get("type") == "TEXT":
                    # Usuń znaczniki HTML
                    czysty_tekst = BeautifulSoup(item["content"], "html.parser").get_text()
                    teksty.append(czysty_tekst)

        # Połącz wyczyszczony tekst w jedną całość
        return "\n\n".join(teksty)
    except Exception as e:
        return f"Błąd podczas przetwarzania: {e}"

# Wczytywanie danych
try:
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")

    # Przetwórz kolumnę "Opis oferty"
    if "Opis oferty" in data.columns:
        data["Opis oferty (czysty tekst)"] = data["Opis oferty"].apply(przetworz_opis)
    else:
        st.warning("Kolumna 'Opis oferty' nie została znaleziona w danych.")

    # Wyświetlanie danych
    st.title("Aplikacja do filtrowania danych z czyszczeniem opisów")
    st.write("Tabela zawiera wszystkie dane wraz z przetworzonymi opisami.")

    # Filtr dla kolumny "Status oferty"
    status_options = data["Status oferty"].dropna().unique()  # Unikalne wartości w kolumnie
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

    # Wyświetlanie przefiltrowanych danych z czystymi opisami
    st.dataframe(filtered_data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except KeyError as e:
    st.error(f"Brakuje kolumny w danych: {e}")

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
