import socket
import time

# --- Configuration ---
# Replace with the IP address of your Arduino/ESP32
UDP_IP = "169.254.24.26"
UDP_PORT = 5001

# --- Python Client ---
def send_message(message):
    """Sends a UDP message to the specified IP and port."""
    print(f"Sending message: '{message}' to {UDP_IP}:{UDP_PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    send_message("Hello from Python!")
    time.sleep(1)
    send_message("How is it going?")
