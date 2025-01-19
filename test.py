import pandas as pd

# Wczytaj dane z pliku CSV
plik_csv = "1.csv"
data = pd.read_csv(plik_csv)

# Wyświetl pierwsze 10 wierszy
print("Pierwsze 10 wierszy pliku CSV:")
print(data.head(10))

# Sprawdź, czy pierwsze wiersze mają puste kluczowe kolumny
kluczowe_kolumny = ["ID oferty", "Opis oferty", "Tytuł oferty"]
print("\nCzy kluczowe kolumny zawierają puste wartości w pierwszych wierszach?")
for kolumna in kluczowe_kolumny:
    if kolumna in data.columns:
        print(f"Kolumna '{kolumna}':")
        print(data[kolumna].head(10).isnull())
    else:
        print(f"Kolumna '{kolumna}' nie istnieje w danych.")

# Wyświetl typy danych dla wszystkich kolumn
print("\nTypy danych w pliku CSV:")
print(data.dtypes)

# Sprawdź, czy wiersze mają ukryte problemy
print("\nPodsumowanie brakujących danych:")
print(data.isnull().sum())

# Wyświetl ogólne informacje o danych
print("\nInformacje o danych:")
print(data.info())
