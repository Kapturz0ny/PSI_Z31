# Zadanie 1.1 Komunikacja UDP

Realizacja komunikacji protokołem UDP między klientem, a serwerem, oba zrealizowane zarówno w języku C jak i Python. Możliwe uruchomienie "między-platformowe" np. klient w Python z serwerem w C.

## Schemat Komunikacji

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


## Uruchomienie

### Jednolinijkowe
`docker compose up --build` buduje, a następnie uruchamia wszystkie kontenery

**Zalecane** jest jednak wcześniejsze zbudowanie wszystkich kontenerów poleceniem `docker compose build`
Następnie można uruchomić wybraną komunikację:
- `docker compose up z31_pserver_pclient` serwer Python, klient Python
- `docker compose up z31_pserver_cclient` serwer Python, klient C
- `docker compose up z31_cserver_pclient` serwer C, klient Python
- `docker compose up z31_cserver_cclient` serwer C, klient C
- `docker compose up z31_pserver_pclient_test` serwer Python, klient Python w konfiguracji testowej
(sprawdzenie maksymalnego rozmiaru datagramu)

Oraz
- `docker compose up z31_pserver` serwer Python
- `docker compose up z31_cserver` serwer C