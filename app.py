from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import socket
from motor import MotorController
import pandas as pd 
import threading
modbus_lock = threading.Lock()



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
alarmErrors = False
machineRuning = False
motorVelocity_z = 500
motorVelocity_x = 6000
# Debug Variables 
machine_setting_mode = 0
home_done = False

sendtime = 0
retry_count =0
SRRVD = False
SRRVU = False


SRRHL = False
SRRHR = False

CUP_MODE = 1


SRRHR_event = threading.Event()
SRRHL_event = threading.Event()
SRRVU_event = threading.Event()
SRRVD_event = threading.Event()

SR0CO_event = threading.Event()
SR0EX_event = threading.Event()

IMSENSOR_event = threading.Event()

CUP_STACK_COMPLETE_event  = threading.Event()




ROBOT_ARM_COMPLETE_event = threading.Event()
ROBOT_ARM_PICKING_COMPLETED_event = threading.Event()



# packing axis io pin verify 

packing_suction_01_event = threading.Event()
packing_suction_02_event = threading.Event()
packing_expander_event = threading.Event()


PSR01OK  = False
PSG01OK  = False
PSR02OK  = False
PSG02OK  = False
PSR03OK  = False
PSG03OK  = False

PSR04OK  = False
PSG04OK  = False




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


def IO_control(io_pin , state):
    pass

@socketio.on('START_STOP')
def startingReques(data):
    global machineRuning
    machineRuning = data
    global home_done

    if home_done ==False:
        Homing_loop()
        home_done = True
    
    
    print("START THE MACHINE  " , data)  



@socketio.on('SOLONOID_ONOFF')
def handle_button_click(button):
    data = button.strip()

    if 'toggle-btn 03 on' in data:
        sending_Ethernet_command('CIF0030')

    if 'toggle-btn 03 off' in data:
        sending_Ethernet_command('CIF0031')

    if 'toggle-btn 01 on' in data:
        sending_Ethernet_command('CIF0010')

    if 'toggle-btn 01 off' in data:
        sending_Ethernet_command('CIF0011')

    if 'toggle-btn 02 on' in data:
        sending_Ethernet_command('CIF0020')

    if 'toggle-btn 02 off' in data:
        sending_Ethernet_command('CIF0021')
        
    if 'toggle-btn 04 on' in data:
        sending_Ethernet_command('CIF0040')

    if 'toggle-btn 04 off' in data:
        sending_Ethernet_command('CIF0041')

    if 'toggle-btn 05 on' in data:
        sending_Ethernet_command('CIF0050')

    if 'toggle-btn 05 off' in data:
        sending_Ethernet_command('CIF0051')

    if 'toggle-btn 06 on' in data:
        sending_Ethernet_command('CIF0060')

    if 'toggle-btn 06 off' in data:
        sending_Ethernet_command('CIF0061')

    if 'toggle-btn 07 on' in data:
        sending_Ethernet_command('CIF0070')

    if 'toggle-btn 07 off' in data:
        sending_Ethernet_command('CIF0071')
        
    if 'toggle-btn 08 on' in data:
        sending_Ethernet_command('CIF0080')

    if 'toggle-btn 08 off' in data:
        sending_Ethernet_command('CIF0081')

    if 'toggle-btn 09 on' in data:
        sending_Ethernet_command('CIE0010')

    if 'toggle-btn 09 off' in data:
        sending_Ethernet_command('CIE0011')

    if 'toggle-btn 10 on' in data:
        sending_Ethernet_command('CIE0020')

    if 'toggle-btn 10 off' in data:
        sending_Ethernet_command('CIE0021')

    if 'toggle-btn 11 on' in data:
        sending_Ethernet_command('CIE0030')

    if 'toggle-btn 11 off' in data:
        sending_Ethernet_command('CIE0031')


    if 'toggle-btn 12 on' in data:
        sending_Ethernet_command('CIE0040')

    if 'toggle-btn 12 off' in data:
        sending_Ethernet_command('CIE0041')


    if 'toggle-btn 13 on' in data:
        sending_Ethernet_command('CIA0070')

    if 'toggle-btn 13 off' in data:
        sending_Ethernet_command('CIA0071')

    if 'toggle-btn 14 on' in data:
        sending_Ethernet_command('CIA0040')

    if 'toggle-btn 14 off' in data:
        sending_Ethernet_command('CIA0041')

    if 'toggle-btn 15 on' in data:
        sending_Ethernet_command('CIA0050')

    if 'toggle-btn 15 off' in data:
        sending_Ethernet_command('CIA0051')

    if 'toggle-btn 16 on' in data:
        sending_Ethernet_command('CIA0070')

    if 'toggle-btn 16 off' in data:
        sending_Ethernet_command('CIA0071')

    # if 'toggle-btn 04 on' in data:
    #     sending_Ethernet_command('CIB0011')
    #     print(mc.JogVelocity(6 , 10)) 
    #     print(mc.JogVelocity(2 , 0)) 
    #     print(mc.JogVelocity(7 , 0)) 
    #     print(mc.JogVelocity(1 , 0)) 
    #     print(mc.JogVelocity(3 , 0)) 

    #     # mc.send_immediate_trigger_relative(pos=1000000 , slave_id=6 , velocity=100)
    #     # corrent homing
    #     # mc.homing(axis=7 , direction=0) #high speed arm x
    #     # mc.homing(axis=2 , direction=1) # cup sucking arm aixs 
    #     # mc.homing(axis=1 ,direction=1) #stacking robot z axis 
    #     # mc.homing(axis=6 ,direction=1) #high speed arm Z 
    #     # mc.homing(axis=3 , direction=1) # stacking robot x axis 



    #     print('io 4 off ')
    # if 'toggle-btn 04 off' in data:
    #     sending_Ethernet_command('CIB0010')
    #     # mc.send_immediate_trigger(pos=0 , slave_id=1 , velocity=100)
        
    #     print('io 4  on')
    


