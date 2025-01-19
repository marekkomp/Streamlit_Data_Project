import streamlit as st
import pandas as pd

# Wczytywanie danych z CSV
try:
    data = pd.read_csv("1.csv")  # Upewnij się, że nazwa pliku się zgadza

    st.title("Podgląd danych")
    st.write("Poniżej znajdują się dane z pliku CSV:")
    st.write(data)

except FileNotFoundError:
    st.error("Nie znaleziono pliku CSV. Upewnij się, że plik jest w repozytorium i nazwa jest poprawna.")

except Exception as e:
    st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")
