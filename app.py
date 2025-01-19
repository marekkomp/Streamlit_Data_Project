from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json
from io import BytesIO

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

# Wczytywanie danych i przetwarzanie opisów (tylko raz)
@st.cache_data
def wczytaj_i_przetworz_dane():
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")
    
    # Przetwórz opisy
    if "Opis oferty" in data.columns:
        data["Opis oferty (czysty tekst)"] = data["Opis oferty"].apply(przetworz_opis)
    else:
        st.warning("Kolumna 'Opis oferty' nie została znaleziona w danych.")

    return data

# Wczytaj dane (z pamięcią cache)
data = wczytaj_i_przetworz_dane()

# Wyświetlanie interfejsu
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

# Wyświetlanie przefiltrowanych danych
st.dataframe(filtered_data)

# Funkcje do zapisywania plików
def download_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def download_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    return output.getvalue()

# Dodanie przycisku do pobierania CSV
st.download_button(
    label="Pobierz dane jako CSV",
    data=download_csv(filtered_data),
    file_name="przefiltrowane_dane.csv",
    mime="text/csv"
)

# Dodanie przycisku do pobierania Excel
st.download_button(
    label="Pobierz dane jako Excel",
    data=download_excel(filtered_data),
    file_name="przefiltrowane_dane.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
