#sensmon#
In Polish, in English soon

sensmon jest aplikacj¹ webow¹ do monitorowania czujników z projektu sensnode

##Wymagania##


sensmon dzia³a tylko na systemie Linuks. Do dzia³ania potrzebuje Pythona oraz kilka innych zewnêtrznych aplikacji, m.in.

- python2
- redis
- remserial
- tornado
- tornado-redis
- python2-simplejson
- (jak sobie przypomnê dodam kolejne :)


##Instalacja##

Przyk³ad instalacji na [Raspberry Pi](http://raspberrypi.org) z zainstalowanym [ArchlinuxARM](http://archlinuxarm.org)

    $ pacman -Suy
    $ pacman -S python2 redis remserial tornado tornado-redis python2-simplejson


##Konfiguracja remserial##

Potrzebujemy remserial do pobierania danych z uk³adu sensbase, który komunikuje siê z Raspberry Pi po interfejsie szeregowym (RS232).

Archlinux od pewnego czasy korzysta z systemd, wiêc trzeba przygotowaæ skrytp do startowania remserial na starcie systemu

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

## Aplikacja Web


##Screenshot

![sensmon] (https://dl.dropbox.com/u/677573/Photos/sensmon.png)


![Valid XHTML] (http://w3.org/Icons/valid-xhtml10)