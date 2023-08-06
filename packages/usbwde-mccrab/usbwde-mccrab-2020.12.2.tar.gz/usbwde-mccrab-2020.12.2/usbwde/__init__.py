"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import collections
import logging
import serial
import threading
from typing import Tuple


class WdeReadError(Exception):
  pass


Sensor = collections.namedtuple('Sensor', ['temperature', 'humidity'])


class __G(object):
    lock = threading.Lock()
    wde  = None


def _parse_temperature(value : str) -> float:
  if not value:
    return None
  # temperatures follow the "de" locale, but as a module, the current setting can be neither relied upon nor changed.
  parts = value.split(',')
  try:
    if len(parts) == 1:
      return float(parts[0])
    elif len(parts) == 2:
      return float(parts[0]) + float(parts[1]) / pow(10, len(parts[1]))
    else:
      raise WdeReadError('Unable to parse temperature string "{}"'.format(value))
  except ValueError:
    raise WdeReadError('Unable to parse temperature string "{}"'.format(value))


def _parse_humidity(value : str) -> int:
  if not value:
    return None
  try:
    return int(value)
  except ValueError:
    raise WdeReadError('Unable to parse humidity string "{}"'.format(value))


class DataSet(object):

  def __init__(self, line : str):
    """Parse one line returned from the WDE1 into the data it represents.

    Args:
      line: string read from the device. Expected to look something like:
          "$1;1;;21,9;21,5;21,5;;;;;;46;48;50;;;;;;;;;;;0"

    Raises:
      WdeReadError if there was any trouble parsing the line.
    """
    fields = line.split(';')
    if len(fields) != 25:
      raise WdeReadError('Expected 25 fields, got {}'.format(len(fields)))
    if fields[0] != '$1' or fields[24] != '0':
      raise WdeReadError('Expected "$1" and "0" SOR/EOR fields, got "{}" and "{}"'.format(fields[0], fields[-1]))
    temps = [_parse_temperature(t) for t in fields[3:11] + [fields[19]]]
    humidity = [_parse_humidity(h) for h in fields[11:19] + [fields[20]]]

    self.sensors = zip(temps, humidity)

    # these are currently ignored:
    unused_windspeed = fields[21]
    unused_rainfall = fields[22]
    unused_is_raining = fields[23]

  @property
  def sensors(self) -> Tuple[Sensor, ...]:
    return self._sensors

  @sensors.setter
  def sensors(self, values):
    new_sensors = [Sensor(t, h) for t,h in values]
    self._sensors = tuple(new_sensors)

  def __str__(self):
    return str(self._sensors)


class UsbWde(object):

  def __init__(self, device='/dev/ttyUSB0', speed=9600, initialize=True):
    self._wde = serial.Serial(port=device, baudrate=speed)
    self._thread = None
    self._lock = threading.Lock()
    self._callback = None
    self._latest = None
    if initialize:
      self._wde.write(B'M2')
      line = self._wde.readline().decode('ascii').strip('\r\n')
      line = self._wde.readline().decode('ascii').strip('\r\n')
      logging.debug('Initialized WDE: {}'.format(line))

  def latest(self):
    return self._latest

  def sync(self):
    while True:
      line = self._wde.readline()
      line = line.decode('ascii').strip('\r\n')
      logging.debug('Read line: "{}"'.format(line))
      try:
        dataset = DataSet(line)
        self._latest = dataset
        logging.debug('Read dataset: {}'.format(dataset))
        yield dataset
      except WdeReadError:
        logging.warn('Error reading from WDE, got: [{}]'.format(line))

  def async(self, callback : callable):
    if self._thread is not None:
      with self._lock:
        self._callback = None
      self._thread.join()
      self._thread = None
    if callback is nont None:
      self._thread = threading.Thread(target=self._background, name='USB-WDE-Background-Thread')
      self._callback = callback
      self._thread.start()

  def _background(self):
    wde = UsbWde()
    for dataset in wde.sync():
      with self._lock:
        if self._callback is not None:
          self._callback(dataset)
        else:
          return

  def run_in_background(self):
    self.async(lambda: None)


def _debug():
  import datetime
  import time
  logging.basicConfig(level=logging.DEBUG)
  wde = UsbWde()
  for d in wde.sync():
    print('{}: {}'.format(datetime.datetime.fromtimestamp(time.time()), d))
    # does not return.


def WDE(device='/dev/ttyUSB0', speed=9600, initialize=True):
    with __G.lock:
        if __G.wde is None:
            __G.wde = UsbWde(device, speed, initialize)
            __G.wde.run_in_background()
    return __G.wde

