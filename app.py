from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import socket
from motor import MotorController

app = Flask(__name__)
socketio = SocketIO(app)

UDP_IP = "169.254.5.191"      
UDP_PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 5001))


sock_02 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_02.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_02.bind(("0.0.0.0", 7920))

readingFlag = False



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
    print("Initiating the system!")
    InitMotors()

    try:
        message = 'hello from  computer'
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as e:
        print(f"[UDP Send Error] {e}")


def InitMotors():
    for n in range(1 , 7):
        status =mc.enable_motor(axis=n)
        print("Enabling Axis " , n)
        if(status == 0):
            print("Something went wrong with Axis " , n)
            break
    if n == 6:
        emit('INIT_BACKEND', {"message": "initialized"}, broadcast=True)
    else:
        emit('INIT_BACKEND', {"message": "stopped"}, broadcast=True)

def DesableMotors():
    for n in range(1 , 7):
        status =mc.disable_motor(axis=n)
        print("Desabling Axis  " , n)
        if(status == 0):
            print("Something went wrong with  Axis " , n)
            break


def ethernet_thread():
    """Example background thread function."""
    while True:
        data, addr = sock.recvfrom(1024)
        print("[Arduino] Received:", data.decode())
        
        time.sleep(0.1)


def ethernet_thread_AI():
    """Example background thread function."""
    while True:
        data, addr = sock_02.recvfrom(1024)
        print("AI Received:", data.decode())
        
        time.sleep(0.1)


def ReadMotors():
    while True:
        if readingFlag:
            ReadMotorPos()
            ReadMotorVoltage()
        time.sleep(2)

def ReadMotorPos():
    for n in range(1,7):
        try:   
            data = mc.read_motor_pos(axis=n)
            time.sleep(0.01)
            print("Axis " , n , data.registers)
        except:
            print("Something Wrong with Axis " ,n)
            break


def ReadMotorVoltage():
    pass

    

if __name__ == "__main__":
    # ✅ Start your background task properly
    mc = MotorController(port="COM1")
    socketio.start_background_task(ethernet_thread)
    socketio.start_background_task(ethernet_thread_AI)
    socketio.start_background_task(ReadMotors)
    


    # ✅ Run the SocketIO server (supports WebSockets + threads)
    socketio.run(app, debug=True, use_reloader=False)
    DesableMotors()
    mc.close()

   


# This is github test