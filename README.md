# sensmon

sensmon jest aplikacja webową do monitorowania czujników z projektu sensnode. Aplikacja działa w oparciu o [Websocket](http://pl.wikipedia.org/wiki/WebSocket).

## Wymagania

sensmon działa tylko na systemie Linuks. Do działania potrzebuje Pythona 2.x oraz kilka innych zewnętrznych aplikacji, m.in.

- python
- python-simplejson
- python-pip
- redis
- ser2net
- tornado (3.0)
- tornado-redis
- screen
- git
- pil
- plyvel

Debian wymaga jeszcze:

- python-dev
- build-essential
- libleveldb-dev


Debian:

  $ sudo apt-get install python redis-server screen git ser2net python-pip python-dev build-essential libleveldb-dev
  $ sudo pip-2.7 install simplejson tornado tornado-redis plyvel


### Transmisja szeregowa (UART)

Łącznikiem pomiędzy stroną WWW, a modułem jest ser2net. Aplikacja ta przekierowuje dane z UART na TCP. 

Zalecane ustawienie w pliku /etc/ser2net.conf:

    2000:raw:0:/dev/ttyAMA0:9600
    
Należy pamiętać, aby ustawić ten sam port w pliku settings.conf aplikacji sensmon (patrz niżej)

## Aplikacja Web
### Konfiguracja

Pliki konfiguracyjne aplikacji znajduja sie w *static/conf*.

- settings.json - ustawienia aplikacji
- nodemap.json - mapowanie nazwy z id punktu
- control.json - konfiguracja przekaźników

### Uruchomienie

     $ cd sensmon
     $ screen -d -m python2 sensmon.py

Przeglądarka - http://IP-RPI:8081

### Co działa?

- dashboard
- logi z czujników
- sterowanie przekaźnikami

### Plany

- wykresy
- panel administatora

## Zrzuty ekranu

![sensmon dash](https://dl.dropbox.com/u/677573/Photos/sensmon.png)
![sensmon logs](https://dl.dropbox.com/u/677573/Photos/sensmon_i.png)

# Uwaga
Aplikacja jest we wstępnym stanie rozwoju autor nie ponosi odpowiedzialności na niewłaściwe działanie programu.

## Licencja

The MIT License (MIT)

Copyright (c) 2015 Artur Wronowski

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

