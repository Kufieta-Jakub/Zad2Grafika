# Zad2Grafika

Zadanie #2 - analiza jakości zdjęć na podstawie automatycznej oceny histogramu (Akademia WSB).

Program wczytuje zdalne zdjęcie, wyświetla histogram dla całego zdjęcia oraz dla kanałów R, G i B, a następnie na podstawie wartości histogramu ocenia jakość zdjęcia. Wykryte wady program próbuje poprawić i pokazuje wynik obok oryginału.

## Co robi program

1. Wczytuje zdalne zdjęcie (`urllib`). Jeśli strona nie pozwala na pobranie, wypisuje komunikat o błędzie.
2. Wyświetla histogram całego zdjęcia (jasność) oraz osobno kanałów R, G i B (`matplotlib`).
3. Ocenia jakość zdjęcia na podstawie statystyk histogramu: niedoświetlone, prześwietlone, niski kontrast, obcięte cienie, obcięte światła, dominanta kolorystyczna.
4. Poprawia wykryte wady (zadanie dodatkowe) i wyświetla zdjęcie przed i po poprawie wraz z histogramami.

## Wymagania

- Python 3.8 lub nowszy
- Biblioteki: `opencv-python`, `matplotlib`, `numpy`

Przed uruchomieniem programu należy zainstalować poniższe biblioteki:

```bash
pip install opencv-python matplotlib numpy
```

## Zmiana obrazu

Na początku pliku `zadanie2_histogram.py` znajduje się zmienna `SOURCE`. Można w niej podać adres URL zdjęcia albo ścieżkę do pliku lokalnego:

```python
SOURCE = "link do obrazu"
```

Obrazy pochodzą z [Wikimedia Commons](https://commons.wikimedia.org).

## Użyte biblioteki

| Biblioteka | Zastosowanie |
|---|---|
| `urllib` | pobranie zdjęcia zdalnego |
| `opencv-python` (`cv2`) | histogramy, konwersje kolorów |
| `numpy` | statystyki histogramu, operacje na macierzach |
| `matplotlib` | wyświetlanie zdjęć i histogramów |

## Autor

Projekt wykonany w ramach zajęć - Jakub Kufieta Gr1
