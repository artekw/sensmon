# sensmon - home automation

sensmon jest aplikacją monitorowania czujników z projektu sensnode oraz sterowania przekaźnikami. Aplikacja działa w oparciu o techologię [Websocket](http://pl.wikipedia.org/wiki/WebSocket). Została napisana w frameworku [Tornado](http://www.tornadoweb.org/en/stable/) oraz [AngularJS](https://angularjs.org/). Do przechowywania danych wykorzystano bazę [LMDB](https://lmdb.readthedocs.io/en/release/) oraz [Redis](https://redis.io/).

## Wymagania

sensmon działa tylko na systemie Linuks. Do uruchomienia potrzebny jest Python 2.6.x/2.7.x oraz kilka innych zewnętrznych aplikacji/modułów m.in.

- python
- python-pip
- redis-server
- ser2net
- screen
- git

Debian potrzebuje jeszcze:

- python-dev
- build-essential

Instalacja dla Debiana/Ubuntu:

    $ sudo apt-get install python redis-server screen git ser2net python-pip python-dev build-essential lmdb
    $ git clone https://github.com/artekw/sensmon
    $ cd sensmon
    $ sudo pip install -r requirements.txt

### Ustawienie komunikacji między sensbase a aplikacją

Łącznikiem pomiędzy stroną WWW, a sensbase jest ser2net. Aplikacja ta przekierowuje dane z sensbase do przeglądarki.

Zalecane ustawienie w pliku /etc/ser2net.conf:

    2000:raw:0:/dev/ttyAMA0:9600

Należy pamiętać, aby ustawić ten sam port w pliku settings.conf aplikacji sensmon (patrz niżej)

## Aplikacja Web

Do używania aplikacji zaleca się Chrome/Chromium lub Firefox. Dostosowana jest do pracy na urządzeniach mobilnych.

### Konfiguracja

Pliki konfiguracyjne aplikacji znajdują się w *static/conf*.

- settings.json - ustawienia aplikacji - [dokumentacja](https://github.com/artekw/sensmon/tree/master/static/conf)
- nodemap.json - mapa nodów oraz powiązanych z nim czujników oraz przekaźników

### Uruchomienie

     $ screen -d -m python2 sensmon.py

Wejdz przez przeglądarkę na adres http://adres-ip-hosta:8081

### Co działa?

- dashboard
- wykresy (tylko dzienne)
- prognoza pogody wg [OpenWatherMap](http://openweathermap.org/city/7530941)
- sterowanie przekaźnikami

### Plany

- wykresy
    - tygodniowe
    - miesięczne
    - roczne
- kalendarz Google
- [PushBulllet](https://www.pushbullet.com/)
- panel administatora
- usunięcie pośrednika tj ser2net
- zastosowanie jsonschema do walidacji JSON

### Znane problemy
   - "ConnectionError: Tried to read from non-existent connection" przy generowaniu wykresów

## Zrzuty ekranu

![sensmon info](https://dl.dropboxusercontent.com/u/677573/Photos/sensmon/intro.png)
![sensmon dashboard](https://dl.dropboxusercontent.com/u/677573/Photos/sensmon/dashboard.png)
![sensmon wykresy](https://dl.dropboxusercontent.com/u/677573/Photos/sensmon/graphs.png)
![sensmon switchs](https://dl.dropboxusercontent.com/u/677573/Photos/sensmon/switches.png)

# Uwaga
Aplikacja jest we wstępnym stanie rozwoju autor nie ponosi odpowiedzialności za niewłaściwe działanie programu i ewentualne uszkodzenia powstałe na skutek jego działania.

## Licencja

The MIT License (MIT)

Copyright (c) 2015-2017 Artur Wronowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


![Valid XHTML](http://w3.org/Icons/valid-xhtml10)