@socketio.on('IO_DATA_REQUEST')
def io_data_request():
    sending_Ethernet_command("A")
    global machine_setting_mode
    machine_setting_mode = 1
    print("Requesting io Data")  

@socketio.on('ESTOP')
def estop_data_request():
    DesableMotors()
    print("estop has actuated")  


@socketio.on('HOME_BUTTON')
def home_button_trigger(data):
    global machine_setting_mode
    machine_setting_mode = 0
    print("home button has been pressed")  


@socketio.on('SERVO_CONTROL_MANUAL')
def servo_data_request(motor , data):
    # sending_Ethernet_command("A")
    # readingFlag = False
    # time.sleep(0.5)
    print("-------------------SETTING SERVO DATA---------------------" , motor, data)  
    mc.send_immediate_trigger(pos=data , slave_id=motor)
    # time.sleep(0.5)
    # readingFlag = True
  

def Homing_loop():
    mc.homing(axis=2 , direction=1)
    time.sleep(0.1)
    while movement_complete(axis=2) == 0:
        print("Waiting for Complete Home .. Axis 2")
        time.sleep(0.1)
    print("Home Done :  Axis 2")

    mc.homing(axis=1 ,direction=1) 
    time.sleep(0.1)
    while movement_complete(axis=1) == 0:
        print("Waiting for Complete Home .. Axis 1")
        time.sleep(0.1)
    print("Home Done :  Axis 1")
    

    mc.homing(axis=3 , direction=1)
    time.sleep(0.1)
    while movement_complete(axis=3) == 0:
        print("Waiting for Complete Home .. Aixs 3")
        time.sleep(0.1)
    print("Home Done :  Axis 3")

    mc.homing(axis=6 ,direction=1)
    time.sleep(0.1)
    while movement_complete(axis=6) == 0:
        print("Waiting for Complete Home .. Aixs 6")
        time.sleep(0.1)
    print("Home Done :  Axis 6")

    mc.homing(axis=7 , direction=0)
    time.sleep(0.1)
    while movement_complete(axis=7) == 0:
        print("Waiting for Complete Home .. Aixs 7")
        time.sleep(0.1)
    print("Home Done :  Axis 7")


def HomeDirectionSet():
    sending_Ethernet_command("CIF0010")
    time.sleep(0.2)
    sending_Ethernet_command("CIF0030")
    time.sleep(0.2)
    




@socketio.on('INIT')
def handle_init():
    print("Initiating the system!")
    # Motorstatus()
    InitMotors()

    # Ethernet preformnce testing --------------------------
    # global sendtime
    # sendtime = time.time_ns()
    # print("sending time : " , sendtime)
    # -------------------------------------------------------

    try:
        message = 'hello from  computer'
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
     
    except Exception as e:
        print(f"[UDP Send Error] {e}")

def Motorstatus():
    for n in range(1,8):
        try:   
            data = mc.read_driver_status(axis=n)
            time.sleep(0.01)
            print("Axis " , n , data.registers)
        except:
            print("Something Wrong with Axis " ,n)
            break

