import time
import ujson
import _thread as thread
from espmax import ESPMax
from PWMServo import PWMServo
from BusServo import BusServo
from SuctionNozzle import SuctionNozzle


runAction_ = True

class RobotControl:
  
  def __init__(self):
    self.pwm = PWMServo()
    self.bus_servo = BusServo()
    self.arm = ESPMax(self.bus_servo)
    self.nozzle = SuctionNozzle()
  
  
  def read_json_file(self, act_name):
    with open(act_name+'.rob','r') as load_f:
      fp = ujson.load(load_f)
      da = fp['Actions']
      return da
  
  
  def runAction(self, act_name, times):
    da = self.read_json_file(act_name)
    for s in range(times):
      num = 0
      for i in da:
        if not runAction_:
          break
        print('$$>'+str(num)+'<$$')
        times = i['Duration']
        pos = i['Values']
        nozzle_suck = pos['suck']
        nozzle_angle = pos['nozzle']
        x, y, z = pos['x'], pos['y'], pos['z']
        self.arm.set_position((x,y,z),times)
        self.nozzle.set_angle(nozzle_angle,times)
        if nozzle_suck:
          self.nozzle.on()
        else:
          self.nozzle.off()
        num += 1
        time.sleep_ms(times)
    print('$$>end<$$')    
    return True
  
  
  def runActionGroup(self, act_name, times = 1):
    global runAction_
    if not runAction_:
      runAction_ = True
    thread.start_new_thread(self.runAction, (act_name, times))#启动线程
  
  
  def stopActionGroup(self):
    global runAction_
    runAction_ = False
  





















