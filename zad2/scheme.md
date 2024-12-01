# Polecenie

Napisz zestaw dwóch programów – klienta i serwera komunikujących się poprzez TCP. Transmitowany strumień danych powinien być stosunkowo duży, nie mniej niż 100 kB.

Klient TCP wysyła złożoną strukturę danych. Przykładowo: tworzymy w pamięci listę jednokierunkową lub drzewo binarne struktur zawierających (oprócz danych organizacyjnych) pewne dane dodatkowe: np. liczbę całkowitą 16-o bitową, liczbę całkowitą 32-u bitową oraz napis zmiennej i ograniczonej długości. Serwer napisany w Pythonie/C powinien te dane odebrać, dokonać poprawnego „odpakowania” tej struktury i wydrukować jej pola (być może w skróconej postaci, aby uniknąć nadmiaru wyświetlanych danych). Klient oraz serwer powinny być napisane w różnych językach.

# Rozwiązanie
## Języki
Klient ma prostsze zadanie do wykonania - wygenerować dane, spakować i przesłać.
Serwer musi je odpakować, zbudować i dodatkowo przetworzyć. 
Praca z napisami w C jest mozolna: proponuję Python na serwer, C na klienta

## Struktura
Lista jednokierunkowa, w wypisywaniu pola będą zapisane jeden po drugim

## Element struktury (węzeł)

i32 - id węzła
i16 - długość napisu
char* - napis ograniczonej (ale zmiennej) długości, max 50

## Generacja danych
n