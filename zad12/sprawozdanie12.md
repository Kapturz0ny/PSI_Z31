# PSI zad 1.2 - sprawozdanie

24.11.2024

Zespół Z31:
- Marcin Bagnowski
- Maciej Kaniewski
- Tomasz Kurzela

Repozytorium GitHub:
[https://github.com/Kapturz0ny/PSI_Z31](https://github.com/Kapturz0ny/PSI_Z31)



# Treść Zadania:
**Z 1 Komunikacja UDP**
Napisz zestaw dwóch programów – klienta i serwera wysyłające datagramy UDP. Wykonaj ćwiczenie w kolejnych inkrementalnych wariantach (rozszerzając kod z poprzedniej wersji). Klient jak i serwer powinien być napisany zarówno w C jak i Pythonie (4 programy).
Sprawdzić i przetestować działanie „między-platformowe”, tj. klient w C z serwerem Python i vice versa.

**Z 1.2**
Wychodzimy z kodu z zadania 1.1, tym razem pakiety datagramu mają stałą wielkość, można przyjąć np. 512B. Należy zaimplementować prosty protokół niezawodnej transmisji, uwzględniający możliwość gubienia datagramów. Rozszerzyć protokół i program tak, aby gubione pakiety były wykrywane i retransmitowane. Wskazówka – „Bit alternate protocol”. Należy uruchomić program w środowisku symulującym błędy gubienia pakietów. (Informacja o tym, jak to zrobić znajduje się w skrypcie opisującym środowisko Dockera).

# Rozwiązanie

## Schemat Komunikacji
DO UZUPEŁNIENIA

### Struktura datagramu klienta:
- 2 bajty - rozmiar całego datagramu (n)
- n-2 bajty - kolejne litery A-Z, powtarzające się

### Struktura datagramu serwera:
- b'CORRECT datagram' - jeśli otrzymano poprawny datagram
- b'INCORRECT datagram' - wpp.


### Przykładowa komunikacja z perspektywy serwera:
1. received: 0x0 0x4 A B
2. sent: CORRECT datagram
3. received: 0x0 0x8 A B C
4. sent: INCORRECT datagram

## Opis konfiguracji testowej

Sieć: docker network o nazwie `z31_network`

Nie deklarujemy adresów IP wprost, korzystamy z nazw kontenerów i resolvera DNS w programach.

Port: 8000

# Uruchomienie i testowanie

## Instrukcja uruchomienia
DO UZUPEŁNIENIA

## Testowanie
DO UZUPEŁNIENIA

# Wnioski
DO UZUPEŁNIENIA
