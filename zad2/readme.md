# PSI zad2 - TCP

Realizacja komunikacji między kilentem, a serwerem z wykorzystaniem protkołu TCP, przy transmitowanym strumieniu o rozmiarze minimum 100kB. 

# Rozwiązanie
## Klient
Zrealizowany w języku C, generuje dane - odpowiednio przygotowaną strukturę. Następnie je pakuje i przesyła do serwera.

## Serwer
Zrealizowany w języku Python, czeka na dane od klienta. Po odebraniu odpakowuje otrzymane dane, a następnie przetwarza w celu utrzymania odpowiedniej struktury danych. 

## Struktura
Lista jednokierunkowa, gdzie każdy węzeł listy ma następującą budowę:
- liczba całkowita 32 bitowa - id węzła
- liczba całkowita 16 bitowa - długość napisu
- napis ograniczonej (ale zmiennej) długości, max 50

## Uruchomienie

### Jednolinijkowe
`docker compose up --build` buduje, a następnie uruchamia wszystkie kontenery

**Zalecane** jest jednak wcześniejsze zbudowanie wszystkich kontenerów poleceniem `docker compose build`
Następnie można uruchomić w oddzielnych terminalach:
- `docker compose up z31_tcp_server` serwer Python
- `docker compose up z31_zad2_client` klient C