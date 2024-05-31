Autor: Franciszek Kępski
numer studenta: s25925


# Dokumentacja Projektu Szachów w Pythonie

## Wprowadzenie

Projekt Szachów w Pythonie to gra szachowa zaimplementowana w języku Python, umożliwiająca rozgrywkę pomiędzy dwoma graczami. Projekt ten został stworzony na przedmiot PPY na uczelni PJATK. Aplikacja oferuje pełną funkcjonalność klasycznej gry w szachy, w tym poprawne ruchy figur, wykrywanie szachów, szach-matów oraz patów.

## Funkcjonalności

1. **Interfejs użytkownika**:
   - Graficzny interfejs użytkownika (GUI),
   - Wyświetlanie planszy szachowej oraz figur.
   - Możliwość customizacji wyglądu GUI w opcjach
   - Interaktywne zaznaczanie i przemieszczanie figur za pomocą klawiszy wsad lub strzałek i spacji/enter.

2. **Logika gry**:
   - Implementacja zasad gry w szachy, w tym ruchów wszystkich figur (król, hetman, wieża, goniec, skoczek, pion).
   - Wykrywanie szacha, szach-mata oraz pata.
   - Zapisywanie stanu gry do pliku
   - Implementacja pinowania figur
   - [TODO] Obsługa promocji piona, roszady oraz bicia w przelocie.

## Struktura Kodu

1. **Główne moduły**:
   - `main.py`: Plik startowy uruchamiający grę oraz inicjujący główną pętlę gry.
   - `ChessEngine.py`: Klasa odpowiedzialna wykonywania ruchów oraz pilnowanie zasad szachów.
   - `Board.py`: Klasa odpowiedzialna za reprezentację planszy.

## Instalacja i Uruchomienie

### Wymagania

- Python 3.7 lub nowszy
- pynput 1.7.7

### Kroki instalacji

1. Zainstaluj Pygame:
   ```bash
   pip install pynput
   ```
2. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/uzytkownik/projekt-szachy.git
   ```
3. Przejdź do katalogu projektu:
   ```bash
   cd projekt-szachy
   ```
4. Uruchom grę:
   ```bash
   python main.py
   ```

## Użycie
Starowania - wsad, strzałki, enter, spacja

Po uruchomieniu gry pojawi się okno z planszą szachową. Gracze mogą na przemian wykonywać ruchy, zaznaczając figury i przestawiając je na wybrane pola. Gra automatycznie wykrywa nielegalne ruchy oraz informuje o zakończeniu gry w przypadku szach-mata lub pata.