import time
import math
import __espmax
from BusServo import BusServo

L0 = 84.0
L1 = 8.2
L2 = 128.0
L3 = 138.0
L4 = 16.8


class ESPMax:
    ORIGIN = 0, -(L1 + L3 + L4), L0 + L2

    def __init__(self, bus_servo=BusServo(), origin=ORIGIN):
      self.bus_servo = bus_servo
      self.origin = origin
      self.position = self.origin
      self.joints = 120, 90, 0
      self.servos = 500, 500, 500  # [servo id 1, servo id 2, servo id 3]
      self.last_position = self.position
      self.distance = 0
      self.duration = 0
      self.L4 = L4

    def set_servo_in_range(self, servo_id, p, duration):
        if servo_id == 3 and p < 470:
            p = 470
        if servo_id == 2 and p > 700:
            p = 700
            
        self.bus_servo.run(servo_id, int(p), duration)
        return True
    
    def position_to_pulses(self, position):
        angles = __espmax.inverse(self.L4, position)
        pulses = __espmax.deg_to_pulse(angles)
        return pulses
  
    def pulses_to_position(self, pulses):
        joints = __espmax.pulse_to_deg(pulses)
        x,y,z = __espmax.forward(self.L4, joints)
        return -int(x+0.5),int(y+0.5),int(z+0.5)
  
    def set_position(self, position, duration):
        duration = int(duration)
        x, y, z = position
        try:
          if z > 225:
              z = 225
          if math.sqrt(x ** 2 + y ** 2) < 50:
              return None
          angles = __espmax.inverse(self.L4, (-x, y, z))
          pulses = __espmax.deg_to_pulse(angles)
          for i in range(3):
                  ret = self.set_servo_in_range(i + 1, pulses[i], duration)
                  if not ret:
                      raise ValueError("{} Out of limit range".format(pulses[i]))
          self.servos = pulses
          self.joints = angles
          self.position = x, y, z
          return True
        except:
          return False
    
    def set_position_with_speed(self, position, speed):
            old_position = self.position
            distance = math.sqrt(sum([(position[i] - old_position[i]) ** 2 for i in range(0, 3)]))
            duration = distance / max(speed, 0.001)
            self.distance = distance
            self.last_position = self.position
            self.duration = duration
            self.set_position(position, duration)
    
    def set_position_relatively(self, values, duration):
            x, y, z = self.position
            x_v, y_v, z_v = values
            x += x_v
            y += y_v
            z += z_v
            return self.set_position((x, y, z), duration)
    
    def set_servo(self, servo_id, pulse, duration):
        if not 0 < servo_id < 4:
            raise ValueError("Invalid servo id:{}".format(servo_id))
        pulse = 0 if pulse < 0 else pulse
        pulse = 1000 if pulse > 1000 else pulse
        servos = list(self.servos)
        servos[servo_id - 1] = pulse
        joints = __espmax.pulse_to_deg(servos)
        new_position = __espmax.forward(self.L4, joints)
        self.set_position(new_position, duration)

    def set_servo_with_speed(self, servo_id, pulse, speed):
        if not 0 < servo_id < 4:
            raise ValueError("Invalid servo id:{}".format(servo_id))
        pulse = 0 if pulse < 0 else pulse
        pulse = 1000 if pulse > 1000 else pulse
        servos = list(self.servos)
        servos[servo_id - 1] = pulse
        joints = __espmax.pulse_to_deg(servos)
        new_position = __espmax.forward(self.L4, joints)
        self.set_position_with_speed(new_position, speed)

    def set_servo_relatively(self, servo_id, value, duration):
        if not 0 < servo_id < 4:
            raise ValueError("Invalid servo id:{}".format(servo_id))
        index = servo_id - 1
        pulse = self.servos[index]
        pulse += value
        return self.set_servo(servo_id, pulse, duration)

    def set_joint(self, joint_id, angle, duration):
        if not 0 < joint_id < 4:
            raise ValueError("Invalid joint id:{}".format(joint_id))
        angles = list(self.joints)
        angles[joint_id - 1] = angle
        servos = __espmax.deg_to_pulse(angles)
        return self.set_servo(joint_id, servos[joint_id - 1], duration)

    def set_joint_relatively(self, joint_id, value, duration):
        if not 0 < joint_id < 4:
            raise ValueError("Invalid joint id:{}".format(joint_id))
        angles = list(self.joints)
        angles[joint_id - 1] += value
        servos = __espmax.deg_to_pulse(angles)
        return self.set_servo(joint_id, servos[joint_id - 1], duration)

    def go_home(self, duration=2000):
        self.set_position(self.origin, duration)
  
    def teaching_mode(self):
      for i in range(3):
        self.bus_servo.unload(i+1)
  
    def read_position(self):
      pulses_list = []
      for i in range(3):
        pulses = self.bus_servo.get_position(i+1)
        if pulses:
          pulses_list.append(pulses)
        else:
          n = 0
          for s in range(3):
            pulses = self.bus_servo.get_position(i+1)
            if pulses:
              pulses_list.append(pulses)
              break
            else:
              n += 1
              if n == 3:
                return False
            time.sleep_ms(5)
        time.sleep_ms(5)
      x,y,z = ESPMax.pulses_to_position(self,pulses_list)
      return x,y,z
    
    def read_angles(self):
      pulses_list = []
      for i in range(3):
        pulses = self.bus_servo.get_position(i+1)
        if pulses:
          pulses_list.append(pulses)
        else:
          n = 0
          for s in range(3):
            pulses = self.bus_servo.get_position(i+1)
            if pulses:
              pulses_list.append(pulses)
              break
            else:
              n += 1
              if n == 3:
                return False
            time.sleep_ms(5)
        time.sleep_ms(5)
      return pulses_list
      
    def verify_position(self, x,y,z):
      try:
        angles = __espmax.inverse(self.L4, (x,y,z))
        pulses = __espmax.deg_to_pulse(angles)
        return True
      except:
        return False

















