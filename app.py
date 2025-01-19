from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json

# Funkcja do przetwarzania opisów z debugowaniem
def przetworz_opis_debug(json_opis):
    try:
        # Załaduj JSON
        data = json.loads(json_opis)
        
        # Wyciągnij wszystkie pola "content" z sekcji
        teksty = []
        for section in data.get("sections", []):
            for item in section.get("items", []):
                if item.get("type") == "TEXT":
                    # Przetwórz zawartość HTML
                    soup = BeautifulSoup(item["content"], "html.parser")
                    
                    # Debug: pokaż oryginalny HTML
                    st.text("\n[DEBUG] Oryginalny HTML:\n" + soup.prettify())
                    
                    # Zamień znaczniki <ul> i <li> na czytelne formatowanie
                    for ul in soup.find_all("ul"):
                        ul.insert_before("\n")  # Dodaj przerwę przed listą
                        for li in ul.find_all("li"):
                            li.insert_before("- ")  # Dodaj myślnik przed każdą pozycją listy
                            li.insert_after("\n")  # Dodaj nową linię po każdej pozycji
                        ul.unwrap()  # Usuń znacznik <ul>
                    
                    # Debug: pokaż HTML po przetworzeniu list
                    st.text("\n[DEBUG] HTML po przetworzeniu list:\n" + soup.prettify())
                    
                    # Zamień znaczniki <h2>, <h3>, itp., na nowe wiersze
                    for header in soup.find_all(["h1", "h2", "h3", "h4"]):
                        header.insert_before("\n")  # Przerwa przed nagłówkiem
                        header.insert_after("\n")  # Przerwa po nagłówku
                    
                    # Zamień znaczniki <p> na nowe wiersze
                    for p in soup.find_all("p"):
                        p.insert_before("\n")  # Przerwa przed akapitem
                        p.insert_after("\n")  # Przerwa po akapicie
                    
                    # Debug: pokaż HTML po przetworzeniu nagłówków i akapitów
                    st.text("\n[DEBUG] HTML po przetworzeniu nagłówków i akapitów:\n" + soup.prettify())
                    
                    # Usuń wszystkie znaczniki HTML, zachowując formatowanie
                    czysty_tekst = soup.get_text(separator="\n")
                    teksty.append(czysty_tekst)

                    # Debug: pokaż przetworzony tekst
                    st.text("\n[DEBUG] Przetworzony tekst:\n" + czysty_tekst)

        # Połącz wyczyszczony tekst w jedną całość, dodając przerwy między sekcjami
        return "\n\n".join(tekstów)
    except Exception as e:
        st.error(f"Błąd podczas przetwarzania opisu: {e}")
        return ""

# Wczytywanie danych i przetwarzanie opisów (tylko raz)
@st.cache_data
def wczytaj_i_przetworz_dane():
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")
    
    # Przetwórz opisy
    if "Opis oferty" in data.columns:
        data["Opis oferty (czysty tekst)"] = data["Opis oferty"].apply(przetworz_opis_debug)
    else:
        st.warning("Kolumna 'Opis oferty' nie została znaleziona w danych.")

    return data

# Wczytaj dane (z pamięcią cache)
data = wczytaj_i_przetworz_dane()

# Wyświetlanie interfejsu
st.title("Aplikacja do filtrowania danych z czyszczeniem opisów i debugowaniem")
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

# Opcja pobrania przetworzonej tabeli
st.download_button(
    label="Pobierz przetworzoną tabelę",
    data=filtered_data.to_csv(index=False).encode("utf-8"),
    file_name="przetworzona_tabela.csv",
    mime="text/csv"
)
