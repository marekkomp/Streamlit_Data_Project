import streamlit as st
import pandas as pd

# Wczytaj dane z pliku CSV
plik_csv = "1.csv"
try:
    data = pd.read_csv(plik_csv)
    st.write("Plik CSV załadowany pomyślnie!")
except Exception as e:
    st.error(f"Błąd podczas wczytywania pliku: {e}")
    st.stop()

# Wyświetl pierwsze 10 wierszy
st.write("Pierwsze 10 wierszy pliku CSV:")
st.dataframe(data.head(10))

# Sprawdź brakujące wartości w kluczowych kolumnach
kluczowe_kolumny = ["ID oferty", "Opis oferty", "Tytuł oferty"]
st.write("Czy kluczowe kolumny zawierają puste wartości w pierwszych wierszach?")
for kolumna in kluczowe_kolumny:
    if kolumna in data.columns:
        st.write(f"Kolumna '{kolumna}':")
        st.write(data[kolumna].head(10).isnull())
    else:
        st.warning(f"Kolumna '{kolumna}' nie istnieje w danych.")

# Wyświetl typy danych dla wszystkich kolumn
st.write("Typy danych w pliku CSV:")
st.write(data.dtypes)

# Podsumowanie brakujących danych
st.write("Podsumowanie brakujących danych:")
st.write(data.isnull().sum())

# Informacje o danych
st.write("Informacje o danych:")
st.text(data.info())
