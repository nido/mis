#!/usr/bin/python
"""Original Author: Elmer#eth0@eth0"""
import threading

class TransactionIdGenerator(object):
  """A simple, threadsafe, monotonic incrementer"""
  def __init__(self):
    self.counter = 0
    self.lock = threading.Lock()
  
  def GetTransactionId(self):
    with self.lock:
      self.counter += 1
      return self.counter
