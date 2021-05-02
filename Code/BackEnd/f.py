import threading
import queue
import os

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

#print(os.getcwd() + "\\..\\DB\\cameraPhotos\\" + "192-168-0-176-8080" + ".jpg")
os.remove(os.getcwd() + "\\..\\DB\\cameraPhotos\\" + "192-168-0-176-8080" + ".jpg")