def verfly_motor_errors(axis ,  data):
    global alarmErrors
    print(axis , "  " , hex(data[0]))
    if data[0] != 0:
        socketio.emit('ALARM', {"Axis" : axis,"Error": hex(data[0])})
        alarmErrors = True           
    else:
        alarmErrors = False
    
    
def Init_Convayer():
    
    pass



def InitMotors():
    global alarmErrors

    # TOQUE LIMIT SETUP ..

    mc.MotorToqueSetting(axis=1  ,toque=400)
    time.sleep(0.5)
    mc.MotorToqueSetting(axis=2  ,toque=400)
    time.sleep(0.5)
    mc.MotorToqueSetting(axis=3  ,toque=400)
    time.sleep(0.5)
    mc.MotorToqueSetting(axis=6  ,toque=200)
    time.sleep(0.5)
    mc.MotorToqueSetting(axis=7  ,toque=400)
    time.sleep(0.5)

    # SOFTWARE LIMIT SETUP 


    mc.MinSoftwareLimit(axis=6 , min= 100)
    time.sleep(0.5)
    mc.MaxSoftwareLimit(axis=6 , Max=32000)
    time.sleep(0.5)
    mc.MinSoftwareLimit(axis=2 , min= 100)
    time.sleep(0.5)
    mc.MaxSoftwareLimit(axis=2 , Max=130000)
    time.sleep(0.5)
    mc.MinSoftwareLimit(axis=7 , min= -210000)
    time.sleep(0.5)
    mc.MaxSoftwareLimit(axis=7 , Max=-100)
    time.sleep(0.5)
    mc.MinSoftwareLimit(axis=3 , min= 100)
    time.sleep(0.5)
    mc.MaxSoftwareLimit(axis=3 , Max=441000)
    time.sleep(0.5)
    mc.MinSoftwareLimit(axis=1 , min= 10)
    time.sleep(0.5)
    mc.MaxSoftwareLimit(axis=1 , Max=87000)
    time.sleep(0.5)
    # mc.clear_alarm(axis=1)
    # time.sleep(1)
    # status =mc.enable_motor(axis=1)
    # time.sleep(1)
    # mc.homing(axis=1)

    for c in range(1 , 8):
        print("Clear Alarms Axis " , c)
        alarmClearState = mc.clear_alarm(axis=c)
        if(alarmClearState == 0):
            print("Something went wrong with Axis " , c)
            alarmErrors = True
            break
    
    time.sleep(1)
    ReadMotorAlams()
    time.sleep(1)
    HomeDirectionSet()
    # time.sleep(1)

    if alarmErrors == False:
        for n in range(1 , 8):
            status =mc.enable_motor(axis=n)
            print("Enabling Axis " , n)
            if(status == 0):
                print("Something went wrong with Axis " , n)
                socketio.emit('INIT_BACKEND', {"message": "stopped"})
                break
            if n == 6:
                socketio.emit('INIT_BACKEND', {"message": "initialized"})
            
                
    else:
        socketio.emit('INIT_BACKEND', {"message": "stopped"})

    

def DesableMotors():
    for n in range(1 , 8):
        status =mc.disable_motor(axis=n)
        print("Desabling Axis  " , n)
        if(status == 0):
            print("Something went wrong with  Axis " , n)
            # break


def sending_Ethernet_command(message):
 
    try:
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as e:
        print(f"[UDP Send Error] {e}")

def ReadMotorAlams():
    for n in range(1,7):
        try:   
            data = mc.read_current_alarm(axis=n)
            verfly_motor_errors(axis=n , data= data.registers)
            time.sleep(0.01)
            
        except:
            print("Something Wrong with Axis " ,n)
            break

def ethernet_thread():
    """Example background thread function."""
    while True:
        data, addr = sock.recvfrom(1024)
        Controller_data_loader(data.decode())


def safe_move(axis, velocity, pos):
    with modbus_lock:
        Movement_exicuter(axis=axis, velocity=velocity, pos=pos)

def safe_move_relative(axis, velocity, pos):
    with modbus_lock:
        Movement_exicuter_relative(axis=axis, velocity=velocity, pos=pos)


def safe_movement_complete(axis):
    with modbus_lock:
        return movement_complete(axis=axis)



def ethernet_thread_AI():
    """Example background thread function."""
    while True:
        data, addr = sock_02.recvfrom(1024)
        print("AI Received:", data.decode())
        sending_Ethernet_command(data.decode())
        
        time.sleep(0.1)

