import threading
import queue

def drive(speed_queue):
    speed = 1
    while True:
        try:
            speed = speed_queue.get(1)
            if speed == 0:
                break
        except queue.Empty:
            pass
        print("speed:", speed)

def main():
    speed_queue = queue.Queue()
    threading.Thread(target=drive, args=(speed_queue,)).start()
    while True:
        speed = int(input("Enter 0 to Exit or 1/2/3 to continue: "))
        speed_queue.put(speed)
        if speed == 0:
            break

main()