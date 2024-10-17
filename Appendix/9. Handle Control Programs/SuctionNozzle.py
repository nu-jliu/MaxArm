import time
import _thread as thread
from machine import Pin, PWM
from PWMServo import PWMServo

pump_io = [21,19] # M1接口
valve_io = [18,5] # M2接口


class SuctionNozzle:
  
  def __init__(self, pump_io=pump_io, valve_io=valve_io, hz=1000):
    self.pump_f = PWM(Pin(pump_io[0]))
    self.pump_b = PWM(Pin(pump_io[1]))
    self.valve_f = PWM(Pin(valve_io[0]))
    self.valve_b = PWM(Pin(valve_io[1]))
    self.pump_f.freq(hz)
    self.pump_b.freq(hz)
    self.valve_f.freq(hz)
    self.valve_b.freq(hz)
    self.hz = hz
    self.pwm_servo = PWMServo()
    self.pwm_servo.work_with_time()
    self.nozzle_st = False
    
  def on(self): # 开启气泵，关闭电磁阀
    if not self.nozzle_st:
      self.pump_f.duty(self.hz)
      self.pump_b.duty(0)
      self.valve_f.duty(0)
      self.valve_b.duty(0)
      self.nozzle_st = True
  
  def _off(self): # 打开电磁阀，关闭气泵
    if self.nozzle_st:
      self.valve_f.duty(self.hz)
      self.valve_b.duty(0)
      self.pump_f.duty(0)
      self.pump_b.duty(0) 
      time.sleep_ms(1000)
      self.valve_f.duty(0)
      self.valve_b.duty(0)
      self.nozzle_st = False
  
  def off(self):
    thread.start_new_thread(self._off, ())#启动线程
  
  def set_angle(self, angle=0, duration=1000):
    pulse = map(angle, -90, 90, 500, 2500)
    pulse = 500 if pulse < 500 else pulse
    pulse = 2500 if pulse > 2500 else pulse
    self.pwm_servo.run(1, pulse, duration)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  
  








