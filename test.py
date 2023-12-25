from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from time import sleep
from gpiozero import LED
from gpiozero import Button
from signal import pause

hostName = "0.0.0.0"
serverPort = 80
taso_lock = threading.Lock()
taso1, taso2, taso3, taso4 = 0, 0, 0, 0

def setLed(r, g, b, duration):
    red_led = LED(2, active_high=False)
    green_led = LED(3, active_high=False)
    blue_led = LED(4, active_high=False)
    try:
        red_led.value = r
        green_led.value = g
        blue_led.value = b
        sleep(duration)
    finally:
        red_led.close()
        green_led.close()
        blue_led.close()

def changeLed(path: str):
    c = path[path.__len__() - 1]
    print("led is now " + str(c))
    if c == 'R':
        setLed(1, 0, 0, 2)
    elif c == 'G':
        setLed(0, 1, 0, 2)
    elif c == 'C':
        setLed(0, 0, 1, 2)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global taso1, taso2, taso3, taso4

        if self.path.startswith("/led"):
            changeLed(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Ruokalistaäänestys</title><meta charset=\"utf-8\"></head>", "utf-8"))
        
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(f""" 
        <h2>
        Punainen (taso1) = {taso1}
        </h2>
         <h2>
        vaalean punainen (taso2) = {taso2}
        </h2>
         <h2>
        vaalean vihreä (taso3) = {taso3}
        </h2>
         <h2>
        vihreä (taso4) = {taso4}
        </h2>
        <br>
        <button onclick="location.href = '/led?c=R';" id="myButton1" class="float-left submit-button" >LED RED</button>
        <button onclick="location.href = '/led?c=G';" id="myButton1" class="float-left submit-button" >LED GREEN</button>
        <button onclick="location.href = '/led?c=B';" id="myButton1" class="float-left submit-button" >LED BLUE</button>


        """, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

def main(url, token):
     #pinnit numeroitu Broadcom järjestelmällä, lisää https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
    
    red_button = Button(6, hold_time=0.05)
    red_button.when_held = lambda: aanesta(url, token, 1)

    light_red_button = Button(13, hold_time=0.05)
    light_red_button.when_held = lambda: aanesta(url, token, 2)

    light_green_button = Button(19, hold_time=0.05)
    light_green_button.when_held = lambda: aanesta(url, token, 3)

    green_button = Button(26, hold_time=0.05)
    green_button.when_held = lambda: aanesta(url, token, 4)

    pause()

def aanesta(url, token, taso):
    global taso1, taso2, taso3, taso4
    with taso_lock:
        print(f"testi äänestetty, TASO:{taso} ")
        if taso == 1:
            taso1 += 1
        elif taso == 2:
            taso2 += 1
        elif taso == 3:
            taso3 += 1
        elif taso == 4:
            taso4 += 1
        sleep(0.8)

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    # Create a new thread for the webserver function
    webserver_thread = threading.Thread(target=webServer.serve_forever)

    # Start the webserver thread
    webserver_thread.start()

    # Call the main function in the main thread
    main("url", "token")

    # Wait for the webserver thread to finish
    webserver_thread.join()

    # Close the webserver
    webServer.server_close()
    print("Server stopped.")
