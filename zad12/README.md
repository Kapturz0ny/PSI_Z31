# Zadanie 1.2 Niezawodna transmisja protokołem UDP

Realizacja komunikacji protokołem UDP między klientem, a serwerem, zrealizowana w języku Python. Komunikacja uwzględnia możliwość gubienia przesyłanych datagramów. Wprowadzone zakłócenie to 1000ms opóźnienia wysłania datagramu z odchyleniem do 500ms oraz prawdopodobieństwo 50%, że zostanie zgubiony. Wtedy taki zgubiony datagram jest wykrywany i retransmitowany co zapewnia niezawodność transmisji.

## Schemat Komunikacji

### Struktura datagramu klienta:
- rozmiar - 512 bajtów
- pierwsze 2 bajty - rozmiar całego datagramu (n)
- trzeci bajt - numer datagramu
- n-3 bajty - kolejne litery A-Z, powtarzające się

### Struktura datagramu serwera:
- b'CORRECT datagram' - jeśli otrzymano poprawny datagram
- b'INCORRECT datagram' - wpp.

### Przykładowa komunikacja z perspektywy serwera:
DO POPRAWIENIA

1. received: 0x0 0x4 A B
2. sent: CORRECT datagram
3. received: 0x0 0x8 A B C
4. sent: INCORRECT datagram


## Uruchomienie

### Jednolinijkowe
`docker compose up --build` buduje, a następnie uruchamia wszystkie kontenery

**Zalecane** jest jednak wcześniejsze zbudowanie wszystkich kontenerów poleceniem `docker compose build`
Następnie można uruchomić w oddzielnych terminalach:
- `docker compose up z31_server` serwer Python
- `docker compose up z31_client` klient Python
