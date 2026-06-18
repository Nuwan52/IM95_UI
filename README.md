# 🏭 Industrial Automation Control System (Flask + SocketIO)

A real-time industrial machine control system built using **Flask**, **Flask-SocketIO**, and **UDP communication**, integrated with a custom **motor controller**. This system is designed for **multi-axis robotic automation**, enabling synchronized motion control, IO handling, and live monitoring via a web interface.

---

## 🚀 Features

- ⚡ Real-time communication using WebSockets (Socket.IO)
- 🎯 Multi-axis motor control (up to 7 axes)
- 🔄 Automated motion sequences with synchronization signals
- 🧠 Homing and initialization routines
- 📡 UDP-based communication with external controllers / PLCs
- 🧾 Alarm monitoring and fault handling
- 📊 Live motor position and IO visualization
- 🖥️ Web-based control dashboard

---

## 🏗️ System Architecture


<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/eb76d63c-dec4-473e-87f7-a58e6c6d3ceb" />


## Project Structure

```text
├── app.py                # Main Flask application
├── motor.py              # Motor controller interface
├── templates/
│   ├── index.html
│   ├── analytics.html
│   ├── settings.html
│   └── item-settings.html
├── static/               # CSS, JS, assets
├── alarms.csv            # Alarm definitions
└── README.md
```

---

## ⚙️ Technologies Used

- Python 3.x
- Flask
- Flask-SocketIO
- Pandas
- UDP Sockets
- Custom Motor Control API (Modbus-based)

---

## 🔌 Hardware Integration

- Multi-axis motor drivers (7 axes supported)
- Industrial IO system via UDP
- Sensors:
  - Position sensors (SRRVD, SRRVU, etc.)
  - Presence sensors (PSG/PSR signals)
- External controller / PLC

---

## 🧠 Core Functionalities

### 1. Motor Initialization
- Torque configuration
- Software limits setup
- Alarm clearing
- Motor enabling

---

### 2. Homing Sequence

Executed once before operation:

- Axis 2 → Cup arm  
- Axis 1 → Z axis  
- Axis 3 → X axis  
- Axis 6 & 7 → High-speed arm  

---

### 3. Automated Operation Loop

The system executes a synchronized pick-and-place style sequence:

- Multi-axis coordinated motion
- IO-triggered state transitions
- Sensor-based synchronization:
  - `SRRVD`, `SRRVU`, `SRRHL`, `SRRHR`
- Conveyor and actuator control via UDP commands

---

### 4. Real-Time Monitoring

- Motor position streaming via Socket.IO
- IO status updates
- Alarm broadcasting to frontend

---

## 🌐 API / Socket Events

### Client → Server

| Event | Description |
|------|------------|
| `INIT` | Initialize system |
| `START_STOP` | Start/Stop machine |
| `SOLONOID_ONOFF` | Control IO outputs |
| `SERVO_CONTROL_MANUAL` | Manual motor movement |
| `IO_DATA_REQUEST` | Request IO states |
| `ESTOP` | Emergency stop |

---

### Server → Client

| Event | Description |
|------|------------|
| `MOTOR_POS` | Motor position updates |
| `IO_DATA` | IO state updates |
| `ALARM` | Alarm notifications |
| `INIT_BACKEND` | Initialization status |

---

## 🔄 Communication Protocol

### UDP Commands Example

| Command | Function |
|--------|--------|
| `CIF0010` | Turn ON output 1 |
| `CIF0011` | Turn OFF output 1 |
| `SRRVD` | Sensor feedback (Down) |
| `PSG01OK` | Presence sensor OK |

---

## 🧪 Running the Project

### 1. Install Dependencies

```bash
pip install flask flask-socketio pandas
```
###  Run the Sever 
```bash
python app.py
```
### Open UI
```bash
http://localhost:5000
