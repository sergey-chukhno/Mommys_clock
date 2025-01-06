import sys # 
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout # Importing widgets for our clock
from PyQt5.QtCore import QTimer, QTime, Qt # QtCore provides functionality not related to Qwidgets components
from PyQt5.QtGui import QFont, QFontDatabase 


class MommysClock(QWidget): # Our class inherits from QWidte class
  def __init__(self): 
    super().__init__() # Constructor to inherit the elements of the parent class 
    self.time_label = QLabel(self) # label to display the time 
    self.timer = QTimer(self) # timer attribute
    self.initUI()

  # Method to design UI of the digital clock
  def initUI(self): 
    self.setWindowTitle("Mommy's Clock")
    self.setGeometry(600, 400, 300, 100)

    vbox = QVBoxLayout() # Layout manager for our widget 
    vbox.addWidget(self.time_label) # method to add our widget 
    self.setLayout(vbox)

    # method to center our time label
    self.time_label.setAlignment(Qt.AlignCenter) # to center our time label 

    # method to style our clock
    self.time_label.setStyleSheet('font-size: 150px;'
                                  'color: blue;'
                                  'background-color: black;')
    
    
    # Setting a custom font 
    font_path = os.path.join(os.path.dirname(__file__), 'ds_digit.TTF')
    font_id = QFontDatabase.addApplicationFont(font_path) # to get a custom font
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0] # returns the list of font names
    my_font = QFont(font_family, 150) #two attributes - font family and font size
    self.time_label.setFont(my_font)
    
    self.timer.timeout.connect(self.update_time) # We connect the timer to the slot to update time
    self.timer.start(1000) # we update our time every 1000 milliseconds, i.e. every second
    
    self.update_time()

  # method to update time 
  def update_time(self): 
    current_time = QTime.currentTime().toString('hh:mm:ss AP') # We use to string method to convert it to the string that we put on the screen. AP is used to display AM/PM
    self.time_label.setText(current_time) 


if __name__ == '__main__': 
  app = QApplication(sys.argv) # App object of QApplication class
  clock = MommysClock() #Clock object which is the object of our MoommysClock class 
  clock.show() # show method on our object clock
  sys.exit(app.exec_())