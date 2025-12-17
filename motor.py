from pymodbus.client import ModbusSerialClient
import time


class MotorController:
    def __init__(self, port="COM1", baudrate=38400, timeout=0.01):
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity="N",
            stopbits=2,
            timeout=timeout
        )

        if not self.client.connect():
            raise Exception("❌ Failed to connect to Modbus device")
        else:
            print("✅ Modbus Connected")

    # ============================
    #   BASIC READ FUNCTIONS
    # ============================

    def read_motor_pos(self , axis):
        rr = self.client.read_holding_registers(device_id=axis, address=0X602C, count=2)
        return rr

    def read_current_alarm(self, axis):
        rr = self.client.read_holding_registers(device_id=axis, address=0x0B03, count=1)
        print(rr.registers)
        return rr

    def read_bus_voltage(self, axis):
        rr = self.client.read_holding_registers(device_id=axis, address=0x0B0A, count=1)
        print(rr.registers)

    def read_driver_temp(self, axis):
        rr = self.client.read_holding_registers(device_id=axis, address=0x0B0B, count=1)
        print(rr.registers)

    def read_driver_current(self, axis):
        rr = self.client.read_holding_registers(device_id=axis, address=0x0B08, count=1)
        print(rr.registers)

    def read_driver_status(self, axis):
        rr = self.client.read_holding_registers(device_id=axis, address=0x0B05, count=1)
        print(bin(rr.registers[0]))
        return rr

    # ============================
    #      MOTION CONTROL
    # ============================

    def send_immediate_trigger(self, pos, velocity=4000, slave_id=1):

        mode = 0x0001
        acceleration = 50
        deceleration = 50
        delay = 0
        trigger = 0x0010

        pos_high = (pos >> 16) & 0xFFFF
        pos_low = pos & 0xFFFF

        registers = [
            mode,
            pos_high,
            pos_low,
            velocity,
            acceleration,
            deceleration,
            delay,
            trigger
        ]

        print(f"\n=== Sending Trigger to Axis {slave_id} ===")

        rr = self.client.write_registers(
            address=0x6200,
            values=registers,
            device_id=slave_id
        )

        if rr.isError():
            print(f"❌ Error writing immediate trigger: {rr}")
        else:
            print(f"✅ Trigger OK (Axis {slave_id})")
            time.sleep(0.01)

    # ============================
    #     MOTOR ENABLE / DISABLE
    # ============================

    def enable_motor(self, axis):
        try:
            return self.client.write_register(address=0x0409, value=0x0083, device_id=axis)
        except:
            return 0

        

    def disable_motor(self, axis):
        try:
            return self.client.write_register(address=0x0409, value=0x0003, device_id=axis)
        except:
            return 0
            
        

    def estop(self, axis):
        return self.client.write_register(address=0x6002, value=0x0040, device_id=axis)

    def clear_alarm(self, axis):
        return self.client.write_register(address=0x0033, value=0x1111, device_id=axis)

    def jog(self, axis):
        return self.client.write_register(address=0x0033, value=0x4001, device_id=axis)

    # ============================
    #          HOMING
    # ============================

    def homing(self, axis):
        sequence = [
            (0X600A, 0x0004),
            (0X600F, 0x0064),
            (0X6010, 0x001E),
            (0X6002, 0x0020)
        ]
        for addr, value in sequence:
            rr = self.client.write_register(address=addr, value=value, device_id=axis)
            time.sleep(0.01)
            print(rr)

    def homing_all(self, axes=[1, 2, 3, 4]):
        for axis in axes:
            print(f"\n=== Homing Axis {axis} ===")
            self.homing(axis)

    def close(self):
        self.client.close()
        print("🔌 Modbus Disconnected")



