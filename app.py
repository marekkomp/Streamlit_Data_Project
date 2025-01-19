import streamlit as st
import pandas as pd

# Wczytywanie danych
try:
    # Wczytaj cały plik CSV
    data = pd.read_csv("test.csv")

    # Wyświetlanie danych
    st.title("Pełny podgląd danych")
    st.write("Poniżej znajdują się wszystkie kolumny i wiersze danych z pliku CSV:")
    st.dataframe(data)  # Dynamiczny podgląd tabeli

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except Exception as e:
    st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")
