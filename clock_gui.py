import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QInputDialog, QComboBox, QRadioButton, QDialog, QVBoxLayout as RadioButtonLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase
from pytz import timezone
from datetime import datetime


class MommysClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.is_paused = False
        self.is_24hr_mode = False
        self.alarm_time = None
        self.custom_time = None
        self.time_zone = 'Europe/Paris'  # Default time zone
        self.alarm_sound = 'Ring'  # Default alarm sound
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mommy's Clock")
        self.setGeometry(600, 400, 300, 100)

        main_layout = QVBoxLayout()

        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet('font-size: 150px;'
                                      'color: blue;'
                                      'background-color: black;')
        main_layout.addWidget(self.time_label)

        main_layout.addStretch(1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(60)

        self.set_time_button = QPushButton('Set Time', self)
        self.set_time_button.clicked.connect(self.set_time_dialog)
        self.set_time_button.setFixedSize(140, 140)
        button_layout.addWidget(self.set_time_button)

        self.set_alarm_button = QPushButton('Set Alarm', self)
        self.set_alarm_button.clicked.connect(self.set_alarm_dialog)
        self.set_alarm_button.setFixedSize(140, 140)
        button_layout.addWidget(self.set_alarm_button)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setFixedSize(140, 140)
        button_layout.addWidget(self.pause_button)

        self.change_time_mode_button = QPushButton('Time Mode', self)
        self.change_time_mode_button.clicked.connect(self.change_time_mode)
        self.change_time_mode_button.setFixedSize(140, 140)
        button_layout.addWidget(self.change_time_mode_button)

        self.set_time_zone_button = QPushButton('Set Time Zone', self)
        self.set_time_zone_button.clicked.connect(self.set_time_zone_dialog)
        self.set_time_zone_button.setFixedSize(140, 140)
        button_layout.addWidget(self.set_time_zone_button)

        self.set_alarm_sound_button = QPushButton('Set Alarm Sound', self)
        self.set_alarm_sound_button.clicked.connect(self.set_alarm_sound_dialog)
        self.set_alarm_sound_button.setFixedSize(140, 140)
        button_layout.addWidget(self.set_alarm_sound_button)

        button_container = QHBoxLayout()
        button_container.addStretch(1)
        button_container.addLayout(button_layout)
        button_container.addStretch(1)

        main_layout.addLayout(button_container)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.set_time_button.setStyleSheet(self.button_style())
        self.set_alarm_button.setStyleSheet(self.button_style())
        self.pause_button.setStyleSheet(self.button_style())
        self.change_time_mode_button.setStyleSheet(self.button_style())
        self.set_time_zone_button.setStyleSheet(self.button_style())
        self.set_alarm_sound_button.setStyleSheet(self.button_style())

        font_path = os.path.join(os.path.dirname(__file__), 'ds_digit.TTF')
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 150)
        self.time_label.setFont(my_font)

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def button_style(self):
        return '''
            QPushButton {
                font-size: 18px;
                background-color: #4CAF50;
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
    '''

    def update_time(self):
        if not self.is_paused:
            if self.custom_time:
                self.custom_time = self.custom_time.addSecs(1)

                if self.is_24hr_mode:
                    time_string = self.custom_time.toString('HH:mm:ss')
                else:
                    time_string = self.custom_time.toString('hh:mm:ss AP')
            else:
                current_time = QTime.currentTime()
                if self.is_24hr_mode:
                    time_string = current_time.toString('HH:mm:ss')
                else:
                    time_string = current_time.toString('hh:mm:ss AP')

        self.time_label.setText(time_string)

        check_time = self.custom_time if self.custom_time else QTime.currentTime()
        if self.alarm_time:
            if self.is_24hr_mode:
                formatted_current_time = check_time.toString('HH:mm:ss')
                formatted_alarm_time = self.alarm_time.toString('HH:mm:ss')
            else:
                formatted_current_time = check_time.toString('hh:mm:ss AP')
                formatted_alarm_time = self.alarm_time.toString('hh:mm:ss AP')

            if formatted_current_time == formatted_alarm_time:
                self.show_alarm_message()

    def set_time(self, time_tuple):
        hours, minutes, seconds = time_tuple
        self.timer.stop()
        self.custom_time = QTime(hours, minutes, seconds)
        self.alarm_time = None
        self.time_label.setText(self.custom_time.toString('hh:mm:ss AP'))
        self.timer.start(1000)

    def set_alarm(self, alarm_tuple):
        hours, minutes, seconds = alarm_tuple
        self.alarm_time = QTime(hours, minutes, seconds)

    def show_alarm_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Alarm ringing')
        msg.setWindowTitle('Alarm!')
        msg.exec_()

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.timer.start(1000)
        else:
            self.is_paused = True
            self.timer.stop()

    def change_time_mode(self):
        self.is_24hr_mode = not self.is_24hr_mode
        self.update_time()

    def set_time_dialog(self):
        text, ok = QInputDialog.getText(self, 'Set Time', 'Enter time: (hh:mm:ss):')
        if ok and text:
            try:
                hours, minutes, seconds = map(int, text.split(':'))
                self.set_time((hours, minutes, seconds))
            except ValueError:
                self.show_error_message('Invalid time format! Please use hh:mm:ss.')

    def set_alarm_dialog(self):
        text, ok = QInputDialog.getText(self, 'Set Alarm Time', 'Enter time: (hh:mm:ss):')
        if ok and text:
            try:
                hours, minutes, seconds = map(int, text.split(':'))
                self.set_alarm((hours, minutes, seconds))
            except ValueError:
                self.show_error_message('Invalid alarm format! Please use hh:mm:ss.')

    def set_time_zone_dialog(self):
        # Create ComboBox for time zone selection
        time_zone_dialog = QComboBox(self)
        time_zone_dialog.addItems(['Europe', 'UTC', 'America', 'Asia'])
        time_zone_dialog.setCurrentText(self.time_zone)  # Set current selected time zone as the default option

        # Create a separate window for time zone selection
        dialog = QDialog(self)
        dialog.setWindowTitle('Select Time Zone')
        dialog.setGeometry(600, 400, 300, 150)

        layout = QVBoxLayout(dialog)
        layout.addWidget(time_zone_dialog)

        # Add the 'Set' button to confirm the selection
        set_button = QPushButton('Set', dialog)
        set_button.setStyleSheet("""
            background-color: blue; 
            color: white; 
            width: 30px;
            font-size: 12px; 
            border-radius: 15px; 
            padding: 10px 10px;
        """)

        def set_time_zone():
            selected_timezone = time_zone_dialog.currentText()
            self.time_zone = selected_timezone  # Update the current time zone
            self.time_label.setText(f"{selected_timezone}")  # Show new time zone on screen for 10 seconds

            # Timer to revert the display time zone back after 10 seconds
            QTimer.singleShot(10000, lambda: self.time_label.setText(''))

            dialog.accept()  # Close the dialog after setting the time zone

        set_button.clicked.connect(set_time_zone)
        layout.addWidget(set_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_alarm_sound_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Select Alarm Sound')

        layout = RadioButtonLayout()
        sounds = ['Ring', 'Beep', 'Melody', 'Chime']
        for sound in sounds:
            radio_button = QRadioButton(sound, dialog)
            radio_button.toggled.connect(lambda checked, sound=sound: self.set_alarm_sound(sound) if checked else None)
            layout.addWidget(radio_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_alarm_sound(self, sound):
        self.alarm_sound = sound

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle('Error')
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MommysClock()
    window.show()
    sys.exit(app.exec_())







