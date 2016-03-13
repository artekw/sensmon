# settings.json

## webapp
Główna konfiguracja aplikacji

   - __host__ - adres ip aplikacji
   - __port__ - port dla aplikacji
   - __password__ - hasło do podstron wymagających logowania, username - admin
   - __iface__
   - __verbose__ - dodatkowe komunikaty w konsoli potrzebne w celu debugowania aplikacji

## serial
Ustawienia dla komunikacji poprzez ser2net lub remserial.

  - __port__ - port na jakim uruchomiony jest ser2net lub remerial
  - __host__ - j.w. ale hostname

## redis
Konfiguracja bazy Redis. Baza przechowuje dane tymczasowe z czujek.

  - __host__ - hostname na jakim działa serwer Redis

## leveldb
Konfiguracja bazy LevelDB(by Google). Baza przechowuje dane historyczne.

  - __enable__ - włączenie rejestrowania odczytów do bazy
  - __dbname__ - katalog w którym będzie przechowywana baza
  - __path__ - ścieżka do w/w katalogu; "kropka" oznacza, że w tym samym co uruchamiana aplikacja
  - __forgot__ - lista nazw czujników dla których nie są zbierane dane do bazy tzw. czarna lista

## mqtt
Konfiguracja serwera komunikatów MQTT dla aplikacji

  - __enable__ - włączenie wysyłania komunikatów MQTT dla czujników; domyślny topic to '/sensmon/< nodename >';
  - __broker__ - hostname brokera MQTT
  - __port__ - port brokera; domyślnie 1883

## mail

## weather
Konfiguracja dla portalu http://openweathermap.org/ z prognozą pogody dla wybranego miasta

  - __enable__ - włączenie pobierania prognozy pogody
  - __city__ - miasto dla którego ma zostać pobrana prognoza pogody
  - __appid__ - identyfikator aplikacji; wymagana rejestracja

## aqi
Konfiguracja dla strony http://aqicn.org z danymi o jakości powietrza dla wybranego miasta

  - __station__ - nazwa stacji

### TODO
  - dodać dla MQTT definiowanie topic'a; teraz jest /sesmon/< nodename > 
