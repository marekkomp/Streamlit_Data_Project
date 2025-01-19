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
selected_brand = st.sidebar.multiselect(
    "Wybierz markę", 
    options=brand_options, 
    default=brand_options if len(brand_options) > 0 else [],
    help="Odznacz wszystkie, aby wybrać wszystkie dostępne opcje"
)
if not selected_brand and brand_options:
    selected_brand = brand_options

# Typ pamięci RAM
ram_type_options = data["Typ pamięci RAM"].dropna().unique() if "Typ pamięci RAM" in data.columns else []
selected_ram_type = st.sidebar.multiselect(
    "Wybierz typ pamięci RAM", 
    options=ram_type_options, 
    default=ram_type_options if len(ram_type_options) > 0 else []
)
if not selected_ram_type and ram_type_options:
    selected_ram_type = ram_type_options

# Wielkość pamięci RAM
ram_size_options = data["Wielkość pamięci RAM"].dropna().unique() if "Wielkość pamięci RAM" in data.columns else []
selected_ram_size = st.sidebar.multiselect(
    "Wybierz wielkość pamięci RAM", 
    options=ram_size_options, 
    default=ram_size_options if len(ram_size_options) > 0 else []
)
if not selected_ram_size and ram_size_options:
    selected_ram_size = ram_size_options

# Typ dysku twardego
hdd_type_options = data["Typ dysku twardego"].dropna().unique() if "Typ dysku twardego" in data.columns else []
selected_hdd_type = st.sidebar.multiselect(
    "Wybierz typ dysku twardego", 
    options=hdd_type_options, 
    default=hdd_type_options if len(hdd_type_options) > 0 else []
)
if not selected_hdd_type and hdd_type_options:
    selected_hdd_type = hdd_type_options

# Filtrowanie danych
filtered_data = data.copy()

# Filtrowanie po tytule oferty
if search_title:
    filtered_data = filtered_data[filtered_data["Tytuł oferty"].str.contains(search_title, case=False, na=False)]

# Filtrowanie po marce
if "Marka" in data.columns:
    filtered_data = filtered_data[filtered_data["Marka"].isin(selected_brand)]

# Filtrowanie po typie pamięci RAM
if "Typ pamięci RAM" in data.columns:
    filtered_data = filtered_data[filtered_data["Typ pamięci RAM"].isin(selected_ram_type)]

# Filtrowanie po wielkości pamięci RAM
if "Wielkość pamięci RAM" in data.columns:
    filtered_data = filtered_data[filtered_data["Wielkość pamięci RAM"].isin(selected_ram_size)]

# Filtrowanie po typie dysku twardego
if "Typ dysku twardego" in data.columns:
    filtered_data = filtered_data[filtered_data["Typ dysku twardego"].isin(selected_hdd_type)]

# Wyświetl tabelę z przetworzonymi opisami
st.title("Tabela z przetworzonymi opisami i filtrami")
st.write("Tabela zawiera oryginalne dane oraz przetworzony opis w nowej kolumnie:")
st.dataframe(filtered_data)

# Pobieranie przetworzonej tabeli
st.download_button(
    label="Pobierz przetworzoną tabelę",
    data=filtered_data.to_csv(index=False).encode("utf-8"),
    file_name="przetworzona_tabela.csv",
    mime="text/csv",
)
