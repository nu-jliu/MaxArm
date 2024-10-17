from machine import Pin, PWM
import time



class LED:
  
  def __init__(self, io=26, hz=1000):
    self.led = PWM(Pin(io))
    self.led.freq(hz)
    self.hz = hz
  def on(self):
    self.led.duty(self.hz)
  
  def off(self):
    self.led.duty(0)
    
  def pwm(self,hz = 500):
    self.led.duty(hz)





