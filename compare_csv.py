import streamlit as st
import pandas as pd

# Funkcja do porównywania danych
def compare_csv_files(df1, df2, id_column):
    # Łączenie danych na podstawie ID oferty
    merged = pd.merge(df1, df2, on=id_column, how='outer', suffixes=('_original', '_new'), indicator=True)
    
    # Znalezienie różnic
    added = merged[merged['_merge'] == 'right_only']
    removed = merged[merged['_merge'] == 'left_only']
    updated = merged[(merged['_merge'] == 'both') & (merged.filter(like='_original').ne(merged.filter(like='_new')).any(axis=1))]

    return added, removed, updated

# Aplikacja Streamlit
st.title("Porównanie dwóch plików CSV")

# Wgrywanie plików CSV
uploaded_file1 = st.file_uploader("Wgraj pierwszy plik CSV (test.csv)", type=["csv"], key="file1")
uploaded_file2 = st.file_uploader("Wgraj drugi plik CSV (test2.csv)", type=["csv"], key="file2")

if uploaded_file1 and uploaded_file2:
    # Wczytywanie plików do DataFrame
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)

    st.subheader("Podgląd pierwszego pliku")
    st.dataframe(df1)

    st.subheader("Podgląd drugiego pliku")
    st.dataframe(df2)

    # Wybór kolumny do porównania
    id_column = st.selectbox("Wybierz kolumnę ID do porównania", options=df1.columns.intersection(df2.columns))

    if id_column:
        # Porównanie plików
        added, removed, updated = compare_csv_files(df1, df2, id_column)

        # Wyświetlanie wyników
        st.subheader("Dodane rekordy")
        st.dataframe(added)

        st.subheader("Usunięte rekordy")
        st.dataframe(removed)

        st.subheader("Zmienione rekordy")
        st.dataframe(updated)

else:
    st.info("Wgraj oba pliki CSV, aby rozpocząć porównanie.")
