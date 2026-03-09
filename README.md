# Zadanie rekrutacyjne do koła AGH Solar Plane
Skrypt w języku Python, który przywraca przesyłanie obrazu z Raspberry Pi w dronie do stacji naziemnej

## Zależności systemowe
* [Alpine Linux](https://alpinelinux.org/) lub [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)
* Python 3.12+
* nasm 2.16+
* libcap-dev 2.75+
* libjpeg-turbo-dev 2.1+
* hostapd 2.1+

## Instalacja pakietów Python
`pip install -r requirements.txt`

## Rozwiązanie problemu
Aby zamontowany w UAV mikrokomputer Raspberry Pi Zero W mógł przesyłać zdjęcia z podłączonej kamery,
niezbędna do jej obsługi jest pakiet [Picamera2](https://github.com/raspberrypi/picamera2).
Jako iż jednym z założeń projektu jest odbieranie obrazu przez przeglądarkę internetową, postanowiłem
zastosować mikroframework do serwerów WWW - [Flask](https://github.com/pallets/flask). Przekształciłem
Raspberry Pi w taki serwer, aby móc łatwo wysyłać zrobione zdjęcie do klienta przez przeglądarkę.
Polega to na tym, że kamera robi zdjęcie co 10 sekund wraz z wysłaniem przez klienta ponownego żądania
udostępnienia zawartości strony głównej do serwera. Obrazy są zapisane w pamięci trwałej mikrokomputera.

Modem Wi-Fi jest podłączony do laptopa w stacji naziemnej jako punkt dostępowy (AP). Umożliwia to demon `hostapd`.
Poniżej jest plik konfiguracyjny, który zapewnia najlepszą obsługę obecnych kart sieciowych przez AP w zabezpieczonym połączeniu:
```
# Interfejs używany przez modem
interface=wlan0
# Punkt dostępowy nadaje na częstotliwości 2.4GHz
hw_mode=g
# Kanał do wykorzystania
channel=6
# Używane są tylko polskie częstotliwości
ieee80211d=1
country_code=PL
# Wsparcie standardu 802.11n
ieee80211n=1
# Wsparcie QoS (Quality of Service) - ustawianie priorytetów aplikacji oraz usług w sieci
wmm_enabled=1

# Nazwa punktu dostępowego
ssid=nazwa_ap
# Jest możliwa zarówno otwarte uwierzytelnianie (OSA), jak i przez współdzielony klucz (SKA)
auth_algs=3
# Ustawienia uwierzytelniania WPA2
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=haslo_do_zmiany
```
