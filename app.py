import streamlit as st
import pandas as pd

# Wczytywanie danych
try:
    # Wczytaj dane z CSV
    data = pd.read_csv("1.csv")

    # Wyciągnięcie kluczowych kolumn
    kluczowe_kolumny = ["Status oferty", "Liczba sztuk", "Cena PL", "Tytuł oferty"]
    dane_filtr = data[kluczowe_kolumny]

    # Wyświetlanie danych
    st.title("Podgląd danych ofert")
    st.write("Poniżej znajdują się dane z wybranych kolumn:")
    st.write(dane_filtr.head(50))  # Wyświetl tylko 50 pierwszych wierszy

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except Exception as e:
    st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")
