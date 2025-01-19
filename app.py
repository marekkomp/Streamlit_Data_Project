import streamlit as st
import pandas as pd
import re  # Do pracy z wyrażeniami regularnymi

# Funkcja do filtrowania opisu
def filtruj_opis(opis):
    if isinstance(opis, str):
        # Zatrzymaj tekst do pierwszego wystąpienia "items":[{"type":"IMAGE"
        wzorzec = r'{"items":\[{"type":"IMAGE".*'
        opis_skrócony = re.split(wzorzec, opis)[0]

        # Usuń wszystko poza tekstem w liniach
        opis_czysty = re.sub(r'[^a-zA-Z0-9.,<>/=" ]', '', opis_skrócony)
        return opis_czysty.strip()
    return ""

# Wczytywanie danych
try:
    # Wczytaj plik CSV
    data = pd.read_csv("1.csv")

    st.title("Aplikacja z filtrowaniem opisów")
    st.write("Filtrowanie danych oraz modyfikowanie kolumny opisowej zgodnie z podanymi regułami.")

    # Dodaj filtr dla opisów
    if "Opis oferty" in data.columns:
        data["Opis oferty (przefiltrowany)"] = data["Opis oferty"].apply(filtruj_opis)

    # Wyświetl dane z przefiltrowanym opisem
    st.dataframe(data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except KeyError as e:
    st.error(f"Brakuje kolumny w danych: {e}")

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
