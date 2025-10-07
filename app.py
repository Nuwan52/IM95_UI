from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

UDP_IP = "192.168.1.177"      
UDP_PORT = 5001        


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0)  



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analytics')
def analytics():
    return render_template("analytics.html")

@app.route('/item-settings')
def item_settings():
    return render_template("item-settings.html")

@app.route('/settings')
def settings():
    print("page requested")
    return render_template("settings.html")


@socketio.on('SOLONOID_ONOFF')
def handle_button_click(button):
    print(button)  # Do your Python function here


@socketio.on('INIT')
def handle_init():
    print("Initiating the system!")  # Do your Python function here
    time.sleep(2)
    emit('INIT_BACKEND', {"message": "Button was clicked!"}, broadcast=True)

    try:
        message = 'hello from  computer'
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as e:
        print(f"[UDP Send Error] {e}")



def ethernet_thread():
    """Example background thread function."""
    while True:
        print('Ethernet thread running...')
        time.sleep(0.1)


if __name__ == "__main__":
    # ✅ Start your background task properly
    # socketio.start_background_task(ethernet_thread)

    # ✅ Run the SocketIO server (supports WebSockets + threads)
    socketio.run(app, debug=True)
