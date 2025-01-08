import time 
import threading 
from datetime import datetime, timedelta 
import os, select, sys

class MommysClock: 
  def __init__(self): 
    self.current_time = datetime.now()
    self.alarm_time = None 
    self.is_running = True
    self.is_paused = False 
    self.is_24hr_mode = True 
  
  def run_clock(self): 
    while self.is_running: 
      if not self.is_paused: 
        self.current_time += timedelta(seconds =1) 
        self.check_alarm() 
        time.sleep(1) 
  
  def display_time(self):
    while True:
      self.clear_screen()
      if self.is_24hr_mode: 
        print(self.current_time.strftime("%H:%M:%S")) 
      else: 
        print(self.current_time.strftime("%I:%M:%S %p")) 
      print("Press Enter to return to menu.")

      i, _, _ = select.select([sys.stdin], [], [], 1)  # Waits for input for 1 second
      if i:  # If there's input, exit the loop
          input()
          break

      

  def set_time(self, time_tuple): 
    hours, minutes, seconds = time_tuple
    self.current_time = self.current_time.replace(hour=hours, minute=minutes, second=seconds)
    print(f"Time set to {self.current_time.strftime('%H:%M:%S')}")
    print("Press Enter to return to menu.")
    input()

  def set_alarm(self, time_tuple): 
    hours, minutes, seconds = time_tuple
    self.alarm_time = self.current_time.replace(hour=hours, minute=minutes, second=seconds)
    print(f"Alarm set for {self.alarm_time.strftime('%H:%M:%S')}")
    print("Press Enter to return to menu.")
    input()
  
  def check_alarm(self): 
    if self.alarm_time and self.current_time == self.alarm_time: 
      print("\n\n⏰ ALARM! Time to wake up! ⏰")
      self.alarm_time = None 

  def change_time_mode(self): 
    self.is_24hr_mode = not self.is_24hr_mode 
    mode = '24-hour' if self.is_24hr_mode else '12-hour AM/PM'
    print(f"Time format switched to {mode} mode.")
    print("Press Enter to return to menu.")
    input()

  def pause_clock(self):
    self.is_paused = True
    print('Clock is paused')
    print("Press Enter to return to menu.")
    input()
  
  def resume_clock(self): 
    self.is_paused = False
    print('Clock resumed')
    print("Press Enter to return to menu.")
    input()
  
  def stop_clock(self): 
    self.is_running = False
    print('Clock stopped')

  def clear_screen(self):
    if os.name == 'nt':  
      os.system('cls')
    else:  
      os.system('clear')


def main(): 
  clock = MommysClock()
  clock_thread = threading.Thread(target=clock.run_clock)
  clock_thread.daemon = True
  clock_thread.start()

  while True: 
    clock.display_time()
    clock.clear_screen()
    print("\n\n--- Menu ---")
    print("1. Display Time")
    print("2. Set Time")
    print("3. Set Alarm")
    print("4. Change 12/24 Hour Mode")
    print("5. Pause Clock")
    print("6. Resume Clock")
    print("7. Exit")  

    choice = input('Enter your choice: ')

    if choice == '1': 
      clock.display_time()
    elif choice == '2':
      time_tuple = tuple(map(int, input("Enter time (hh mm ss): ").split()))
      clock.set_time(time_tuple)
    elif choice == '3':
      time_tuple = tuple(map(int, input("Set alarm for (hh mm ss): ").split()))
      clock.set_alarm(time_tuple)
    elif choice == '4':
      clock.change_time_mode()
    elif choice == '5':
      clock.pause_clock()
    elif choice == '6':
      clock.resume_clock()
    elif choice == '7':
      clock.stop_clock()
      break
    else:
      print("The number you have entered is incorrect. Please choose a number between 1 and 7.")

  clock_thread.join()

if __name__ == '__main__': 
  main()

