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


###Konsola szeregowa###

Do poprawnej działania konsoli szeregowej w Raspberry Pi z remserial należy wykonać kilka czynności [opisanych] (https://github.com/artekw/sensmon/wiki/Konsola-szeregowa) na stronie wiki. Jest to proces wymagany, gdyż Raspberry Pi komunikuje się z modułem po tym protokole.

Archlinux od pewnego czasu korzysta z systemd, więc trzeba przygotować skrypt do uruchamiania remserial.

    cp sensmon
    sudo cp other/remserial.service /etc/systemd/system/remserial

Pozostaje uruchomić usługę:

    sudo systemctl enable remserial
    sudo systemctl start remserial

## Aplikacja Web

Odpal screen

     ./webapp.py

(Ctrl-A+D)

Przeglądarka - http://IP-RPI:8080

##Screenshot

![sensmon] (https://dl.dropbox.com/u/677573/Photos/sensmon.png)


![Valid XHTML] (http://w3.org/Icons/valid-xhtml10)