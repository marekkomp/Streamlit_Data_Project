import streamlit as st
import pandas as pd

# Funkcja do porównywania danych
def compare_csv_files(df1, df2):
    # Znajdowanie różnic
    df1_set = set([tuple(row) for row in df1.values])
    df2_set = set([tuple(row) for row in df2.values])

    differences = df2_set - df1_set
    differences_df = pd.DataFrame(list(differences), columns=df2.columns)

    return differences_df

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
