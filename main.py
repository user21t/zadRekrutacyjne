from picamera2 import Picamera2
from os import makedirs
import sys
from flask import Flask, session

picam2 = Picamera2()
# Tworzony jest obiekt klasy kamery Raspberry Pi

cam_cfg = picam2.create_still_configuration()
picam2.configure(cam_cfg)
# Kamera jest konfigurowana tak, aby robiła pojedyncze zdjęcia o wysokiej rozdzielczości

picam2.start()
# Kamera zostaje włączona

img_dir = "static/img/"
# Lokalizacja katalogu, gdzie są umieszczane zdjęcia z kamery

try:
  makedirs(img_dir)
  print(f"Katalog {img_dir} pomyślnie utworzony.")
except FileExistsError:
  print(f"Katalog {img_dir} już istnieje.")
except Exception as e:
  print(f"Błąd: {e}")
  sys.exit(1)
# Utwórz katalog ze ścieżką względną "static/img/"

app = Flask(__name__, static_url_path='/static')
# Obiekt klasy Flask - prostego serwera WWW - został zainicjowany
# wraz z nazwą aplikacji oraz odnośnikiem do plików statycznych (static_url_path)

app.i=0

@app.route("/")
def rpi_drone_cam():
  """Funkcja widoku, która wyświetla zawartość strony
  głównej po połączeniu się klienta z serwerem.

  Za każdym odświeżeniem strony kamera robi zdjęcie
  i zapisuje je w katalogu 'static/img/'.
  Następnie wyświetlane jest ono w przeglądarce
  internetowej wraz z podpisem. Po odświeżeniu zostaje
  podmienione na nowsze, zaś folder powiększa się o kolejny obraz.
  """

  app.i+=1
  pic_src=f"{img_dir}zdj_{app.i}.jpg"
  picam2.capture_file(pic_src)
  pic_desc="Oto zdjęcie zrobione przez kamerkę Raspberry Pi"
  
  return f"""
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="Refresh" content="10">
    </head>
    <body>
      <img src="{pic_src}">
      <h2>{pic_desc}</h2>
    </body>
  </html>
  """

if __name__ == '__main__':
  # Uruchamiany jest serwer Flask z adresem IP 10.10.10.1 oraz portem 5000
  app.run(host="10.10.10.1")
