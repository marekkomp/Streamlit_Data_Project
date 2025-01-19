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

# Wczytywanie danych tylko dla jednej pozycji
def wczytaj_dane_dla_id(id_pozycji):
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")
    
    # Znajdź wiersz z wybranym ID
    if "ID" in data.columns:
        wybrana_pozycja = data[data["ID"] == id_pozycji]
        if wybrana_pozycja.empty:
            st.error(f"Nie znaleziono pozycji o ID {id_pozycji}")
            return None
        return wybrana_pozycja
    else:
        st.error("Kolumna 'ID' nie została znaleziona w danych.")
        return None

# Wczytaj dane dla konkretnego ID
wybrany_id = 11132647668
data = wczytaj_dane_dla_id(wybrany_id)

if data is not None:
    # Przetwórz opis tylko dla tej pozycji
    if "Opis oferty" in data.columns:
        opis = data["Opis oferty"].iloc[0]
        przetworzony_opis = przetworz_opis_debug(opis)
        st.write(f"Przetworzony opis dla ID {wybrany_id}:")
        st.text(przetworzony_opis)
    else:
        st.error("Kolumna 'Opis oferty' nie została znaleziona w danych.")
