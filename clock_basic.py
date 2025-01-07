import time 
import threading 
from datetime import datetime, timedelta # Timedelta is a class in time module that represents a duration (difference between two dates or times). 
import os

class MommysClock: 
  def __init__(self): 
    self.current_time = datetime.now()
    self.alarm_time = None 
    self.is_running = True
    self.is_paused = False 
    self.is_24hr_mode = True # By default, the clock is in 24-hour mode
  
  # Run the clock
  def run_clock(self): 
    while self.is_running: 
      if not self.is_paused: 
        self.current_time += timedelta(seconds = 1) # We increment current time by one second (deltatime)
        self.display_time() # We show time
        self.check_alarm() # We check for alarm time if it is set
        time.sleep(1)
  
  # Method to display time in terminal 
  def display_time(self):
    # we check for time mode (12hrs or 24hrs)
    if self.is_24hr_mode: 
      print("\r" + self.current_time.strftime("%H:%M:%S"), end="", flush=True) # '\r' rewrites the same line in the terminal, strftime method turns current time to string, flush forces the output to be immediately printed in terminal (without being buffered first)
    else: 
      print("\r" + self.current_time.strftime("%I:%M:%S %p"), end="", flush=True) # Similar to the previous print, but time is shown in 12-hour AM/PM mode
  
  # Method to set time
  def set_time(self, time_tuple): 
    hours, minutes, seconds = time_tuple
    self.current_time = self.current_time.replace(hour=hours, minute=minutes, second=seconds)
    print(f"\nTime set to {self.current_time.strftime('%H:%M:%S')}")
  
  # Method to set alarm time
  def set_alarm(self, time_tuple): 
    hours, minutes, seconds = time_tuple
    self.alarm_time = self.current_time.replace(hour=hours, minute=minutes, second=seconds)
    print(f"\nAlarm set for {self.alarm_time.strftime('%H:%M:%S')}")
  
  # Method to check if it's time for alarm to ring
  def check_alarm(self): 
    if self.alarm_time and self.current_time == self.alarm_time: 
      print("\n\n\u23F0 ALARM! Time to wake up! \u23F0")
      self.alarm_time = None # Reset alarm time to none 
  # Here we need to decide what if current_time is greater than alarm time. 
  # To check if current time is in 12-hour mode and alarm time is always set in 24-hour mode, what we are to do 

  # Method to change time format 
  def change_time_mode(self): 
    self.is_24hr_mode = not self.is_24hr_mode # Flip between 12-hr and 24-hr modes
    mode = '24-hour' if self.is_24hr_mode else '12-hour AM/PM'
    print(f"\nTime format switched to {mode} mode.")
  
  # Method to pause our clock
  def pause_clock(self):
    self.is_paused = True
    print('\nClock is paused')
  
  # Method to resume clock
  def resume_clock(self): 
    self.is_paused = False
    print('\nClock resumed')
  
  # Method to stop clock 
  def stop_clock(self): 
    self.is_running = False
    print('\nClock stopped')
  
   # Method to clear terminal screen
  def clear_screen(self):
    # Clear the screen depending on the operating system
    if os.name == 'nt':  # Windows
      os.system('cls')
    else:  # Linux/Mac
      os.system('clear')

# main funct
def main(): 
  clock = MommysClock()
  clock_thread = threading.Thread(target=clock.run_clock)
  clock_thread.daemon = True
  clock_thread.start()

  while True: 
    clock.clear_screen()
    print("\n\n---Menu ---")
    print("1. Set Time")
    print("2. Set Alarm")
    print("3. Change 12/24 Hour Mode")
    print("4. Pause Clock")
    print("5. Resume Clock")
    print("6. Exit")  

    choice = input('Enter your choice:')

    if choice == '1': 
       time_tuple = tuple(map(int, input("Enter time (hh mm ss): ").split()))
       clock.set_time(time_tuple)
    elif choice == '2':
        time_tuple = tuple(map(int, input("Set alarm for (hh mm ss): ").split()))
        clock.set_alarm(time_tuple)
    elif choice == '3':
        clock.change_time_mode()
    elif choice == '4':
        clock.pause_clock()
    elif choice == '5':
        clock.resume_clock()
    elif choice == '6':
        clock.stop_clock()
        break
    else:
        print("Invalid choice. Please try again.")

  clock_thread.join()

if __name__ == '__main__': 
   main()
    


  



