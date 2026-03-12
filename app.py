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


PSR01OK  = False
PSG01OK  = False
PSR02OK  = False
PSG02OK  = False




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
        mc.homing(axis=2 , direction=1) # cup sucking arm aixs 
        time.sleep(5)
        mc.homing(axis=1 ,direction=1) #stacking robot z axis 
        time.sleep(5)
        mc.homing(axis=3 , direction=1) # stacking robot x axis
        time.sleep(5) 
        mc.homing(axis=6 ,direction=1) #high speed arm Z
        time.sleep(5) 
        mc.homing(axis=7 , direction=0) #high speed arm x
        time.sleep(5)
        print("home done")
        home_done = True

   
    
    
    # mc.send_immediate_trigger(pos=135000 , velocity=100 , slave_id=2)

    # if data == 1:
    #     mc.send_immediate_trigger(pos=-150000 , velocity=100 , slave_id=3)
    #     mc.send_immediate_trigger(pos=30000 , velocity=100 , slave_id=2)
    # else:
    #     mc.send_immediate_trigger(pos=-1000 , velocity=100 , slave_id=3)
    #     mc.send_immediate_trigger(pos=1000 , velocity=100 , slave_id=2)
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

    mc.MotorToqueSetting(axis=1  ,toque=200)
    mc.MotorToqueSetting(axis=2  ,toque=400)
    mc.MotorToqueSetting(axis=3  ,toque=400)
    mc.MotorToqueSetting(axis=6  ,toque=200)
    mc.MotorToqueSetting(axis=7  ,toque=400)
    
    
    

    mc.MinSoftwareLimit(axis=6 , min= 100)

    # time.sleep(1)

    mc.MaxSoftwareLimit(axis=6 , Max=35000)


    mc.MinSoftwareLimit(axis=2 , min= 100)

    # time.sleep(1)

    mc.MaxSoftwareLimit(axis=2 , Max=130000)



    mc.MinSoftwareLimit(axis=7 , min= -210000)

    # time.sleep(1)

    mc.MaxSoftwareLimit(axis=7 , Max=-100)



    mc.MinSoftwareLimit(axis=3 , min= 100)

    # time.sleep(1)

    mc.MaxSoftwareLimit(axis=3 , Max=300000)


    mc.MinSoftwareLimit(axis=1 , min= 10)

    # time.sleep(1)

    mc.MaxSoftwareLimit(axis=1 , Max=1000)


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
        


