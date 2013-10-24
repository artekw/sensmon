# sensmon

sensmon jest aplikacja webową do monitorowania czujników z projektu sensnode. Aplikacja działa w oparciu o [Websocket](http://pl.wikipedia.org/wiki/WebSocket).

## Wymagania

sensmon działa tylko na systemie Linuks. Do działania potrzebuje Pythona 2.7 oraz kilka innych zewnętrznych aplikacji, m.in.

- python2
- python2-simplejson
- redis
- remserial
- tornado (3.0)
- tornado-redis
- screen
- git
- pil
- qrcode
- leveldb

## Instalacja

Przykład instalacji na [Raspberry Pi](http://raspberrypi.org) z zainstalowanym [ArchlinuxARM](http://archlinuxarm.org)

    $ pacman -Sy python2 redis tornado tornado-redis python2-simplejson git screen remserial python2-pip
    $ sudo pip-2.7 install pil qrcode
    $ git clone https://github.com/artekw/sensmon.git


### Transmisja szeregowa (UART)

Do poprawnej współpracy transmisji szeregowej(UART) w Raspberry Pi z remserial należy wykonać kilka czynności [opisanych](https://github.com/artekw/sensmon/wiki/Konsola-szeregowa) na stronie wiki. Jest to proces wymagany, gdyż Raspberry Pi komunikuje się z modułem po tym protokole.

Archlinux od pewnego czasu korzysta z systemd, więc trzeba przygotować skrypt do uruchamiania remserial.

    $ cp sensmon
    $ sudo cp other/remserial.service /etc/systemd/system/remserial

Pozostaje uruchomić usługę:

    $ sudo systemctl enable remserial
    $ sudo systemctl start remserial

## Aplikacja Web
### Konfiguracja

Pliki konfiguracyjne aplikacji znajduja sie w *static/conf*.

- settings.json - ustawienia aplikacji
- nodes.json - konfiguracja punktów
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
- autoryzacja

### Plany

- wykresy
- panel administatora

## Zrzuty ekranu

![sensmon dash](https://dl.dropbox.com/u/677573/Photos/sensmon.png)
![sensmon control](https://dl.dropbox.com/u/677573/Photos/sensmon_c.png)
![sensmon logs](https://dl.dropbox.com/u/677573/Photos/sensmon_i.png)


![Valid XHTML](http://w3.org/Icons/valid-xhtml10)
