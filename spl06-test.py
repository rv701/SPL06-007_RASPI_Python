#!/usr/bin/env python

import time
import smbus
import numpy as np
i2c_ch = 1

# SPL06-007 I2C address
i2c_address = 0x76

def get_c0():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x10)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x11)

  tmp_LSB = tmp_LSB >> 4;
  tmp = tmp_MSB << 4 | tmp_LSB

  if (tmp & (1 << 11)):
    tmp = tmp | 0xF000

  return np.int16(tmp)

def get_c1():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x11)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x12)

  tmp_LSB = bus.read_byte_data(i2c_address, 0xF)
  tmp = tmp_MSB << 8 | tmp_LSB

  if (tmp & (1 << 11)):
    tmp = tmp | 0xF000

  return np.int16(tmp)

def get_c00():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x13)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x14)
  tmp_XLSB = bus.read_byte_data(i2c_address, 0x15)

  tmp = np.uint32(tmp_MSB << 12) | np.uint32(tmp_LSB << 4) | np.uint32(tmp_XLSB >> 4)

  if(tmp & (1 << 19)):
    tmp = tmp | 0XFFF00000
  
  return np.int32(tmp)

def get_c10():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x15)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x16)
  tmp_XLSB = bus.read_byte_data(i2c_address, 0x17)

  tmp_MSB = tmp_MSB & 0xF

  #tmp = tmp_MSB << 8 | tmp_LSB
  #tmp = tmp << 8
  tmp = np.uint32(tmp_MSB << 16) | np.uint32(tmp_LSB << 8) | np.uint32(tmp_XLSB)

  if(tmp & (1 << 19)):
    tmp = tmp | 0XFFF00000

  return np.int32(tmp)

def get_c01():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x18)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x19)

  tmp = (tmp_MSB << 8) | tmp_LSB

  return np.int16(tmp)

def get_c11():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x1A)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x1B)

  tmp = (tmp_MSB << 8) | tmp_LSB

  return np.int16(tmp)

def get_c20():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x1C)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x1D)

  tmp = (tmp_MSB << 8) | tmp_LSB

  return np.int16(tmp)

def get_c21():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x1E)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x1F)

  tmp = (tmp_MSB << 8) | tmp_LSB

  return np.int16(tmp)

def get_c30():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x20)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x21)

  tmp = (tmp_MSB << 8) | tmp_LSB

  return np.int16(tmp)

def get_traw():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x03)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x04)
  tmp_XLSB = bus.read_byte_data(i2c_address, 0x05)

  tmp = np.uint32(tmp_MSB << 16) | np.uint32(tmp_LSB << 8) | np.uint32(tmp_XLSB)

  if(tmp & (1 << 23)):
    tmp = tmp | 0XFF000000

  return np.int32(tmp)

def get_temperature_scale_factor():
  tmp_Byte = bus.read_byte_data(i2c_address, 0x07)

  tmp_Byte = (tmp_Byte >> 4) & 0B111

  if(tmp_Byte == 0B000):
    k = 524288.0

  if(tmp_Byte == 0B001):
    k = 1572864.0

  if(tmp_Byte == 0B010):
    k = 3670016.0

  if(tmp_Byte == 0B011):
    k = 7864320.0

  if(tmp_Byte == 0B100):
    k = 253952.0

  if(tmp_Byte == 0B101):
    k = 516096.0

  if(tmp_Byte == 0B110):
    k = 1040384.0

  if(tmp_Byte == 0B111):
    k = 2088960.0 

  return k

def get_praw():
  tmp_MSB = bus.read_byte_data(i2c_address, 0x00)
  tmp_LSB = bus.read_byte_data(i2c_address, 0x01)
  tmp_XLSB = bus.read_byte_data(i2c_address, 0x02)

  tmp = np.uint32(tmp_MSB << 16) | np.uint32(tmp_LSB << 8) | np.uint32(tmp_XLSB)

  if(tmp & (1 << 23)):
    tmp = tmp | 0XFF000000

  return np.int32(tmp)


def get_pressure_scale_factor():
  tmp_Byte = bus.read_byte_data(i2c_address, 0x06)

  tmp_Byte = tmp_Byte & 0B111

  if(tmp_Byte == 0B000):
    k = 524288.0

  if(tmp_Byte == 0B001):
    k = 1572864.0

  if(tmp_Byte == 0B010):
    k = 3670016.0

  if(tmp_Byte == 0B011):
    k = 7864320.0

  if(tmp_Byte == 0B100):
    k = 253952.0

  if(tmp_Byte == 0B101):
    k = 516096.0

  if(tmp_Byte == 0B110):
    k = 1040384.0

  if(tmp_Byte == 0B111):
    k = 2088960.0

  return k

def get_altitude(pressure, pressure_sealevel):
  pressure /= 100
  altitude = 44330 * (1.0 - pow((pressure / pressure_sealevel), 0.1903))
  return altitude
  


# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Set pressure configuration register
bus.write_byte_data(i2c_address, 0x06, 0x03)

# Set temperature configuration register
bus.write_byte_data(i2c_address, 0x07, 0x80)

# Set measurement register
bus.write_byte_data(i2c_address, 0x08, 0x07)

# Set configuration register
bus.write_byte_data(i2c_address, 0x09, 0x00)



# Read SPL06-007 Device ID
id = bus.read_byte_data(i2c_address, 0x0D)
print "ID:", id

# Read pressure configuration register
var = bus.read_byte_data(i2c_address, 0x06)
print "PRG_CFG:", bin(var)

var = bus.read_byte_data(i2c_address, 0x07)
print "TMP_CFG:", bin(var)

var = bus.read_byte_data(i2c_address, 0x08)
print "MEAS_CFG:", bin(var)

var = bus.read_byte_data(i2c_address, 0x09)
print "CFG_REG:", bin(var)

var = bus.read_byte_data(i2c_address, 0x0A)
print "INT_STS:", bin(var)

var = bus.read_byte_data(i2c_address, 0x0B)
print "FIFO_STS:", bin(var)

c0 = get_c0()
print "c0:", c0

c1 = get_c1()
print "c1:", c1

c00 = get_c00()
print "c00:", c00

c10 = get_c10()
print "c10:", c10

c01 = get_c01()
print "c01:", c01

c11 = get_c11()
print "c11:", c11

c20 = get_c20()
print "c20:", c20

c21 = get_c21()
print "c21:", c21

c30 = get_c30()
print "c30:", c30

traw = get_traw()
print "traw:", traw

t_scale = get_temperature_scale_factor()
print "t_scale:", t_scale

traw_sc = traw / t_scale
print "traw_sc:", "{:.3f}".format(traw_sc)

temp_c = ((c0) * 0.5) + ((c1) * traw_sc)
temp_f = (temp_c * 9/5) + 32

print "temp_c:", "{:.1f}".format(temp_c), "C"
print "temp_f:", "{:.1f}".format(temp_f), "F"

praw = get_praw()
print "praw:", praw

p_scale = get_pressure_scale_factor()
print "p_scale:", p_scale

praw_sc = praw / p_scale
print "p_scale", "{:.3f}".format(praw_sc)

pcomp = c00+ praw_sc*(c10+ praw_sc*(c20+ praw_sc*c30)) + traw_sc*c01 + traw_sc*praw_sc*(c11+praw_sc*c21)
print "pcomp", "{:.2f}".format(pcomp)

altitude = get_altitude(pcomp, 1009.7)
print "altitude:",  "{:.1f}".format(altitude), "m"

altitude_f = altitude * 3.281
print "altitude",  "{:.1f}".format(altitude_f), "ft"

