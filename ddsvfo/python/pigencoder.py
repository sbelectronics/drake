#!/usr/bin/env python

# based on pigpio2 rotary encoder example

import pigpio
import threading

class PigEncoder:
   def __init__(self, pi, gpioA, gpioB):
      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

      # We can easily fall behind if we callback every time a fast encoder changes
      # Instead, keep a running total of the delta, and the caller can poll us for
      # changes.
      self.lock = threading.Lock()
      self.delta = 0

   def _pulse(self, gpio, level, tick):

      """
      Decode the rotary encoder pulse.

                   +---------+         +---------+      0
                   |         |         |         |
         A         |         |         |         |
                   |         |         |         |
         +---------+         +---------+         +----- 1

             +---------+         +---------+            0
             |         |         |         |
         B   |         |         |         |
             |         |         |         |
         ----+         +---------+         +---------+  1
      """

      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level;

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               with self.lock:
                   self.delta += 1
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               with self.lock:
                   self.delta -= 1

   def getAndResetDelta(self):
      with self.lock:
          delta = self.delta
          self.delta = 0
      return delta

   def cancel(self):
      self.cbA.cancel()
      self.cbB.cancel()
