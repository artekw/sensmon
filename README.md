# sensmon - home automation

sensmon jest aplikacją przeglądarkową do monitorowania czujników z projektu sensnode. Aplikacja działa w oparciu o techologię [Websocket](http://pl.wikipedia.org/wiki/WebSocket). Została napisana w frameworku [Tornado](http://www.tornadoweb.org/en/stable/) oraz [AngularJS](https://angularjs.org/).

## Wymagania

sensmon działa tylko na systemie Linuks. Do uruchomienia potrzebny jest Python 2.x oraz kilka innych zewnętrznych aplikacji/modułów m.in.

- python
- python-simplejson
- python-pip
- redis
- ser2net
- tornado
- tornado-redis
- screen
- git
- plyvel
- jsontree
- pacho-mqtt
- bokeh

Debian potrzebuje jeszcze:

- python-dev
- build-essential
- libleveldb-dev

Instalacja w dystrybucji Debiana/Ubuntu:

    $ sudo apt-get install python redis-server screen git ser2net python-pip python-dev build-essential libleveldb-dev
    $ git clone https://github.com/artekw/sensmon
    $ cd sensmon
    $ sudo pip-2.7 install -r requirements.txt

### Ustawienie komunikacji między sensbase a aplikacją

Łącznikiem pomiędzy stroną WWW, a sensbase jest ser2net. Aplikacja ta przekierowuje dane z sensbase do przeglądarki.

Zalecane ustawienie w pliku /etc/ser2net.conf:

    2000:raw:0:/dev/ttyAMA0:9600

Należy pamiętać, aby ustawić ten sam port w pliku settings.conf aplikacji sensmon (patrz niżej)

## Aplikacja Web
### Konfiguracja

Pliki konfiguracyjne aplikacji znajdują się w *static/conf*.

- settings.json - ustawienia aplikacji (tu ustaw poprawny port dla ser2net)
- nodemap.json - mapa nodów oraz powiązanych z nim czujników
- control.json - konfiguracja przekaźników

### Uruchomienie

     $ screen -d -m python2 sensmon.py

Wejdz przez przeglądarkę na adres http://adres-ip-hosta:8081

### Co działa?

- dashboard
- wykresy (tylko dzienne)

### Plany

- wykresy
    - tygodniowe
    - miesięczne
    - roczne
- panel administatora
- sterowanie przekaźnikami

## Zrzuty ekranu

![sensmon dashboard](https://dl.dropboxusercontent.com/u/677573/Photos/sensmon/dashboard.png)
![sensmon wykresy](https://dl.dropboxusercontent.com/u/677573/Photos/sensmon/graphs.png)

# Uwaga
Aplikacja jest we wstępnym stanie rozwoju autor nie ponosi odpowiedzialności na niewłaściwe działanie programu i ewentualne uszkodzenia powstałe na skutek jego działania.

## Licencja

The MIT License (MIT)

Copyright (c) 2015-2016 Artur Wronowski

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
