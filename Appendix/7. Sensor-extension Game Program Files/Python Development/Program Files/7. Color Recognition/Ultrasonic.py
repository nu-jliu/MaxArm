from micropython import const


RGB_WORK_SIMPLE_MODE        = const(0)
RGB_WORK_BREATHING_MODE     = const(1)
DISDENCE_L      = const(0)
DISDENCE_H      = const(1)
RGB_WORK_MODE   = const(2)#RGB灯模式，0：用户自定义模式   1：呼吸灯模式  默认0
RGB1_R       = const(3)#1号探头的R值，0~255，默认0
RGB1_G       = const(4)#默认0
RGB1_B       = const(5)#默认255
RGB2_R       = const(6)#2号探头的R值，0~255，默认0
RGB2_G       = const(7)#默认0
RGB2_B       = const(8)#默认255

RGB1_R_BREATHING_CYCLE       = const(9) #呼吸灯模式时，1号探头的R的呼吸周期，单位100ms 默认0，
                                        #如果设置周期3000ms，则此值为30
RGB1_G_BREATHING_CYCLE       = const(10)
RGB1_B_BREATHING_CYCLE       = const(11)

RGB2_R_BREATHING_CYCLE       = const(12)#2号探头
RGB2_G_BREATHING_CYCLE       = const(13)
RGB2_B_BREATHING_CYCLE       = const(14)



class ULTRASONIC:
  def __init__(self, i2c, address = 0x77):
    self.address = address
    self.bus = i2c

  def readByte(self, reg):
    return self.bus.readfrom_mem(self.address, reg, 1)[0]
    
  def writeByte(self, reg, val):
    self.bus.writeto_mem(self.address, reg, val.to_bytes(1,'little'))
  
  def writeByteArray(self, reg, array):
    self.bus.writeto_mem(self.address, reg, array)
    
  def getDistance(self):
    l = self.readByte(DISDENCE_L)
    h = self.readByte(DISDENCE_H)
    return (h<<8) + l
    
  def setRGBMode(self, mode):
    self.writeByte(RGB_WORK_MODE,mode)
  
  def setRGBValue(self, value):
    self.writeByteArray(RGB1_R, value)
    
  def setRGBBreathingValue(self, value):
    self.writeByteArray(RGB1_R_BREATHING_CYCLE, value)










