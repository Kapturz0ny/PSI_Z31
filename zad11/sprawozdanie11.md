# PSI zad 1.1 - sprawozdanie

18.11.2024

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

**Z 1.1**
Klient wysyła, a serwer odbiera datagramy o stałym rozmiarze (rzędu kilkuset bajtów). Datagramy powinny posiadać ustaloną formę danych. Przykładowo: pierwsze dwa bajty datagramu mogą zawierać informację o jego długości, a kolejne bajty kolejne litery A-Z powtarzające się wymaganą liczbę razy (ale można przyjąć inne rozwiązanie).  Odbiorca powinien weryfikować odebrany datagram i odsyłać odpowiedź  o ustalonym formacie. Klient powinien wysyłać kolejne datagramy o przyrastającej wielkości np. 1, 100, 200, 1000, 2000… bajtów.   Sprawdzić, jaki był maksymalny rozmiar wysłanego (przyjętego) datagramu. Ustalić z dokładnością do jednego bajta jak duży datagram jest obsługiwany. Wyjaśnić.

# Rozwiązanie

## Schemat Komunikacji

Klient na przemian wysyła pakiet o zadanym rozmiarze po czym czeka na odpowiedź serwera. Powtarza tę pętlę dla każdego rozmiaru jaki otrzymał.

Serwer czeka w pętli na komunikat, sprawdza czy jego rozmiar zgadza się z rozmiarem przekazanym w komunikacie, po czym przesyła odpowiedź - czy otrzymany datagram był prawidłowy oraz numier datagramu jaki wysyła serwer.


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

Porty: 8000 dla serwera Python, 8001 dla serwera C


# Uruchomienie i testowanie

## Instrukcja uruchomienia

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


## Testowanie

Klient: Python, Server: Python

```
tkurzela@bigubu:~/PSI_Z31/zad11$ docker compose up z31_pclient_pserver
(...)
Attaching to z31_pclient_pserver, z31_pserver
z31_pclient_pserver  | Python client for zadanie 1.1
z31_pclient_pserver  | Will send to  z31_pserver : 8000
z31_pclient_pserver  | sending dgram of size=100
z31_pserver          | received good datagram of size=100
z31_pserver          | sending: b'CORRECT datagram'
z31_pclient_pserver  | response=b'CORRECT datagram'
z31_pclient_pserver  | sending dgram of size=200
z31_pserver          | received good datagram of size=200
z31_pserver          | sending: b'CORRECT datagram'
z31_pclient_pserver  | response=b'CORRECT datagram'
z31_pclient_pserver  | sending dgram of size=500
z31_pserver          | received good datagram of size=500
z31_pserver          | sending: b'CORRECT datagram'
z31_pclient_pserver  | response=b'CORRECT datagram'
z31_pclient_pserver  | sending dgram of size=1000
z31_pserver          | received good datagram of size=1000
z31_pserver          | sending: b'CORRECT datagram'
z31_pclient_pserver  | response=b'CORRECT datagram'

```

Klient: C, Server: Python

```
tkurzela@bigubu:~/PSI_Z31/zad11$ docker compose up z31_cclient_pserver
(...)
Attaching to z31_cclient_pserver, z31_pserver
z31_pserver          | received good datagram of size=100
z31_pserver          | sending: b'CORRECT datagram'
z31_pserver          | received good datagram of size=200
z31_pserver          | sending: b'CORRECT datagram'
z31_pserver          | received good datagram of size=500
z31_pserver          | sending: b'CORRECT datagram'
z31_pserver          | received good datagram of size=1000
z31_pserver          | sending: b'CORRECT datagram'
z31_pserver          | received good datagram of size=2000
z31_pserver          | sending: b'CORRECT datagram'
z31_pserver          | received good datagram of size=65507
z31_pserver          | sending: b'CORRECT datagram'
z31_cclient_pserver  | C client for zadanie 1.1
z31_cclient_pserver  | Will send to z31_pserver:8000
z31_cclient_pserver  | Sending datagram #1, size: 100
z31_cclient_pserver  | Server response: CORRECT datagram
z31_cclient_pserver  | Sending datagram #2, size: 200
z31_cclient_pserver  | Server response: CORRECT datagram
z31_cclient_pserver  | Sending datagram #3, size: 500
z31_cclient_pserver  | Server response: CORRECT datagram
z31_cclient_pserver  | Sending datagram #4, size: 1000
z31_cclient_pserver  | Server response: CORRECT datagram
z31_cclient_pserver  | Sending datagram #5, size: 2000
z31_cclient_pserver  | Server response: CORRECT datagram
z31_cclient_pserver  | Sending datagram #6, size: 65507
z31_cclient_pserver  | Server response: CORRECT datagram
z31_cclient_pserver  | Sending datagram #7, size: 65508
z31_cclient_pserver  | sending datagram message: Message too long
```

Klient: C, Server: C

