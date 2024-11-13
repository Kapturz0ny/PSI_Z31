Struktura datagramu klienta:
- 2 bajty - rozmiar całego datagramu
- n-2 bajty - kolejne litery A-Z, powtarzające się

Struktura datagramu serwera:

SSS_dgram_#\<i\>
- SSS - kod weryfikacji otrzymanego datagramu
    - COR dla poprawnego
    - ERR dla błędnego
- i - numer wysłanego datagramu przez serwer


Przykładowa komunikacja z perspektywy serwera:
1. received: 0x0 0x4 A B
2. sent: C O R _ d g r a m _ # _ 0x1
3. received: 0x0 0x8 A B C
4. sent: E R R _ d g r a m _ # _ 0x2