def Movement_exicuter(axis , pos , velocity):
    global machineRuning
    status = mc.send_immediate_trigger(pos=pos , velocity=velocity, slave_id=axis)
    retry_count = 0
    while status == 0:
        print("Modbus Failure") 
        machineRuning = 0
        break
        status = mc.send_immediate_trigger(pos=pos , velocity=velocity, slave_id=axis)
        retry_count = retry_count + 1
        if(retry_count > 100):
            print("Modbus Failure .. Please Check SNR values")
            retry_count = 0
            machineRuning = 0
            break



def Movement_exicuter_relative(axis , pos , velocity):
    global machineRuning
    status = mc.send_immediate_trigger_relative(pos=pos , velocity=velocity, slave_id=axis)
    retry_count = 0
    while status == 0:
        print("Modbus Failure") 
        machineRuning = 0
        break
        status = mc.send_immediate_trigger_relative(pos=pos , velocity=velocity, slave_id=axis)
        retry_count = retry_count + 1
        if(retry_count > 100):
            print("Modbus Failure .. Please Check SNR values")
            retry_count = 0
            machineRuning = 0
            break

def movement_complete(axis):
    movement_complete = False
    while movement_complete == False:
        try:
            data = mc.read_driver_status(axis=axis)
            value = data.registers[0]
            time.sleep(0.01)
            if value == 27:
                movement_complete = True
                print("Movet Completed")
                return 1
            else:
                return 0
        except:
            print("Modbus Reading Error")


def PackingAxis_event_clear():
    SR0EX_event.clear()
    SR0CO_event.clear()
    packing_suction_01_event.clear();
    packing_suction_02_event.clear()
        

def Event_clear():
    SRRHL_event.clear()
    SRRHR_event.clear()
    SRRVD_event.clear()
    SRRVU_event.clear()

def veryfy_pos(target , axis):
    data = mc.read_motor_pos(axis=axis)
    time.sleep(0.01)
    pos = modbus_position_to_decimal(data.registers[0] ,data.registers[1])
    if abs(target - pos) < 20:
        return 1
    else:
        return 0

def ReadMotors():
    while True:
       

        if readingFlag:
            global machineRuning
            global motorVelocity_z
            global motorVelocity_x
            global machine_setting_mode
            global home_done
            global retry_count
            global SRRVU, SRRVD , SRRHL , SRRHR
            global PSR01OK , PSG01OK , PSG02OK , PSR02OK , PSR03OK , PSG03OK

            if machine_setting_mode == 1:
                ReadMotorPos()
                time.sleep(0.5)
            



            if machineRuning == 1 and home_done ==True:
                print("Loop exicuting")
                safe_move(axis=2 , velocity= 3000 , pos=130000)
                sending_Ethernet_command('CIF0031') 
       
                SRRVD = False
                SRRVU = False
                SRRHL = False
                SRRHR = False
                PSG01OK = False
                PSG02OK = False
                Event_clear()
                
                # SENDING SUCKTION ON COMMANDS
                time.sleep(0.01)
                sending_Ethernet_command('CIF0041')
                time.sleep(0.01)
                sending_Ethernet_command('CIF0061')
                 
                
                while safe_movement_complete(axis=2) == 0:
                    time.sleep(0.01)

                while not IMSENSOR_event.is_set():
                    sending_Ethernet_command("IMSENSOR")
                    time.sleep(0.2)
                CUP_STACK_COMPLETE_event.set()

                # checkig for 4 cup mode

                # checking for all cup mode. 

                while not PSG01OK or not PSG02OK:
                    time.sleep(0.01)

                
                

                IMSENSOR_event.clear()
                SRRVD = False
                SRRVU = False
                SRRHL = False
                SRRHR = False


                while not SRRHR_event.is_set():
                    sending_Ethernet_command('CIF0011')
                    time.sleep(0.2)

                while not SRRHL_event.is_set():
                    sending_Ethernet_command('CIF0010')
                    time.sleep(0.2)

                while not SRRVU_event.is_set():
                    sending_Ethernet_command('CIF0030')
                    time.sleep(0.2)
                

                # sending_Ethernet_command('CIF0011')
                # print("waiting for CIF0011")
                # SRRHR_event.wait()


                # sending_Ethernet_command('CIF0010')
                # print("waiting for CIF0010")
                # SRRHL_event.wait() 
               
                # sending_Ethernet_command('CIF0030')  
                # print("waiting for CIF0030")
                # SRRVU_event.wait()

                safe_move(axis=2 , velocity= 4000 , pos=100)
                
                while safe_movement_complete(axis=2) == 0:
                    time.sleep(0.01)

                

                ROBOT_ARM_COMPLETE_event.set()
                time.sleep(0.3)

                sending_Ethernet_command('CIF0040')
                time.sleep(0.01)
                sending_Ethernet_command('CIF0060')
                time.sleep(0.01)

                ROBOT_ARM_PICKING_COMPLETED_event.wait()
                ROBOT_ARM_PICKING_COMPLETED_event.clear()

                
                 
                SRRVD = False
                SRRVU = False
                SRRHL = False
                SRRHR = False
                Event_clear()

               

                print("start loop over.............................")
                    
                    
        time.sleep(0.1)


