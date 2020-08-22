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

print "c0:", get_c0()

print "c1:", get_c1()
