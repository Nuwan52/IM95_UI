from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import socket
from motor import MotorController
import pandas as pd 

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

readingFlag = True





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



@socketio.on('IO_DATA_REQUEST')
def io_data_request():
    sending_Ethernet_command("A")
    print("Requesting io Data")  


@socketio.on('INIT')
def handle_init():
    print("Initiating the system!")
    Motorstatus()
    InitMotors()

    try:
        message = 'hello from  computer'
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as e:
        print(f"[UDP Send Error] {e}")

def Motorstatus():
    for n in range(1,7):
        try:   
            data = mc.read_driver_status(axis=n)
            time.sleep(0.01)
            print("Axis " , n , data.registers)
        except:
            print("Something Wrong with Axis " ,n)
            break

def InitMotors():

    # mc.MotorToqueSetting(axis=1  ,toque=20)
    mc.MinSoftwareLimit(axis=1 , min= -1000000)

    time.sleep(1)

    mc.MaxSoftwareLimit(axis=1 , Max=1000000)

    mc.clear_alarm(axis=1)
    time.sleep(1)
    status =mc.enable_motor(axis=1)
    time.sleep(1)
    mc.homing(axis=1)

    
    
    # for n in range(1 , 7):
    #     status =mc.enable_motor(axis=n)
    #     print("Enabling Axis " , n)
    #     if(status == 0):
    #         print("Something went wrong with Axis " , n)
    #         break
    # if n == 6:
    #     emit('INIT_BACKEND', {"message": "initialized"}, broadcast=True)
    # else:
    #     emit('INIT_BACKEND', {"message": "stopped"}, broadcast=True)

def DesableMotors():
    for n in range(1 , 7):
        status =mc.disable_motor(axis=n)
        print("Desabling Axis  " , n)
        if(status == 0):
            print("Something went wrong with  Axis " , n)
            break


def sending_Ethernet_command(message):
    try:
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as e:
        print(f"[UDP Send Error] {e}")

def ReadMotorAlams():
    for n in range(1,7):
        try:   
            data = mc.read_current_alarm(axis=n)
            time.sleep(0.01)
            print("Axis " , n , data.registers)
        except:
            print("Something Wrong with Axis " ,n)
            break

def ethernet_thread():
    """Example background thread function."""
    while True:
        data, addr = sock.recvfrom(1024)
        Controller_data_loader(data.decode())
        
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
            # ReadMotorPos()
            # ReadMotorVoltage()
            Motorstatus()
            ReadMotorAlams()
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


def Controller_data_loader(data):
    if(data == 'HS00'):
        print("Heart Beat Tiggering")
    if(data[:2] == 'RI'):
        code = data[2:]
        IO_Input_Encorder(code)
        
  


def IO_Input_Encorder(code):
    data_io = bin(int(code))
    socketio.emit('IO_DATA', {"message": data_io})
    print(data_io)
    

if __name__ == "__main__":
    # ✅ Start your background task properly
    mc = MotorController(port="COM1")

    alarms = pd.read_csv('alarms.csv' ,sep=',')
    print(alarms.head())


    socketio.start_background_task(ethernet_thread)
    socketio.start_background_task(ethernet_thread_AI)
    socketio.start_background_task(ReadMotors)

   

    


    # ✅ Run the SocketIO server (supports WebSockets + threads)
    socketio.run(app, debug=True, use_reloader=False)
    DesableMotors()
    mc.close()

   
