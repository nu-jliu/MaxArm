import time
import _thread as thread
from machine import Pin, PWM

class Buzzer:
  
  def __init__(self, io=27, freq=2500):
    self.buzzer = PWM(Pin(io), freq=freq, duty=0)
    
  def on(self):
    self.buzzer.duty(300)
  
  def off(self):
    self.buzzer.duty(0)
    
  def set_Buzzer(self,s):
    self.buzzer.duty(300)
    time.sleep_ms(s)
    self.buzzer.duty(0)
    
  def setBuzzer(self,s):
    thread.start_new_thread(self.set_Buzzer, (s,))#启动线程
  

  