```
tkurzela@bigubu:~/PSI_Z31/zad11$ docker compose up --remove-orphans z31_cclient_cserver
(...)
Attaching to z31_cclient_cserver, z31_cserver
z31_cserver          | C server for zadanie 1.1
z31_cserver          | Will listen on 0.0.0.0:8001
z31_cserver          | Datagram size: (100) Client address: 172.21.31.4:52138
z31_cserver          | Datagram size: (200) Client address: 172.21.31.4:52138
z31_cserver          | Datagram size: (500) Client address: 172.21.31.4:52138
z31_cserver          | Datagram size: (1000) Client address: 172.21.31.4:52138
z31_cserver          | Datagram size: (2000) Client address: 172.21.31.4:52138
z31_cserver          | Datagram size: (65507) Client address: 172.21.31.4:52138
z31_cclient_cserver  | sending datagram message: Message too long
z31_cclient_cserver  | C client for zadanie 1.1
z31_cclient_cserver  | Will send to z31_cserver:8001
z31_cclient_cserver  | Sending datagram #1, size: 100
z31_cclient_cserver  | Server response: CORRECT datagram.
z31_cclient_cserver  | Sending datagram #2, size: 200
z31_cclient_cserver  | Server response: CORRECT datagram.
z31_cclient_cserver  | Sending datagram #3, size: 500
z31_cclient_cserver  | Server response: CORRECT datagram.
z31_cclient_cserver  | Sending datagram #4, size: 1000
z31_cclient_cserver  | Server response: CORRECT datagram.
z31_cclient_cserver  | Sending datagram #5, size: 2000
z31_cclient_cserver  | Server response: CORRECT datagram.
z31_cclient_cserver  | Sending datagram #6, size: 65507
z31_cclient_cserver  | Server response: CORRECT datagram.
z31_cclient_cserver  | Sending datagram #7, size: 65508
```

Klient: Python, Server: C

```
tkurzela@bigubu:~/PSI_Z31/zad11$ docker compose up --remove-orphans z31_pclient_cserver
(...)
Attaching to z31_cserver, z31_pclient_cserver
z31_pclient_cserver  | Python client for zadanie 1.1
z31_pclient_cserver  | Will send to  z31_cserver : 8001
z31_pclient_cserver  | sending dgram of size=100
z31_pclient_cserver  | response=b'CORRECT datagram\n'
z31_pclient_cserver  | sending dgram of size=200
z31_cserver          | Datagram size: (100) Client address: 172.21.31.4:51151
z31_pclient_cserver  | response=b'CORRECT datagram\n'
z31_cserver          | Datagram size: (200) Client address: 172.21.31.4:51151
z31_pclient_cserver  | sending dgram of size=500
z31_cserver          | Datagram size: (500) Client address: 172.21.31.4:51151
z31_pclient_cserver  | response=b'CORRECT datagram\n'
z31_pclient_cserver  | sending dgram of size=1000
z31_cserver          | Datagram size: (1000) Client address: 172.21.31.4:51151
z31_pclient_cserver  | response=b'CORRECT datagram\n'
```

### Sprawdzenie maksymalnego rozmiaru datagramu

Datagram UDP musi się zmieścić w jednej ramce IP, której maksymalny rozmiar to 65535 bajtów. Nagłówek IPv4 mieści się na 20 bajtach (standardowo, bez dodatkowych opcji), a nagłówek UDP zajmuje 8 bajtów. Po odliczeniu nagłówków (65535-20-8=65507) na dane zostaje maksymalnie 65507B, co zgadza się z poniższą obserwacją:

```
tkurzela@bigubu:~/PSI_Z31/zad11$ docker compose up z31_test_size
[+] Running 2/0
 ✔ Container z31_pserver               Created                                                                                                                                           0.0s 
 ✔ Container z31_pclient_pserver_test  Created                                                                                                                                           0.0s 
Attaching to z31_pclient_pserver_test, z31_pserver
z31_pserver               | Python server for zadanie 1.1
z31_pserver               | Will listen on  0.0.0.0 : 8000
z31_pclient_pserver_test  | Python client for zadanie 1.1
z31_pclient_pserver_test  | Will send to  z31_pserver : 8000
z31_pclient_pserver_test  | sending dgram of size=65500
z31_pserver               | received good datagram of size=65500
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65501
z31_pserver               | received good datagram of size=65501
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65502
z31_pserver               | received good datagram of size=65502
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65503
z31_pserver               | received good datagram of size=65503
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65504
z31_pserver               | received good datagram of size=65504
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65505
z31_pserver               | received good datagram of size=65505
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65506
z31_pserver               | received good datagram of size=65506
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65507
z31_pserver               | received good datagram of size=65507
z31_pserver               | sending: b'CORRECT datagram'
z31_pclient_pserver_test  | response=b'CORRECT datagram'
z31_pclient_pserver_test  | sending dgram of size=65508
z31_pclient_pserver_test  | [Errno 90] Message too long
z31_pclient_pserver_test  | Could not send dgram of size=65508
z31_pclient_pserver_test  | Max possible size is 65507

```

# Wnioski

UDP to bardzo prosty protokół warstwy transportowej. Łatwo można napisać prosty program który z niego korzysta. Jednak ta prostota wiąże się z brakiem gwarancji poprawnego przesyłu danych - sprawdzanie poprawności trzeba implementować w programie. Dodatkowo jeśli urządzenie docelowe nie jest dostępne w trakcie nadawania, komunikat przepada bez informacji zwrotnej o niepowodzeniu - jeśli potwierdzenie odbioru jest kluczowe, należy je dodać programowo.

W faktycznych aplikacjach UDP powinien być używany tylko kiedy narzut TCP jest problematyczny i nie dbamy o utratę pojedynczych pakietów - np. w przesyle wideo na żywo, rozmowy głosowej czy gry on-line.