def PackingAxis():
    while True:
        global machineRuning , home_done
        if machineRuning == 1 and home_done ==True:
            #  clear the packing axis veraibles
             PackingAxis_event_clear()

             safe_move(axis=3 , velocity= 5000 , pos=440827)

            #  send untill the controller respondes 

             while not SR0CO_event.is_set():
                sending_Ethernet_command('CIA0041')
                time.sleep(0.1)
           
             
             while safe_movement_complete(axis=3) == 0:
                    time.sleep(0.01)
            #  wainting for event to trigger 
             CUP_STACK_COMPLETE_event.wait()
             
             while not packing_suction_01_event.is_set():
                sending_Ethernet_command('CIA0071')
                time.sleep(0.1)

             while not packing_suction_02_event.is_set():
                sending_Ethernet_command('CIA0051')
                time.sleep(0.1)

             

             safe_move(axis=1 , velocity= 5000 , pos=86740)

             while safe_movement_complete(axis=1) == 0:
                    time.sleep(0.01)

             CUP_STACK_COMPLETE_event.clear()
             
             safe_move(axis=1 , velocity= 5000 , pos=100)

             while safe_movement_complete(axis=1) == 0:
                    time.sleep(0.01)


             while not SR0EX_event.is_set():
                sending_Ethernet_command('CIA0040')
                time.sleep(0.1)

             safe_move(axis=3 , velocity= 5000 , pos=100)

             while safe_movement_complete(axis=3) == 0:
                    time.sleep(0.01)
             safe_move(axis=1 , velocity= 5000 , pos=86740)
             while safe_movement_complete(axis=1) == 0:
                    time.sleep(0.01)

             sending_Ethernet_command('CIA0070')
             time.sleep(0.1)
             sending_Ethernet_command('CIA0050')
             time.sleep(0.1)

             safe_move(axis=1 , velocity= 5000 , pos=100)

             while safe_movement_complete(axis=1) == 0:
                    time.sleep(0.01)
             

            




             

        time.sleep(0.1)

def PickPlace():
    while True:
        global machineRuning , home_done ,PSG04OK , PSG03OK
        if machineRuning == 1 and home_done ==True:
            safe_move(axis=7 , velocity= 4000 , pos=-210000)
            while safe_movement_complete(axis=7) == 0:
                time.sleep(0.01)

            PSG03OK = False
            PSG04OK = False
            time.sleep(0.01)
            sending_Ethernet_command('CIE0021')
            time.sleep(0.01)
            sending_Ethernet_command('CIE0031')
            
            ROBOT_ARM_COMPLETE_event.wait()
            ROBOT_ARM_COMPLETE_event.clear()


            safe_move(axis=6 , velocity= 1000 , pos=30000)
            while safe_movement_complete(axis=6) == 0:
                time.sleep(0.01)

            safe_move(axis=6 , velocity= 1000 , pos=100)
            while safe_movement_complete(axis=6) == 0:
                time.sleep(0.01)

            while not PSG03OK or not PSG04OK:
                    time.sleep(0.01)

            ROBOT_ARM_PICKING_COMPLETED_event.set()

            safe_move(axis=7 , velocity= 1500 , pos=-100)
            while safe_movement_complete(axis=7) == 0:
                time.sleep(0.01)

            safe_move(axis=6 , velocity= 1000 , pos=31534)
            while safe_movement_complete(axis=6) == 0:
                time.sleep(0.01)

            time.sleep(0.01)
            sending_Ethernet_command('CIE0020')
            time.sleep(0.01)
            sending_Ethernet_command('CIE0030')

            time.sleep(0.5)

            safe_move(axis=6 , velocity= 1000 , pos=100)
            while safe_movement_complete(axis=6) == 0:
                time.sleep(0.01)

            safe_move_relative(axis=4 , velocity= 1000 , pos=-800000)
            time.sleep(0.01)
            safe_move_relative(axis=5 , velocity= 1000 , pos=-800000)
            time.sleep(0.01)

    
    

        time.sleep(0.1)



