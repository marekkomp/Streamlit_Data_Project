import streamlit as st
import pandas as pd

# Funkcja do porównywania danych
def compare_csv_files(df1, df2):
    id_column = 'ID oferty'

    # Usuwamy nadmiarowe białe znaki w danych
    df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Wiersze, które są tylko w drugim pliku (nowe ID)
    new_rows = df2[~df2[id_column].isin(df1[id_column])]

    # Wiersze, które są w obu plikach, ale mają różne dane
    common_ids = df1[df1[id_column].isin(df2[id_column])]
    differences = []

    for _, row in common_ids.iterrows():
        id_value = row[id_column]
        df1_row = row
        df2_row = df2[df2[id_column] == id_value].iloc[0]

        # Porównujemy wartości w kolumnach
        diff_row = {}
        for col in df1.columns:
            if df1_row[col] != df2_row[col]:
                # Dodajemy pogrubienie i opis różnicy
                diff_row[col] = f"**{df2_row[col]}** (zmienione z {df1_row[col]})"
            else:
                diff_row[col] = df2_row[col]

        if diff_row:
            differences.append(diff_row)

    # Tworzymy DataFrame z różnicami
    changed_rows = pd.DataFrame(differences, columns=df2.columns)

    # Łączenie nowych wierszy i zmienionych wierszy
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
        # Wyświetlamy z obsługą Markdown dla pogrubienia
        st.write(differences.to_markdown(), unsafe_allow_html=False)
    else:
        st.write("Brak różnic między plikami.")

else:
    st.info("Wgraj oba pliki CSV, aby rozpocząć porównanie.")
