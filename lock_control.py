import time

class SimulatedGPIO:
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"
    BCM = "BCM"

    @staticmethod
    def setmode(mode):
        print(f"Setting GPIO mode to {mode}")

    @staticmethod
    def setup(pin, mode):
        print(f"Setting up pin {pin} in mode {mode}")

    @staticmethod
    def output(pin, state):
        print(f"Setting pin {pin} to state {state}")

    @staticmethod
    def cleanup():
        print("Cleaning up GPIO")

# Replace RPi.GPIO with our simulated version
GPIO = SimulatedGPIO

LOCK_PIN = 18  # This is now just a simulated pin number

def setup_lock():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LOCK_PIN, GPIO.OUT)
    GPIO.output(LOCK_PIN, GPIO.HIGH)  # Simulating locked state
    print("Lock setup complete")

def open_lock():
    GPIO.output(LOCK_PIN, GPIO.LOW)
    print("Lock opened")
    time.sleep(5)  # Keep the lock open for 5 seconds
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    print("Lock closed")

def cleanup_lock():
    GPIO.cleanup()

# Test the functions
if __name__ == "__main__":
    setup_lock()
    open_lock()
    cleanup_lock()
