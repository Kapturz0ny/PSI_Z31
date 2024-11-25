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

# Uruchomienie i testowanie

## Instrukcja uruchomienia
`docker compose up --build` - buduje i uruchamia kontener serwera i kontener klienta

## Testowanie

```
$ docker compose up --build
(...)
z31_server  | Server for zadanie 1.2
z31_server  | Will listen on  0.0.0.0 : 8000
z31_client  | Client for zadanie 1.2
z31_client  | Will send to  z31_server : 8000
z31_client  | Sending #1 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #1. Datagram will be resent...
z31_client  | Sending #1 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #1. Datagram will be resent...
z31_client  | Sending #1 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #1. Datagram will be resent...
z31_client  | Sending #1 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #1. Datagram will be resent...
z31_client  | Sending #1 datagram with size = 512
z31_server  | Received datagram  # 1
z31_client  | Sending #2 datagram with size = 512
z31_server  | Received datagram  # 2
z31_client  | Sending #3 datagram with size = 512
z31_server  | Received datagram #1 - datagram may be duplicated or out of order
z31_server  | Awaiting for datagram #3...
z31_client  | Sending #3 datagram with size = 512
z31_client  | Sending #4 datagram with size = 512
z31_server  | Received datagram  # 3
z31_server  | Received datagram #3 - datagram may be duplicated or out of order
z31_server  | Awaiting for datagram #4...
z31_client  | Sending #4 datagram with size = 512
z31_server  | Received datagram  # 4
z31_client  | Sending #5 datagram with size = 512
z31_server  | Received datagram #4 - datagram may be duplicated or out of order
z31_server  | Awaiting for datagram #5...
z31_client  | Sending #5 datagram with size = 512
z31_server  | Received datagram  # 5
z31_client  | Sending #6 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #6. Datagram will be resent...
z31_client  | Sending #6 datagram with size = 512
z31_server  | Received datagram  # 6
z31_client  | Sending #7 datagram with size = 512
z31_server  | Received datagram #6 - datagram may be duplicated or out of order
z31_server  | Awaiting for datagram #7...
z31_client  | Sending #7 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #7. Datagram will be resent...
z31_client  | Sending #7 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #7. Datagram will be resent...
z31_client  | Sending #7 datagram with size = 512
z31_server  | Received datagram  # 7
z31_client  | Sending #8 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #8. Datagram will be resent...
z31_client  | Sending #8 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #8. Datagram will be resent...
z31_client  | Sending #8 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #8. Datagram will be resent...
z31_client  | Sending #8 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #8. Datagram will be resent...
z31_client  | Sending #8 datagram with size = 512
z31_server  | Received datagram  # 8
z31_client  | Sending #9 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #9. Datagram will be resent...
z31_client  | Sending #9 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #9. Datagram will be resent...
z31_client  | Sending #9 datagram with size = 512
z31_server  | Received datagram  # 9
z31_client  | Sending #10 datagram with size = 512
z31_server  | Received datagram #9 - datagram may be duplicated or out of order
z31_server  | Awaiting for datagram #10...
z31_client  | Sending #10 datagram with size = 512
z31_client  | Timeout waiting for ACK for datagram #10. Datagram will be resent...
z31_client  | Sending #10 datagram with size = 512
z31_server  | Received datagram  # 10
```

# Wnioski
Nawet przy bardzo dużych zakłóceniach na łączu komunikacyjnym, prosty algorytm numerowania pakietów i retransmisji przy przekroczeniu limitu czasowego pozwala zapewnić pewną i bezbłędną komunikację przez UDP. Niestety nie ma żadnych mechanizmów korekcyjnych, przez co każda błędna wiadomość musi być retransmitowana.

Każdy datagram wysyłany jest osobno, przy oczekiwaniu na odpowiedź nie są wysyłane kolejne. To spowalnia komunikację. Pewnym rozwiązaniem byłoby zastosowanie przesuwnego okna (używanego np. w TCP).

Co prawda w tym wypadku zakłócenia były symulowane, jednak w rzeczywistości dochodzi do podobnych problemów z komunikacją i zawsze trzeba uwzględniać możliwość przekłamania części danych lub zgubienia całego datagramu. Przy użyciu protokołu UDP mechanizmy kontrolne są konieczne, żeby mieć gwarancję poprawnej komunikacji.