def modbus_position_to_decimal(high_word, low_word):
    value = (high_word << 16) | low_word
    if value >= 0x80000000:
        value -= 0x100000000
    return value

def ReadMotorPos():
    for n in range(1,8):
        try:   
            data = mc.read_motor_pos(axis=n)
            time.sleep(0.01)
            pos = modbus_position_to_decimal(data.registers[0] ,data.registers[1])
            socketio.emit('MOTOR_POS', {"motor": n ,"pos": pos })
            # print(pos)
        except:
            print("Something Wrong with Axis " ,n)
            break


def ReadMotorVoltage():
    pass


def Controller_data_loader(data):
    global SRRVD , SRRVU , SRRHR , SRRHL
    global PSR01OK , PSG01OK , PSG02OK , PSR02OK , PSG03OK , PSR03OK ,PSG04OK , PSR04OK
    # Ethernet preformance teting data letancy check ----------------------------------
    # global sendtime
    # print("data comming : " , time.time_ns())
    # diff = time.time_ns() - sendtime
    # print(diff)
    # -----------------------------------------------------------------------------------
    print(data)
    if(data == 'HS00'):
        print("Heart Beat Tiggering")
    if(data[:2] == 'RI'):
        code = data[2:]
        IO_Input_Encorder(code)

    if(data == 'IMSOK'):
        IMSENSOR_event.set()

    if(data == 'SRRHR'):
        sending_Ethernet_command('SRRHR')
        SRRHR = True
        SRRHR_event.set()

    if(data == 'SRRHL'):
        sending_Ethernet_command('SRRHL') 
        SRRHL = True
        SRRHL_event.set()

    if(data == 'SRRVD'):
        sending_Ethernet_command('SRRVD') 
        SRRVD = True
        SRRVD_event.set()

        
    
    if(data == 'SRRVU'):
        sending_Ethernet_command('SRRVU') 
        SRRVU = True
        SRRVU_event.set()

    if(data == 'SR0CO'):
        sending_Ethernet_command('SR0CO') 
        SR0CO_event.set()

    if(data == 'SR0EX'):
        sending_Ethernet_command('SR0EX') 
        SR0EX_event.set()



    if(data == 'PSG01OK'):
        sending_Ethernet_command('PSG01OK') 
        PSG01OK = True

    if(data == 'PSR01OK'):
        sending_Ethernet_command('PSR01OK') 
        PSR01OK = True

    if(data == 'PSG02OK'):
        sending_Ethernet_command('PSG02OK') 
        PSG02OK = True

    if(data == 'PSR02OK'):
        sending_Ethernet_command('PSR02OK') 
        PSR02OK = True

    if(data == 'PSG03OK'):
        sending_Ethernet_command('PSG03OK') 
        PSG03OK = True

    if(data == 'PSR03OK'):
        sending_Ethernet_command('PSR03OK') 
        PSR03OK = True

    if(data == 'PSG04OK'):
        sending_Ethernet_command('PSG04OK') 
        PSG04OK = True

    if(data == 'PSR04OK'):
        sending_Ethernet_command('PSR04OK') 
        PSR04OK = True

    if(data == 'PAS01'):
        packing_suction_01_event.set()
        

    if(data == 'PAS02'):
        packing_suction_02_event.set()
        
        
        
  
def IO_output_Encorder():
    pass


def IO_Input_Encorder(code):
    data_io = bin(int(code))
    socketio.emit('IO_DATA', {"message": data_io})
    # print(data_io)
    

if __name__ == "__main__":
    # ✅ Start your background task properly
    mc = MotorController(port="COM1")

    alarms = pd.read_csv('alarms.csv' ,sep=',')
    print(alarms.head())


    socketio.start_background_task(ethernet_thread)
    socketio.start_background_task(ethernet_thread_AI)
    socketio.start_background_task(ReadMotors)
    socketio.start_background_task(PackingAxis)
    socketio.start_background_task(PickPlace)

   

    


    # ✅ Run the SocketIO server (supports WebSockets + threads)
    socketio.run(app, debug=True, use_reloader=False)
    DesableMotors()
    mc.close()

   