def ethernet_thread_AI():
    """Example background thread function."""
    while True:
        data, addr = sock_02.recvfrom(1024)
        print("AI Received:", data.decode())
        
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
            global PSR01OK , PSG01OK , PSG02OK , PSR02OK

            if machine_setting_mode == 1:
                ReadMotorPos()
                time.sleep(0.5)

            if machineRuning == 1 and home_done ==True:
                print("Loop exicuting")
                Movement_exicuter_relative(axis=4 , velocity= 500 , pos=-1000000)
                time.sleep(0.01)
                Movement_exicuter_relative(axis=5 , velocity= 500 , pos=-1000000)
                
                Movement_exicuter(axis=2 , velocity= 3000 , pos=130000)

                Movement_exicuter(axis=3 , velocity= 5000 , pos=300000)
                SRRVD = False
                SRRVU = False
                SRRHL = False
                SRRHR = False
                
                
                sending_Ethernet_command('CIF0031')
                while not SRRVD:
                    time.sleep(0.01)
                sending_Ethernet_command('CIF0011')
                 
               
                while movement_complete(axis=2) == 0 and not SRRHR:
                    time.sleep(0.01)

                SRRVD = False
                SRRVU = False
                SRRHL = False
                SRRHR = False
                sending_Ethernet_command('CIF0010') 
                while not SRRHL:
                    time.sleep(0.01)

                sending_Ethernet_command('CIF0030')  
                while not SRRVU:
                    time.sleep(0.01)
                
                
                Movement_exicuter(axis=7 , velocity= 4000 , pos=-210000)
                Movement_exicuter(axis=2 , velocity= 4000 , pos=100)
                
                while movement_complete(axis=2) == 0:
                    time.sleep(0.01)
                 

                Movement_exicuter(axis=6 , velocity= 1000 , pos=15000)
                while movement_complete(axis=6) == 0:
                    time.sleep(0.01)
                    

                Movement_exicuter(axis=6 , velocity= 1000 , pos=100)
                while movement_complete(axis=6) == 0:
                    time.sleep(0.01)
                    

                Movement_exicuter(axis=2 , velocity= 4000 , pos=130000)
                Movement_exicuter(axis=7 , velocity= 4000 , pos=-100)
                SRRVD = False
                SRRVU = False
                SRRHL = False
                SRRHR = False

                
                sending_Ethernet_command('CIF0031') 

                while not SRRVD:
                    time.sleep(0.01)

                sending_Ethernet_command('CIF0011')


                
                
                
                while movement_complete(axis=7) == 0 and not SRRHR:
                    time.sleep(0.01)
                    

                Movement_exicuter(axis=6 , velocity= 1000 , pos=15000)
                while movement_complete(axis=6) == 0:
                    time.sleep(0.01)
                    

                Movement_exicuter(axis=6 , velocity= 1000 , pos=100)
                Movement_exicuter(axis=3 , velocity= 5000 , pos=100)
                
                while movement_complete(axis=3) == 0:
                    time.sleep(0.01)
                while movement_complete(axis=6) == 0:
                    time.sleep(0.01)
                    
                    
                    
                
                
                
                

                


                    
                   
                # status = mc.send_immediate_trigger(pos=-100 , velocity=1000, slave_id=7)
                # if status == 0:
                #     print("Modbus Failure")
                #     machineRuning = 0
                #     break 
                # mc.send_immediate_trigger(pos=-150000 , velocity=motorVelocity_x , slave_id=3)
                # mc.send_immediate_trigger(pos=30000 , velocity=motorVelocity_z , slave_id=2)
                # time.sleep(0.5)
                # mc.send_immediate_trigger(pos=1000 , velocity=motorVelocity_z , slave_id=2)
                # time.sleep(0.5)
                # mc.send_immediate_trigger(pos=-1000 , velocity=motorVelocity_x , slave_id=3)
                
                 
                # status = mc.send_immediate_trigger(pos=100000 , velocity=3000, slave_id=2)
                
                # if status == 0:
                #     print("Modbus Failure")
                #     machineRuning = 0
                #     break 

                # mc.send_immediate_trigger(pos=30000 , velocity=motorVelocity_z , slave_id=2)
                # time.sleep(0.5)
                # mc.send_immediate_trigger(pos=1000 , velocity=motorVelocity_z , slave_id=2)
                # time.sleep(0.5)


            
            # sending_Ethernet_command('CIB0011')
            # time.sleep(0.01)
            # sending_Ethernet_command('CIB0010')
            # time.sleep(0.01)



            # sending_Ethernet_command('CIB0021')
            # time.sleep(0.01)
            # sending_Ethernet_command('CIB0020')
            # time.sleep(0.01)


            # sending_Ethernet_command('CIB0031')
            # time.sleep(0.01)
            # sending_Ethernet_command('CIB0030')
            # time.sleep(0.01)


            # sending_Ethernet_command('CIB0041')
            # time.sleep(0.01)
            # sending_Ethernet_command('CIB0040')
            # time.sleep(0.01)


            # sending_Ethernet_command('CIB0051')
            # time.sleep(0.01)
            # sending_Ethernet_command('CIB0050')
            # time.sleep(0.01)


            # sending_Ethernet_command('CIB0061')
            # time.sleep(0.05)
            # sending_Ethernet_command('CIB0060')
            # time.sleep(0.05)

            # sending_Ethernet_command('CIB0071')
            # time.sleep(0.05)
            # sending_Ethernet_command('CIB0070')
            # time.sleep(0.05)

            # ReadMotorPos()
            # ReadMotorAlams()

            # sending_Ethernet_command('CIB0081')
            # time.sleep(0.05)
            # sending_Ethernet_command('CIB0080')
            # time.sleep(0.05)
            # ReadMotorPos()
            # ReadMotorVoltage()
            #  Motorstatus()
            # ReadMotorAlams()
            # Ethenrnet preformance testing ----------------------------------------------------
            # global sendtime
            # sendtime = time.time_ns()
            # print("sending time : " , sendtime)
            # sending_Ethernet_command("CIA655")
            # -----------------------------------------------------------------------------------
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
            print(pos)
        except:
            print("Something Wrong with Axis " ,n)
            break


def ReadMotorVoltage():
    pass


def Controller_data_loader(data):
    global SRRVD , SRRVU , SRRHR , SRRHL
    global PSR01OK , PSG01OK , PSG02OK , PSR02OK
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


    if(data == 'SRRHR'):
        sending_Ethernet_command('SRRHR')
        SRRHR = True

    if(data == 'SRRHL'):
        sending_Ethernet_command('SRRHL') 
        SRRHL = True

    if(data == 'SRRVD'):
        sending_Ethernet_command('SRRVD') 
        SRRVD = True
        
    
    if(data == 'SRRVU'):
        sending_Ethernet_command('SRRVU') 
        SRRVU = True

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
        
        
  
def IO_output_Encorder():
    pass


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

   
