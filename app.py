from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json
import io

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
                    # Usuń znaczniki HTML, zachowując nowe wiersze dla list i paragrafów
                    czysty_tekst = BeautifulSoup(item["content"], "html.parser").get_text(separator="\n")
                    teksty.append(czysty_tekst)

        # Połącz wyczyszczony tekst w jedną całość, zachowując odstępy między sekcjami
        return "\n\n".join(tekst.replace("\n", "\n") for tekst in teksty)
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

# Opcja pobrania przetworzonej tabeli w formacie CSV
st.download_button(
    label="Pobierz przetworzoną tabelę w CSV",
    data=filtered_data.to_csv(index=False).encode("utf-8"),
    file_name="przetworzona_tabela.csv",
    mime="text/csv"
)

# Opcja pobrania przetworzonej tabeli w formacie Excel
output = io.BytesIO()
filtered_data.to_excel(output, index=False, engine='openpyxl')
output.seek(0)
st.download_button(
    label="Pobierz przetworzoną tabelę w Excelu",
    data=output,
    file_name="przetworzona_tabela.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Wyświetlenie przykładowego opisu (pierwszy wiersz przefiltrowanej tabeli)
if not filtered_data.empty:
    st.subheader("Przykładowy opis (z zachowaniem nowych linii):")
    st.text(filtered_data.iloc[0]["Opis oferty (czysty tekst)"])
