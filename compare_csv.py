import streamlit as st
import pandas as pd

# Funkcja do porównywania danych
def compare_csv_files(df1, df2):
    id_column = 'ID oferty'

    # Wiersze, które są tylko w drugim pliku (nowe ID)
    new_rows = df2[~df2[id_column].isin(df1[id_column])]

    # Łączenie danych na podstawie ID oferty, aby znaleźć różnice w istniejących ID
    merged = pd.merge(df1, df2, on=id_column, how='inner', suffixes=('_file1', '_file2'))

    # Znalezienie różnic w kolumnach oprócz ID
    different_rows = merged[merged.filter(like='_file1').ne(merged.filter(like='_file2')).any(axis=1)]

    # Pobranie tylko zmienionych wierszy z drugiego pliku
    changed_rows = df2[df2[id_column].isin(different_rows[id_column])]

    # Łączenie nowych wierszy i różnic w istniejących ID
    result = pd.concat([new_rows, changed_rows], ignore_index=True)

    return result

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

    # Porównanie plików
    differences = compare_csv_files(df1, df2)

    # Wyświetlanie wyników
    st.subheader("Różnice między plikami")
    if not differences.empty:
        st.dataframe(differences)
    else:
        st.write("Brak różnic między plikami.")

else:
    st.info("Wgraj oba pliki CSV, aby rozpocząć porównanie.")
