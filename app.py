import streamlit as st
import pandas as pd
import json
import re
from html import unescape

# Funkcja do usuwania znaczników HTML
def clean_html(raw_html):
    clean_text = re.sub(r'<.*?>', '', raw_html)  # Usuwa znaczniki HTML
    return unescape(clean_text)  # Dekoduje encje HTML

# Funkcja do przetwarzania opisu
def process_description(raw_description):
    try:
        # Załaduj opis jako JSON
        description_json = json.loads(raw_description)
        clean_texts = []

        # Przejdź przez sekcje i wyciągnij treści tekstowe
        for section in description_json.get("sections", []):
            for item in section.get("items", []):
                if item.get("type") == "TEXT":  # Sprawdź, czy typ to tekst
                    raw_text = item.get("content", "")
                    clean_texts.append(clean_html(raw_text))  # Czyść HTML i dodaj

        # Połącz wyczyszczone fragmenty w jeden ciąg tekstu
        return "\n\n".join(clean_texts)

    except (json.JSONDecodeError, KeyError, TypeError):
        # W przypadku błędu zwróć surową wartość
        return "Nieprawidłowy format opisu"

# Wczytywanie danych
try:
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")

    st.title("Aplikacja do filtrowania i przetwarzania opisów")
    st.write("Filtrujemy dane i przekształcamy opis oferty na czytelny tekst.")

    # Filtrowanie i przetwarzanie danych
    if "Opis oferty" in data.columns:
        data["Przetworzony opis"] = data["Opis oferty"].fillna("").apply(process_description)

    # Wyświetlanie przetworzonych danych
    st.dataframe(data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except KeyError as e:
    st.error(f"Brakuje kolumny w danych: {e}")

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
