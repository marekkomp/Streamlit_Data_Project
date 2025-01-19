import streamlit as st
import pandas as pd

# Wczytywanie danych
data = pd.read_excel("offers_2025-01-19(1).xlsm")  # Podaj dokładną nazwę pliku Excel

# Interfejs aplikacji
st.title("Analiza danych ofert")
st.sidebar.header("Filtry")

# Filtr aktywnych ofert
aktywnosc = st.sidebar.checkbox("Pokaż tylko aktywne oferty")
if aktywnosc:
    data = data[data['Status'] == 'Aktywna']  # Zmień 'Status' na odpowiednią kolumnę w pliku

# Wyświetlanie tabeli danych
st.subheader("Dane ofert")
st.write(data)

# Liczba przedmiotów
if 'Liczba Przedmiotów' in data.columns:
    liczba_przedmiotow = data['Liczba Przedmiotów'].sum()  # Zmień nazwę kolumny na odpowiednią
    st.write(f"Łączna liczba przedmiotów: {liczba_przedmiotow}")
else:
    st.write("Brak kolumny 'Liczba Przedmiotów' w danych.")
