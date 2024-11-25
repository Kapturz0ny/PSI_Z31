# Zadanie 1.2 Niezawodna transmisja protokołem UDP

Realizacja komunikacji protokołem UDP między klientem, a serwerem, zrealizowana w języku Python. Komunikacja uwzględnia możliwość gubienia przesyłanych datagramów. Wprowadzone zakłócenie to 1000ms opóźnienia wysłania datagramu z odchyleniem do 500ms oraz prawdopodobieństwo 50%, że zostanie zgubiony. Wtedy taki zgubiony datagram jest wykrywany i retransmitowany co zapewnia niezawodność transmisji.

## Schemat Komunikacji
Klient wysyła po kolei datagramy o zadanym rozmiarze i rosnących numerach sekwencyjnych.
Jeśli nie otrzyma odpowiedzi od serwera, która potwierdza otrzymanie przez serwer wysłanego datagramu (o tym samym numerze sekwencyjnym) w ustalonym odgórnie czasie (domyślnie 1s), datagram jest wysyłany ponownie aż do skutku.

Serwer czeka w pętli na komunikat, sprawdza czy jego rozmiar zgadza się z rozmiarem przekazanym w komunikacie, po czym przesyła odpowiedź ACK potwierdzającą otrzymanie datagramu wraz z jego numerem sekwencyjnym.

### Struktura datagramu klienta:
- 2 bajty - rozmiar całego datagramu (n)
- 1 bajt - nr sekwencyjny datagramu
- n-3 bajty - kolejne litery A-Z, powtarzające się
- n = 512 w tym zadaniu

### Struktura datagramu serwera:
- b'ACK #\<number\>' 
    - \<number\> to numer datagramu jaki otrzymał


## Opis konfiguracji testowej

Sieć: docker network o nazwie `z31_network`

Nie deklarujemy adresów IP wprost, korzystamy z nazw kontenerów i resolvera DNS w programach.

Port: 8000

Symulacja zakłóceń sieciowych: polecenie
```
tc qdisc add dev eth0 root netem delay 1000ms 500ms loss 50%
```


## Uruchomienie

### Jednolinijkowe
`docker compose up --build` buduje, a następnie uruchamia wszystkie kontenery

**Zalecane** jest jednak wcześniejsze zbudowanie wszystkich kontenerów poleceniem `docker compose build`
Następnie można uruchomić w oddzielnych terminalach:
- `docker compose up z31_server` serwer Python
- `docker compose up z31_client` klient Python
