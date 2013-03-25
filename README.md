#sensmon#
In Polish, in English soon

sensmon jest aplikacja webową do monitorowania czujników z projektu sensnode. Aplikacja działa w oparciu o [Websocket](http://pl.wikipedia.org/wiki/WebSocket).

##Wymagania##

sensmon działa tylko na systemie Linuks. Do działania potrzebuje Pythona oraz kilka innych zewnętrznych aplikacji, m.in.

- python2
- redis
- remserial
- tornado
- tornado-redis
- python2-simplejson
- screen
- git
- (jak sobie przypomnę dodam kolejne :)


##Instalacja##

Przykład instalacji na [Raspberry Pi](http://raspberrypi.org) z zainstalowanym [ArchlinuxARM](http://archlinuxarm.org)

    $ pacman -Sy python2 redis remserial tornado tornado-redis python2-simplejson git screen
    $ git clone https://github.com/artekw/sensmon.git


##Konfiguracja remserial##

Potrzebujemy remserial do komunikacji modułu sensbase z Raspberry Pi po interfejsie szeregowym (RS232).

Archlinux od pewnego czasu korzysta z systemd, więc trzeba przygotować skrypt do uruchamiania remserial na starcie systemu

    nano /etc/systemd/system/remserial.service


    [Service]
    Type=simple
    ExecStart=/usr/bin/remserial -m 2 -d -p 2000 -s "9600 raw" /dev/ttyAMA0 &

    [Install]
    WantedBy=multi-user.target

Zapisz.

    sudo systemctl enable remserial.service
    sudo systemctl start remserial.service

##Baza redis

Odpal screen
    python2 redisdb.py
(Ctrl-A+D)

## Aplikacja Web

Odpal screen
     python2 webapp.py
(Ctrl-A+D)

Przeglądarka - http://<IP-RPI>:8080

##Screenshot

![sensmon] (https://dl.dropbox.com/u/677573/Photos/sensmon.png)


![Valid XHTML] (http://w3.org/Icons/valid-xhtml10)