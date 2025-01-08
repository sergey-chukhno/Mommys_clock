import sys # 
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QInputDialog # Importing widgets for our clock
from PyQt5.QtCore import QTimer, QTime, Qt # QtCore provides functionality not related to Qwidgets components
from PyQt5.QtGui import QFont, QFontDatabase 


class MommysClock(QWidget): # Our class inherits from QWidte class
  def __init__(self): 
    super().__init__() # Constructor to inherit the elements of the parent class 
    self.time_label = QLabel(self) # label to display the time 
    self.timer = QTimer(self) # timer attribute
    self.is_paused = False # Boolean to track if the clock is paused. 
    self.is_24hr_mode = False # Boolean to track time mode. By default, we set 12-hours AM/PM mode
    self.alarm_time = None # We initialize our alarm time variable. Initially, we have no alarm. 
    self.custom_time = None # Manually set time 
    self.initUI()

  # Method to design UI of the digital clock
  def initUI(self): 
    self.setWindowTitle("Mommy's Clock")
    self.setGeometry(600, 400, 300, 100)

   # Main vertcial layout
    main_layout = QVBoxLayout()

    # Time label on top
    self.time_label.setAlignment(Qt.AlignCenter) # to center our time label 
    self.time_label.setStyleSheet('font-size: 150px;'
                                  'color: blue;'
                                  'background-color: black;')
    main_layout.addWidget(self.time_label)

    # Spacer to push buttons down
    main_layout.addStretch(1)

    # Horizontal layout for buttons
    button_layout = QHBoxLayout()
    button_layout.setSpacing(60)

    # Set time button
    self.set_time_button = QPushButton('Set Time', self)
    self.set_time_button.clicked.connect(self.set_time_dialog)
    self.set_time_button.setFixedSize(140, 140)
    button_layout.addWidget(self.set_time_button)

    # Set alarm button
    self.set_alarm_button = QPushButton('Set Alarm', self)
    self.set_alarm_button.clicked.connect(self.set_alarm_dialog)
    self.set_alarm_button.setFixedSize(140, 140)
    button_layout.addWidget(self.set_alarm_button)

    # Pause/resume button
    self.pause_button = QPushButton('Pause', self)
    self.pause_button.clicked.connect(self.toggle_pause)
    self.pause_button.setFixedSize(140,140)
    button_layout.addWidget(self.pause_button)

    # Change time mode button
    self.change_time_mode_button = QPushButton('Time Mode', self)
    self.change_time_mode_button.clicked.connect(self.change_time_mode)
    self.change_time_mode_button.setFixedSize(140,140)
    button_layout.addWidget(self.change_time_mode_button)

    # Center the button layout horizontally
    button_container = QHBoxLayout()
    button_container.addStretch(1) # Push buttons to center
    button_container.addLayout(button_layout)
    button_container.addStretch(1)

    # Add buttons to main layout
    main_layout.addLayout(button_container)
    main_layout.addStretch(1)

    # Set layout
    self.setLayout(main_layout)

    # Apply button styling
    self.set_time_button.setStyleSheet(self.button_style())
    self.set_alarm_button.setStyleSheet(self.button_style())
    self.pause_button.setStyleSheet(self.button_style())
    self.change_time_mode_button.setStyleSheet(self.button_style())
    
    # Set custom font
    font_path = os.path.join(os.path.dirname(__file__), 'ds_digit.TTF')
    font_id = QFontDatabase.addApplicationFont(font_path) # to get a custom font
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0] # returns the list of font names
    my_font = QFont(font_family, 150) #two attributes - font family and font size
    self.time_label.setFont(my_font)
    
    # Set timer to update time
    self.timer.timeout.connect(self.update_time) 
    self.timer.start(1000) # Update every 1000 miliseconds (every second)
    
    self.update_time()
  
  # Define buttons style
  def button_style(self):
    return '''
        QPushButton {
            font-size: 18px;
            background-color: #4CAF50;  /* Green background */
            color: white;  /* White text */
            border-radius: 15px;  /* Round corners */
            padding: 20px;  /* Padding inside the button */
            margin: 5px;  /* Space between buttons */
        }
        QPushButton:hover {
            background-color: #45a049;  /* Darker green when hovered */
        }
        QPushButton:pressed {
            background-color: #388e3c;  /* Even darker green when clicked */
        }
'''

  # method to update time 
  def update_time(self): 
    if not self.is_paused: # If the clock is running
      if self.custom_time: 
        self.custom_time = self.custom_time.addSecs(1)

        if self.is_24hr_mode:
          time_string = self.custom_time.toString('HH:mm:ss')
        else: 
          time_string = self.custom_time.toString('hh:mm:ss AP')
      
      else: 
        current_time = QTime.currentTime()
        # If 24-hour mode, show time in 'HH:mm:ss'
        if self.is_24hr_mode:
          time_string = current_time.toString('HH:mm:ss')
        else: 
          time_string = current_time.toString('hh:mm:ss AP')

    self.time_label.setText(time_string) 

    # Check for alarm time
    # Check time (use custom time or system time)
    check_time = self.custom_time if self.custom_time else QTime.currentTime()
    if self.alarm_time: 
      # we check for the format of set alarm time (we need to make sure that alarm time and current time are in the same mode)
      if self.is_24hr_mode:
        # if 24 hrs mode, compare in 'HH:mm:ss'
        formatted_current_time = check_time.toString('HH:mm:ss')
        formatted_alarm_time = self.alarm_time.toString('HH:mm:ss')
      else:
        # if 12-hrs-mode, compare in 'hh:mm:ss AP'
        formatted_current_time = check_time.toString('hh:mm:ss AP')
        formatted_alarm_time = self.alarm_time.toString('hh:mm:ss AP')
      
      # Check if the current time matches alarm time
      if formatted_current_time == formatted_alarm_time: 
        self.show_alarm_message()
  
  # Method to set a clock to a specific time
  def set_time(self, time_tuple): 
    hours, minutes, seconds = time_tuple 
    self.timer.stop() # Stop the timer temporarily while we are setting time
    self.custom_time = QTime(hours, minutes, seconds)
    self.alarm_time = None # Clear alarm when setting the time
    self.time_label.setText(self.custom_time.toString('hh:mm:ss AP'))
    self.timer.start(1000) # Restart timer

  # Set alarm at a specific time
  def set_alarm(self, alarm_tuple):
    hours, minutes, seconds = alarm_tuple
    self.alarm_time = QTime(hours, minutes, seconds)
  
  # Show a pop-up message when the alarm time is reached
  def show_alarm_message(self): 
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText('Alarm ringing')
    msg.setWindowTitle('Alarm!')
    msg.exec_()
  
  # Pause/resume time
  def toggle_pause(self): 
    if self.is_paused: 
      self.is_paused = False
      self.timer.start(1000) # Restart timer
    else: 
      self.is_paused = True
      self.timer.stop()
  
  # Change tiome mode (between 12-hours and 24-hours modes)
  def change_time_mode(self): 
    self.is_24hr_mode = not self.is_24hr_mode # Flip between 12 and 24 hrs modes
    self.update_time() # Update display with new time format 
  
  # Method to promopt user to input time for set_time function
  def set_time_dialog(self):
    text, ok = QInputDialog.getText(self, 'Set Time', 'Enter time: (hh:mm:ss):')
    if ok and text: 
      try: 
        hours, minutes, seconds = map(int, text.split(':'))
        self.set_time((hours, minutes, seconds))
      except ValueError: 
        self.show_error_message('Invalid time format! Please use hh:mm:ss.')
  
  # Method to promopt user to input time time for set_alarm function
  def set_alarm_dialog(self): 
    text, ok = QInputDialog.getText(self, 'Set Alarm Time', 'Enter time: (hh:mm:ss):')
    if ok and text: 
      try: 
        hours, minutes, seconds = map(int, text.split(':'))
        self.set_alarm((hours, minutes, seconds))
      except ValueError: 
        self.show_error_message('Invalid alarm format! Please use hh:mm:ss.')
  
  # Show an error message box 
  def show_error_message(self, message): 
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle('Error')
    msg.exec_()
  
if __name__ == '__main__': 
  app = QApplication(sys.argv) # App object of QApplication class
  clock = MommysClock() #Clock object which is the object of our MoommysClock class 
  clock.show() # show method on our object clock
  sys.exit(app.exec_())