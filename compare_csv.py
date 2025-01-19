import streamlit as st
import pandas as pd
import numpy as np

# Funkcja do porównywania danych
def compare_csv_files(df1, df2, id_column):
    # Łączenie danych na podstawie ID oferty
    merged = pd.merge(df1, df2, on=id_column, how='outer', suffixes=('_file1', '_file2'), indicator=True)

    # Znalezienie różnic tylko w wierszach o wspólnych ID
    differences = merged[(merged['_merge'] == 'both') & (merged.filter(like='_file1').ne(merged.filter(like='_file2')).any(axis=1))]

    # Tworzenie DataFrame z różnicami
    diff_highlighted = differences.copy()
    for col in df1.columns:
        if col != id_column and f"{col}_file1" in differences.columns and f"{col}_file2" in differences.columns:
            diff_highlighted[col] = np.where(
                differences[f"{col}_file1"] != differences[f"{col}_file2"],
                f"<b>{differences[f'{col}_file2']}</b>",
                differences[f"{col}_file2"]
            )

    # Zwrócenie wyników tylko z wyróżnionymi różnicami
    result = diff_highlighted[[col for col in differences.columns if col.endswith('_file2') or col == id_column]]
    result.columns = [col.replace('_file2', '') for col in result.columns]  # Usunięcie sufiksów dla przejrzystości

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

    # Wybór kolumny ID do porównania
    id_column = st.selectbox("Wybierz kolumnę ID do porównania", options=df1.columns.intersection(df2.columns))

    if id_column:
        # Porównanie plików
        differences = compare_csv_files(df1, df2, id_column)

        # Wyświetlanie wyników
        st.subheader("Różnice między plikami")
        if not differences.empty:
            st.write("Tabela z wyróżnionymi różnicami:")
            st.write(differences.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.write("Brak różnic między plikami.")

else:
    st.info("Wgraj oba pliki CSV, aby rozpocząć porównanie.")
