from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json

# Funkcja do przetwarzania opisów
def przetworz_opis(json_opis):
    try:
        data = json.loads(json_opis)
        teksty = []

        for section in data.get("sections", []):
            for item in section.get("items", []):
                if item.get("type") == "TEXT":
                    soup = BeautifulSoup(item["content"], "html.parser")

                    for li in soup.find_all("li"):
                        li.insert_before("\n- ")
                        li.unwrap()

                    for ul in soup.find_all("ul"):
                        ul.unwrap()

                    for bold in soup.find_all("b"):
                        bold.unwrap()

                    for tag in soup.find_all(["p", "h2", "h3", "h4"]):
                        tag.insert_before("\n")
                        tag.insert_after("\n")
                        tag.unwrap()

                    czysty_tekst = soup.get_text()
                    czysty_tekst = "\n".join(line.strip() for line in czysty_tekst.splitlines() if line.strip())
                    teksty.append(czysty_tekst)

        return "\n\n".join(teksty)
    except Exception as e:
        st.error(f"Błąd podczas przetwarzania opisu: {e}")
        return ""

# Wczytaj dane z pliku
@st.cache_data
def wczytaj_dane():
    data = pd.read_csv("1.csv")
    data.columns = data.columns.str.strip()
    if "ID oferty" in data.columns:
        data["ID oferty"] = data["ID oferty"].astype(str).str.strip()
    else:
        st.error("Kolumna 'ID oferty' nie istnieje w danych.")
    return data

# Wczytaj dane
data = wczytaj_dane()

# Przetwórz opisy i dodaj jako nową kolumnę
if "Opis oferty" in data.columns:
    data["Przetworzony opis"] = data["Opis oferty"].apply(przetworz_opis)

# Filtry
st.sidebar.header("Filtry")
# Tytuł oferty
search_title = st.sidebar.text_input("Szukaj po tytule oferty", value="")

# Marka
brand_options = data["Marka"].dropna().unique() if "Marka" in data.columns else []
selected_brand = st.sidebar.multiselect("Wybierz markę", brand_options, default=brand_options)

# Status oferty
status_options = data["Status oferty"].dropna().unique() if "Status oferty" in data.columns else []
selected_status = st.sidebar.multiselect("Wybierz status oferty", status_options, default=status_options)

# Liczba przedmiotów
min_items = st.sidebar.number_input(
    "Minimalna liczba przedmiotów",
    min_value=0,
    value=int(data["Liczba przedmiotów"].min()) if "Liczba przedmiotów" in data.columns else 0,
)

max_items = st.sidebar.number_input(
    "Maksymalna liczba przedmiotów",
    min_value=0,
    value=int(data["Liczba przedmiotów"].max()) if "Liczba przedmiotów" in data.columns else 0,
)

# Filtrowanie danych
filtered_data = data.copy()

# Filtrowanie po tytule oferty
if search_title:
    filtered_data = filtered_data[filtered_data["Tytuł oferty"].str.contains(search_title, case=False, na=False)]

# Filtrowanie pozostałych kolumn
if "Marka" in data.columns:
    filtered_data = filtered_data[filtered_data["Marka"].isin(selected_brand)]

if "Status oferty" in data.columns:
    filtered_data = filtered_data[filtered_data["Status oferty"].isin(selected_status)]

if "Liczba przedmiotów" in data.columns:
    filtered_data = filtered_data[
        (filtered_data["Liczba przedmiotów"] >= min_items) & (filtered_data["Liczba przedmiotów"] <= max_items)
    ]

# Wyświetl tabelę z przetworzonymi opisami
st.title("Tabela z przetworzonymi opisami i filtrami")
st.write("Tabela zawiera oryginalne dane oraz przetworzony opis w nowej kolumnie.")

# Wyświetl liczbę pozycji
st.write(f"Liczba pozycji po filtrach: {len(filtered_data)}")

st.dataframe(filtered_data)

# Pobieranie przetworzonej tabeli
st.download_button(
    label="Pobierz przetworzoną tabelę",
    data=filtered_data.to_csv(index=False).encode("utf-8"),
    file_name="przetworzona_tabela.csv",
    mime="text/csv",
)
