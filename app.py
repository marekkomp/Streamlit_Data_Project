import streamlit as st
import pandas as pd

# Wczytywanie danych
try:
    # Użyj dokładnej nazwy pliku, który wrzuciłeś do repozytorium
    data = pd.read_excel("offers_2025-01-19(1).xlsm")

    # Wyświetlanie danych w aplikacji
    st.title("Podgląd danych")
    st.write("Poniżej znajdują się dane z pliku Excel:")
    st.write(data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku Excel. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except Exception as e:
    st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")
