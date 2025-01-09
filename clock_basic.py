import time 
import threading 
from datetime import datetime, timedelta 
import os, select, sys
import pytz # Library for accurate timezone handling, commonly used with datetime

class MommysClock: 
  def __init__(self): 
    self.current_time = datetime.now()
    self.alarm_time = None 
    self.is_running = True
    self.is_paused = False 
    self.is_24hr_mode = True
    self.timezone = pytz.timezone('Europe/Paris') # By default, we use Central European Timezone (Paris/Europe) 
    self.alarm_sound = 'Ring'
  
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
      print("Press Enter to go to menu")

      i, _, _ = select.select([sys.stdin], [], [], 1)  # Waits for input for 1 second
      if i:  # If there's input, exit the loop
          input()
          break

  def set_time(self, time_tuple): 
    hours, minutes, seconds = time_tuple
    self.current_time = self.current_time.replace(hour=hours, minute=minutes, second=seconds)
    self.clear_screen()
    print(f"Time set to {self.current_time.strftime('%H:%M:%S')}")
    print('Press Enter to return')
    input()


  def set_alarm(self, time_tuple): 
    hours, minutes, seconds = time_tuple
    self.alarm_time = self.current_time.replace(hour=hours, minute=minutes, second=seconds)
    print(f"Alarm set for {self.alarm_time.strftime('%H:%M:%S')}")
    print("Press Enter to return.")
    input()
  
  def check_alarm(self): 
    if self.alarm_time and self.current_time == self.alarm_time: 
      print("\n\n⏰ ALARM! Time to wake up! ⏰")
      print(f'{self.alarm_sound}')
      self.alarm_time = None
      

  def change_time_mode(self): 
    self.clear_screen()
    self.is_24hr_mode = not self.is_24hr_mode 
    mode = '24-hour' if self.is_24hr_mode else '12-hour AM/PM'
    print(f"Time format switched to {mode} mode.")
    print("Press Enter to return.")
    input()

  def choose_timezone(self):
    self.clear_screen()
    print('Choose a timezone:')
    timezones = ['Europe/Paris', 'UTC', 'America/New_York', 'America/Los_Angeles', 'Asia/Tokyo']
    for index, timezone in enumerate(timezones): 
      print(f'{index+1}.{timezone}')
    choice = input('Enter the number between (1-5) to choose timezone:')
    if choice.isdigit() and 1 <= int(choice) <= len(timezones): 
      self.timezone = pytz.timezone(timezones[int(choice) - 1])
      self.clear_screen()
      print(f'Timezone set to: {self.timezone}')
    else: 
      print('Choice incorrect. Please try again. Timezone by default is Europe/Paris')
    print('Press Enter to return')
    input() 
  
  def choose_alarm_sound(self): 
    self.clear_screen()
    print('Choose an alarm sound:')
    alarm_sounds = ['Ring', 'Beep', 'Melody', 'Chime']
    for index, sound in enumerate(alarm_sounds):
      print(f'{index+1}.{sound}')
    choice = input('Enter the number between (1-4) to choose alarm sound:')
    if choice.isdigit() and 1 <= int(choice) <= len(alarm_sounds):
      self.alarm_sound = alarm_sounds[int(choice) -1]
      self.clear_screen()
      print(f'Alarm sound set to: {self.alarm_sound}')
    else: 
      print("Choice incorrect. Please try again. Alarm sound by default is 'Ring'")
    print('Press Enter to return')
    input()

       
  def pause_clock(self):
    self.is_paused = True
    self.clear_screen()
    print('Clock is paused')
    print("Press Enter to return.")
    input()
  
  def resume_clock(self): 
    self.is_paused = False
    self.clear_screen()
    print('Clock resumed')
    print("Press Enter to return.")
    input()
  
  def stop_clock(self): 
    self.is_running = False
    self.clear_screen
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
    print("5. Choose Timezone")
    print("6. Choose Alarm Sound")
    print("7. Pause Clock")
    print("8. Resume Clock")
    print("9. Exit")  

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
      clock.choose_timezone()
    elif choice == '6': 
      clock.choose_alarm_sound()
    elif choice == '7':
      clock.pause_clock()
    elif choice == '8':
      clock.resume_clock()
    elif choice == '9':
      clock.stop_clock()
      break
    else:
      print("The number you have entered is incorrect. Please choose a number between 1 and 9.")

  clock_thread.join()

if __name__ == '__main__': 
  main()


