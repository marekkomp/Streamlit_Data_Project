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

        return "\n\n".join(tekstów)
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
selected_brand = st.sidebar.multiselect("Wybierz markę", brand_options)

# Status oferty
status_options = data["Status oferty"].dropna().unique() if "Status oferty" in data.columns else []
selected_status = st.sidebar.multiselect("Wybierz status oferty", status_options)

# Kategoria główna
category_options = data["Kategoria główna"].dropna().unique() if "Kategoria główna" in data.columns else []
selected_category = st.sidebar.multiselect("Wybierz kategorię główną", category_options)

# Typ pamięci RAM
ram_type_options = data["Typ pamięci RAM"].dropna().unique() if "Typ pamięci RAM" in data.columns else []
selected_ram_type = st.sidebar.multiselect("Wybierz typ pamięci RAM", ram_type_options)

# Wielkość pamięci RAM
ram_size_options = data["Wielkość pamięci RAM"].dropna().unique() if "Wielkość pamięci RAM" in data.columns else []
selected_ram_size = st.sidebar.multiselect("Wybierz wielkość pamięci RAM", ram_size_options)

# Typ dysku twardego
hdd_type_options = data["Typ dysku twardego"].dropna().unique() if "Typ dysku twardego" in data.columns else []
selected_hdd_type = st.sidebar.multiselect("Wybierz typ dysku twardego", hdd_type_options)

# Pojemność dysku [GB]
hdd_capacity_options = data["Pojemność dysku [GB]"].dropna().unique() if "Pojemność dysku [GB]" in data.columns else []
selected_hdd_capacity = st.sidebar.multiselect("Wybierz pojemność dysku [GB]", hdd_capacity_options)

# Model procesora.1
cpu_model_options = data["Model procesora.1"].dropna().unique() if "Model procesora.1" in data.columns else []
selected_cpu_model = st.sidebar.multiselect("Wybierz model procesora", cpu_model_options)

# Seria procesora
cpu_series_options = data["Seria procesora"].dropna().unique() if "Seria procesora" in data.columns else []
selected_cpu_series = st.sidebar.multiselect("Wybierz serię procesora", cpu_series_options)

# Przekątna ekranu ["]
screen_size_options = data["Przekątna ekranu [\"]"].dropna().unique() if "Przekątna ekranu [\"]" in data.columns else []
selected_screen_size = st.sidebar.multiselect("Wybierz przekątną ekranu [\"]", screen_size_options)

# Liczba rdzeni procesora
core_count_options = data["Liczba rdzeni procesora"].dropna().unique() if "Liczba rdzeni procesora" in data.columns else []
selected_core_count = st.sidebar.multiselect("Wybierz liczbę rdzeni procesora", core_count_options)

# Rodzaj karty graficznej
gpu_type_options = data["Rodzaj karty graficznej"].dropna().unique() if "Rodzaj karty graficznej" in data.columns else []
selected_gpu_type = st.sidebar.multiselect("Wybierz rodzaj karty graficznej", gpu_type_options)

# Rozdzielczość (px)
resolution_options = data["Rozdzielczość (px)"].dropna().unique() if "Rozdzielczość (px)" in data.columns else []
selected_resolution = st.sidebar.multiselect("Wybierz rozdzielczość (px)", resolution_options)

# Cena PL
min_price = st.sidebar.number_input(
    "Minimalna cena (PLN)",
    min_value=0.0,
    value=0.0,
)

max_price = st.sidebar.number_input(
    "Maksymalna cena (PLN)",
    min_value=0.0,
    value=float(data["Cena PL"].max()) if "Cena PL" in data.columns else 0.0,
)

# Filtrowanie danych
filtered_data = data.copy()

if search_title:
    filtered_data = filtered_data[filtered_data["Tytuł oferty"].str.contains(search_title, case=False, na=False)]

if "Marka" in data.columns:
    if selected_brand:
        filtered_data = filtered_data[filtered_data["Marka"].isin(selected_brand)]

if "Status oferty" in data.columns:
    if selected_status:
        filtered_data = filtered_data[filtered_data["Status oferty"].isin(selected_status)]

if "Kategoria główna" in data.columns:
    if selected_category:
        filtered_data = filtered_data[filtered_data["Kategoria główna"].isin(selected_category)]

if "Typ pamięci RAM" in data.columns:
    if selected_ram_type:
        filtered_data = filtered_data[filtered_data["Typ pamięci RAM"].isin(selected_ram_type)]

if "Wielkość pamięci RAM" in data.columns:
    if selected_ram_size:
        filtered_data = filtered_data[filtered_data["Wielkość pamięci RAM"].isin(selected_ram_size)]

if "Typ dysku twardego" in data.columns:
    if selected_hdd_type:
        filtered_data = filtered_data[filtered_data["Typ dysku twardego"].isin(selected_hdd_type)]

if "Pojemność dysku [GB]" in data.columns:
    if selected_hdd_capacity:
        filtered_data = filtered_data[filtered_data["Pojemność dysku [GB]"].isin(selected_hdd_capacity)]

if "Model procesora.1" in data.columns:
    if selected_cpu_model:
        filtered_data = filtered_data[filtered_data["Model procesora.1"].isin(selected_cpu_model)]

if "Seria procesora" in data.columns:
    if selected_cpu_series:
        filtered_data = filtered_data[filtered_data["Seria procesora"].isin(selected_cpu_series)]

if "Przekątna ekranu [\"]" in data.columns:
    if selected_screen_size:
        filtered_data = filtered_data[filtered_data["Przekątna ekranu [\"]"].isin(selected_screen_size)]

if "Liczba rdzeni procesora" in data.columns:
    if selected_core_count:
        filtered_data = filtered_data[filtered_data["Liczba rdzeni procesora"].isin(selected_core_count)]

if "Rodzaj karty graficznej" in data.columns:
    if selected_gpu_type:
        filtered_data = filtered_data[filtered_data["Rodzaj karty graficznej"].isin(selected_gpu_type)]

if "Rozdzielczość (px)" in data.columns:
    if selected_resolution:
        filtered_data = filtered_data[filtered_data["Rozdzielczość (px)"].isin(selected_resolution)]

if "Cena PL" in data.columns:
    filtered_data = filtered_data[
        (filtered_data["Cena PL"] >= min_price) & (filtered_data["Cena PL"] <= max_price)
    ]

# Wyświetl tabelę z przetworzonymi opisami
st.title("Tabela z przetworzonymi opisami i filtrami")
st.write("Tabela zawiera oryginalne dane oraz przetworzony opis w nowej kolumnie:")
st.dataframe(filtered_data)

# Wyświetl liczbę wierszy pod tabelą
st.write(f"Liczba wierszy po zastosowaniu filtrów: {len(filtered_data)}")

# Pobieranie przetworzonej tabeli
st.download_button(
    label="Pobierz przetworzoną tabelę",
    data=filtered_data.to_csv(index=False).encode("utf-8"),
    file_name="przetworzona_tabela.csv",
    mime="text/csv",
)
