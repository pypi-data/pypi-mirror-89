import pygatt
import time
import csv
import matplotlib.pyplot as plt
from binascii import hexlify
import pywinusb.hid as hid
from xlwt import Workbook 
import asyncio
from bleak import discover
import logging
from bleak import BleakClient
from bleak import _logger as logger
import threading
from threading import Thread

from MUL1 import *
from MUL2 import *
from MUL3 import *
from MUL4 import *
from MUL5 import *
from MUL6 import *
from MUL7 import *
from MUL8 import *
from MUL9 import *
from MUL10 import *
from MUL11 import *

CHAR_UUID = "0000fff7-0000-1000-8000-00805f9b34fb"
CHAR_WRITE_UUID = "0000fff6-0000-1000-8000-00805f9b34fb"
DATA_UUID = "00001601-0000-1000-8000-00805f9b34fb"


class Rabboni:
    def __init__(self,mode=None,dongle = "Bluegiga"):
        self.dongle = dongle
        self.device = None
        self.mode = mode
        self.address = ""
        # self.client = None
        self.dataLoop = 0
        if self.mode=="BLE":
            print("------Using " ,dongle , " BLE ------")
            
            if (self.dongle == "Bluegiga"):
                self.adapter = pygatt.BGAPIBackend()
                self.adapter.start()
        elif self.mode =="USB":
            print("------Using USB------")
            pass
        else :
            raise ValueError("Mode must be USB or BLE")
        self.vid = 0x04d9
        self.pid = 0xb564
        self.usb_temp = []
        self.characteristics = []
        self.Status = 0
        self.Sensor_char = 0
        self.Sensor_char_2 = 0
        self.Acc_char = 0
        self.Gyr_char = 0

        self.Hex_data   = 0
        self.Accx = 0
        self.Accy = 0
        self.Accz = 0
        self.Gyrx = 0
        self.Gyry = 0
        self.Gyrz = 0
        self.Cur_Cnt   = 0
        self.Store_Cnt   = 0

        self.data_num = 0
        self.time_list = ["Time"]
        self.Accx_list = ["AccX"]
        self.Accy_list = ["AccY"]
        self.Accz_list = ["AccZ"]
        self.Gyrx_list = ["GyrX"]
        self.Gyry_list = ["GyrY"]
        self.Gyrz_list = ["GyrZ"]
        self.Cnt_list = []
        self.report = 0
        self.print = False
        self.reset = False
        self.resetMode = "Both"
        self.restTime = 0
        self.maxRunTime = 5


        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        self.q4 = 0
        self.q1_list = []
        self.q2_list = []
        self.q3_list = []
        self.q4_list = []
        self.q_last = [1,0,0,0]
        self.qClass = None

        self.sampling_rate = 0


    def stop(self):
        if self.mode == "BLE":
            self.Status = 0

            if (self.dongle != "Bluegiga"):
                self.dataLoop.stop()
            else :
                self.adapter.stop()

        elif self.mode == "USB":
            self.Status = 0
            close_cmd = [0x00 for i in range(33)]
            close_cmd[1] = 0x02 # Report ID
            close_cmd[2] = 0x33
            close_cmd[3] = 0x0a
            self.report[0].set_raw_data(close_cmd)
            self.report[0].send()
            if self.device:
                self.device.close()

    # async def scan_async(self, timeout=5):
    #     if self.mode == "BLE":
    #         self.devices = await discover(10.0)
    #         # for dev in (self.devices):
    #         #     print ("Name : %s  MAC : %s"  %(dev["name"], dev["address"]))
    #         return self.devices

    def scan(self, timeout=5):
        if self.mode == "BLE":
            if (self.dongle == "Bluegiga"):
                self.devices = self.adapter.scan(timeout)
                # for dev in (self.devices):
                #     print ("Name : %s  MAC : %s"  %(dev["name"], dev["address"]))
                return self.devices

    def print_device(self):
        if (self.dongle != "Bluegiga"):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.print_device_async())
        else :        
            # self.devices = self.adapter.scan(timeout)
            for dev in (self.devices):
                print ("Name : %s  MAC : %s"  %(dev["name"], dev["address"]))
            

    async def print_device_async(self,timeout = 10.0):
        if self.mode == "BLE":
            devices = await discover(timeout)
            print ("------Scan BLE Device Start------")
            for d in devices:
                print(d)
            print ("------Scan BLE Device Done------")


    def connect_name(self, name, devices=None):
        if self.mode == "BLE":
            if devices is None:
                devices = self.devices
            for dev in self.devices:
                if name == dev['name']:
                    return self.connect(dev['address'])
            return None

    def connect(self, address = None):
        if self.mode == "BLE":
            if (address in MUL1 or address in MUL2 or address in MUL3 or address in MUL4 or address in MUL5 or address in MUL6 or address in MUL7 or address in MUL8 or address in MUL9 or address in MUL10 or address in MUL11 ):
                print("--- Connecting...")
                if (self.dongle != "Bluegiga"):
                    self.address = address
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.connect_async(loop))

                    
                else :
                    self.device = self.adapter.connect(address,address_type=pygatt.BLEAddressType.random)
                    self.Status = 1
                    self.discover_characteristics()
                    self.read_sensor_char()

                    self.print_char()
     
                # return self.device
            else :
                raise ValueError("Device is not the Rabboni.")
        elif self.mode == "USB":
            _filter = hid.HidDeviceFilter(vendor_id = self.vid, product_id = self.pid)
            hid_device = _filter.get_devices()
            self.Status = 1
            if len(hid_device) > 0:
                self.device = hid_device[0]
                self.device.open()
                self.report = self.device.find_output_reports()
                self.fea_report = self.device.find_feature_reports()
            else : 
                raise ValueError("Nodevice vendor_id : %s , product_id : %s" %(hex(self.vid),hex(self.pid)))
            cmd = [0x00 for i in range(33)]
            cmd[1] = 0x02
            cmd[3] = 0x0a
            send_30 = cmd.copy()
            send_30[2] = 0x30
            # print (self.fea_report)
            ### Report request(set feature)
            szBuf = [0,0,0,0,0,0,0,0,0]
            baudrate = 115200
            szBuf[1] = 0x01
            szBuf[2] = (baudrate & 0x00ff)
            szBuf[3] = (0xC2)
            szBuf[4] = (baudrate >> 16)
            szBuf[5] = (baudrate >> 24)
            szBuf[6] = 0
            szBuf[7] = 0
            szBuf[8] = 0x08
            ### Report request(set feature)
            if self.device:
                if self.fea_report:
                    self.fea_report[0].set_raw_data(szBuf)
                    bytes_num = self.fea_report[0].send()
                if self.report:
                    self.report[0].set_raw_data(send_30)
                    bytes_num = self.report[0].send()
                    time.sleep(0.5)


            self.read_sensor_char()



    def start_loop(self,loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def connect_async(self,loop):
        # async with BleakClient(self.address, timeout=5.0) as client:
            # x = await asyncio.wait_for(client.is_connected(), timeout=5)
            # print(ssss)
            self.device = BleakClient(self.address, loop=loop)
            await self.device.connect(timeout=5.0)
            x = await self.device.is_connected()


            await self.device.start_notify(CHAR_UUID, self.read_char_callback_ble)
            await self.device.write_gatt_char(CHAR_WRITE_UUID, bytearray([0x49]), response=True)
            await asyncio.sleep(1.0)
            print("Connect : " , x)

            # await self.device.start_notify(CHAR_UUID, self.read_char_callback_ble)
            # await self.device.write_gatt_char(CHAR_WRITE_UUID, bytearray([0x49]), response=True)
            # await asyncio.sleep(1.0)
            # await self.device.stop_notify(CHAR_UUID)


            # await self.device.start_notify(DATA_UUID, self.read_callback_BLE)
            
            # await asyncio.sleep(self.maxRunTime)
            
            # await self.device.stop_notify(DATA_UUID)

    async def data_async(self):

            
            # await self.device.stop_notify(CHAR_UUID)
            await self.device.start_notify(DATA_UUID, self.read_callback_BLE)
            self.Status = 1
            await asyncio.sleep(self.maxRunTime)
            
            # await self.device.stop_notify(DATA_UUID)






    def disconnect(self):
        if self.mode == "BLE":
            self.Status = 0
            if (self.dongle != "Bluegiga"):
                self.device.disconnect()
            # self.device.disconnect()
        elif self.mode == "USB":
            self.Status = 0
            close_cmd = [0x00 for i in range(33)]
            close_cmd[1] = 0x02 # Report ID
            close_cmd[2] = 0x33
            close_cmd[3] = 0x0a
            self.report[0].set_raw_data(close_cmd)
            self.report[0].send()
            if self.device:
                self.device.close()

    def discover_characteristics(self, device=None):
        if self.mode == "BLE":
            if device is None:
                device = self.device
            for uuid in device.discover_characteristics().keys():
                try:
                    device.char_read(uuid)
                    self.characteristics.append(
                        {'uuid': uuid, 'handle': device.get_handle(uuid), 'readable': True})
                except Exception as e:
                    if "unable to read" in str(e).lower():
                        self.characteristics.append(
                            {'uuid': uuid, 'handle': device.get_handle(uuid), 'readable': False})
                    else:
                        raise e
            # return characteristics
    def print_char(self):
        if self.mode == "BLE":
            print ("====== device.discover_characteristics() =====")
            for ch_number in range(len(self.characteristics)):
                print("Read UUID %s (handle ): %d Readable: %s" 
                                    %(self.characteristics[ch_number]['uuid'], self.characteristics[ch_number]['handle'], self.characteristics[ch_number]['readable']))


    def read_data(self, device=None):
        if self.mode == "BLE":
            print("")
            ###非Bluegiga的在connet時就讀取資料
            if (self.dongle == "Bluegiga"):
                if device is None:
                    device = self.device               
                device.subscribe("00001601-0000-1000-8000-00805f9b34fb", self.read_callback_BLE)
            else :
                self.dataLoop = asyncio.new_event_loop()
                t = Thread(target=self.start_loop, args=(self.dataLoop,))
                t.start()
                asyncio.run_coroutine_threadsafe(self.data_async(), self.dataLoop)
        elif self.mode == "USB":
            cmd = [0x00 for i in range(33)]
            cmd[1] = 0x02
            cmd[3] = 0x0a
            send_32 = cmd.copy()
            send_32[2] = 0x32
            send_48 = cmd.copy()
            send_48[2] = 0x48
            send_30 = cmd.copy()
            send_30[2] = 0x30
            if self.device:
                if self.report:
                    
                    self.device.set_raw_data_handler(self.read_callback_USB)
                    self.report[0].set_raw_data(send_32)
                    bytes_num = self.report[0].send()

                    self.device.set_raw_data_handler(self.read_callback_USB)
                    self.report[0].set_raw_data(send_48)
                    bytes_num = self.report[0].send()

    def read_sensor_char(self, device=None):
        if self.mode == "BLE":
            if device is None:
                device = self.device
            if (self.dongle == "Bluegiga"):
                device.subscribe("0000fff7-0000-1000-8000-00805f9b34fb", self.read_char_callback_ble)###set scale
                device.char_write("0000fff6-0000-1000-8000-00805f9b34fb", bytearray([0x49]) ,wait_for_response=True)
        elif self.mode == "USB":
            # self.usb_temp = []
            if device is None:
                device = self.device
            cmd = [0x00 for i in range(33)]
            
            cmd[1] = 0x02
            cmd[2] = 0x49
            cmd[3] = 0x0a
            time.sleep(3)
            # print ("self.device",self.device)
            if self.device:
                if self.report:
                    self.device.set_raw_data_handler(self.read_callback_USB_char)
                    self.report[0].set_raw_data(cmd)
                    bytes_num = self.report[0].send()
                    time.sleep(3)
            ###set scale
            # print ("read char:",self.usb_temp)
            # print ("rate " ,self.usb_temp[9])
            if (len(self.usb_temp)!=1):
                acc_char = self.usb_temp[1]
                gyr_char = self.usb_temp[2]
                sampling_rate = self.usb_temp[9]
                # print ("len != 0",acc_char,gyr_char,sampling_rate)
            else :
                acc_char = 2
                gyr_char = 1000
                # print ("len = 0",acc_char,gyr_char,sampling_rate)
            
            if acc_char == '00':
                self.Acc_char = 2 # 2G
            elif acc_char == '01':
                self.Acc_char = 4 # 4G
            elif acc_char == '02':
                self.Acc_char = 8 # 8G
            elif acc_char == '03':
                self.Acc_char = 16 # 16G

            if gyr_char == '00':
                self.Gyr_char = 250 # 2G
            elif gyr_char == '01':
                self.Gyr_char = 500 # 4G
            elif gyr_char == '02':
                self.Gyr_char = 1000 # 8G
            elif gyr_char == '03':
                self.Gyr_char = 2000 # 16G
            self.usb_temp = []

            
            # if sampling_rate == b'00':
            #     self.sampling_rate = 10 # 10Hz
            # elif sampling_rate == b'01':
            #     self.sampling_rate = 20 # 10Hz
            # elif samsampling_rate == b'02':
            #     self.sampling_rate = 50 # 10Hz
            # elif sampling_rate == b'07':
            #     self.sampling_rate = 1 # 10Hz
            # elif sampling_rate == b'08':
            #     self.sampling_rate = 5 # 10Hz
            # elif sampling_rate == b'09':
            #     self.sampling_rate = 40 # 10Hz

            print ("Acc_char:",self.Acc_char,"Gyr_char:",self.Gyr_char)

    async def set_sensor_config_async(self,loop,data):
    # async with BleakClient(self.address, timeout=5.0) as client:
        # x = await asyncio.wait_for(client.is_connected(), timeout=5)
        # print(ssss)
        # print('bytedata ',bytearray(data))

        await self.device.start_notify(CHAR_UUID, self.read_char_callback_ble)
        await self.device.write_gatt_char(CHAR_WRITE_UUID, bytearray(data), response=True)
        await asyncio.sleep(2.0)
        await self.device.stop_notify(CHAR_UUID)

    def set_sensor_config(self,acc_scale = None,gyr_scale = None, rate = None,device = None,threshold = None):
        if (rate != 10 and rate != 20 and rate != 50 and rate != 100 and rate != 200 and rate != 500 and rate != 1000 and rate != 1 and rate != 5 and rate != 10 and rate != 40):
            raise ValueError ("Rate not in allowed range!")
        else:
            self.sampling_rate = rate
            
        if (acc_scale != 2 and acc_scale != 4 and acc_scale != 8 and acc_scale != 16):
            raise ValueError ("acc_scale must be 2 or 4 or 8 or 16!")
        else :
            self.Acc_char = acc_scale
        if (gyr_scale != 250 and gyr_scale != 500 and gyr_scale != 1000 and gyr_scale != 2000):
            raise ValueError ("gyr_scale must be 250 or 500 or 1000 or 2000!")
        else :
            self.Gyr_char = gyr_scale
        if (threshold == None or type(threshold) != int):
            raise ValueError ("threshold can not be None!")


        if self.mode == "BLE":
            if device is None:
                device = self.device
            # print(self.Sensor_char)
            a = bytearray(self.Sensor_char)
            # print ("AA",self.Sensor_char)

            t = str(self.Sensor_char)[2:-1]
            # print("t ", t)
            send_data = [0 for i in range(15)]
            # print (t)
            # print("send_data 1 ", send_data)
            for i in range(15):
                send_data[i] = int(t[i*2:2*i+2],16)
            # print("send_data 2 ", send_data)
            send_data[0] = int('45',16)
            if self.Acc_char == 2:
                send_data[1] = int('00',16)
            elif self.Acc_char == 4:
                send_data[1] = int('01',16)
            elif self.Acc_char == 8:
                send_data[1] = int('02',16)
            elif self.Acc_char == 16:
                send_data[1] = int('03',16)

            if self.Gyr_char == 250:
                send_data[2] =  int('00',16)
            elif self.Gyr_char == 500:
                send_data[2] = int('01',16)
            elif self.Gyr_char == 1000:
                send_data[2] = int('02',16)
            elif self.Gyr_char == 2000:
                send_data[2] = int('03',16)
            # print ("send,data" ,send_data)

            if rate == 10:
                send_data[9] =  int('00',16)
            elif rate == 20:
                send_data[9] = int('01',16)
            elif rate == 50:
                send_data[9] = int('02',16)
            elif rate == 100:
                send_data[9] = int('03',16)
            elif rate == 200:
                send_data[9] = int('04',16)
            elif rate == 500:
                send_data[9] = int('05',16)
            elif rate == 1000:
                send_data[9] = int('06',16)
            elif rate == 1:
                send_data[9] = int('10',16)
            elif rate == 5:
                send_data[9] = int('11',16)
            elif rate == 10:
                send_data[9] = int('12',16)
            elif rate == 40:
                send_data[9] = int('13',16)
            # print("send_data",send_data)

            send_data[10] = int('00',16)

            #############count threshold###########
            # send_data[13] = int('00',16)
            # send_data[14] = int('00',16)
            th_hex = hex (threshold)[2:]
            th_padded = '0' * (4 - len(th_hex)) + th_hex 
            send_data[12] = int("01",16)
            send_data[13] = int(th_padded[0:2],16)
            send_data[14] = int(th_padded[2:],16)

            # print("bytearray(send_data) " ,bytearray(send_data))
            # print (self.Sensor_char)
            # device.char_write(CHAR_WRITE_UUID , bytearray(send_data)) 
            if (self.dongle != "Bluegiga"):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.set_sensor_config_async(loop,send_data))
            else :
                device.char_write("0000fff6-0000-1000-8000-00805f9b34fb", bytearray(send_data)) 
                time.sleep(0.2)  
            # time.sleep(0.2)   
        elif self.mode == "USB":
            # self.read_data()
            
            set_cmd = [0x00 for i in range(33)]
            set_cmd[1] = 0x0e
            set_cmd[2] = 0x45
            set_cmd[3] = 0x01
            set_cmd[4] = 0x03
            set_cmd[5] = 0x00
            set_cmd[6] = 0x00
            set_cmd[7] = 0x01
            set_cmd[8] = 0x01
            set_cmd[9] = 0x00
            set_cmd[10] = 0x00
            set_cmd[11] = 0x00
            set_cmd[12] = 0x00
            set_cmd[13] = 0x00
            set_cmd[14] = 0x00
            set_cmd[15] = 0x00
            set_cmd[16] = 0x00
            set_cmd[17] = 0x0a

            if self.Acc_char == 2:
                set_cmd[3] = 0x00
            elif self.Acc_char == 4:
                set_cmd[3] = 0x01
            elif self.Acc_char == 8:
                set_cmd[3] = 0x02
            elif self.Acc_char == 16:
                set_cmd[3] = 0x03

            if self.Gyr_char == 250:
                set_cmd[4] = 0x00
            elif self.Gyr_char == 500:
                set_cmd[4] = 0x01
            elif self.Gyr_char == 1000:
                set_cmd[4] = 0x02
            elif self.Gyr_char == 2000:
                set_cmd[4] = 0x03

            if rate == 10:
                set_cmd[11] =  0x00
            elif rate == 20:
                set_cmd[11] = 0x01
            elif rate == 50:
                set_cmd[11] = 0x02
            elif rate == 100:
                set_cmd[11] = 0x03
            elif rate == 200:
                set_cmd[11] = 0x04
            elif rate == 500:
                set_cmd[11] = 0x05
            elif rate == 1000:
                set_cmd[11] = 0x06
            elif rate == 1:
                set_cmd[11] = 0x10
            elif rate == 5:
                set_cmd[11] = 0x11
            elif rate == 10:
                set_cmd[11] = 0x12
            elif rate == 40:
                set_cmd[11] = 0x13
            
            ###threshold
            th_hex = hex (threshold)[2:]
            th_padded = '0' * (4 - len(th_hex)) + th_hex 
            set_cmd[15] = int(th_padded[0:2],16)
            set_cmd[16] = int(th_padded[2:],16)
            # print("set scale",set_cmd)

            ####callback cmd
            cmd = [0x00 for i in range(33)]
        
            cmd[1] = 0x02
            cmd[2] = 0x49
            cmd[3] = 0x0a


            if self.device:
                if self.report:
                    # self.device.set_raw_data_handler(self.read_callback_USB)
                    self.report[0].set_raw_data(set_cmd)
                    bytes_num = self.report[0].send()

                    self.device.set_raw_data_handler(self.read_callback_USB_char)
                    self.report[0].set_raw_data(cmd)
                    bytes_num = self.report[0].send()
                    time.sleep(2)
                    # self.connect()
                    # print(self.usb_temp)
                    if self.usb_temp[0] == "45":
                        print( "!!!!!Setting Success!!!!!" )
                    elif self.usb_temp[0] == 'c5':
                        print( "!!!!!Setting Fail!!!!! ")


            # print ("rate " ,self.usb_temp[9])
        # self.read_data()
        time.sleep(3)
        
    def rst_count(self, mode = "Both", device=None):
        # print (mode)
        self.resetMode = mode
        if mode != "Both" and mode != "Store_Cnt" and mode !="Cur_Cnt":
            raise ValueError ("mode must be 'Both' or 'Cur_cnt' or 'Store_cnt' !")
        if self.mode == "BLE":
            self.reset = True
            if device is None:
                device = self.device
            if mode == "Cur_cnt" or mode == "Both" :
                # print("     Cur")
                if (self.dongle != "Bluegiga"):
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.set_sensor_config_async(loop,bytearray([0x38])))
                else :
                    device.char_write("0000fff6-0000-1000-8000-00805f9b34fb", bytearray([0x38]))
                    time.sleep(0.5)
                # device.char_write("0000fff6-0000-1000-8000-00805f9b34fb", bytearray([0x38]))
                # time.sleep(3)
            if mode == "Store_cnt" or mode == "Both" :
                # print("     Store")
                if (self.dongle != "Bluegiga"):
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.set_sensor_config_async(loop,bytearray([0x36])))
                else :
                    device.char_write("0000fff6-0000-1000-8000-00805f9b34fb", bytearray([0x36]))
                    time.sleep(0.5)
                # device.char_write("0000fff6-0000-1000-8000-00805f9b34fb", bytearray([0x36]))
                # time.sleep(3)
        elif self.mode == "USB":
            rst_cmd_stor = [0x00 for i in range(33)]
            rst_cmd_stor[1] = 0x02
            rst_cmd_stor[2] = 0x36
            rst_cmd_stor[3] =0x0a 

            rst_cmd_cur = [0x00 for i in range(33)]
            rst_cmd_cur[1] = 0x02
            rst_cmd_cur[2] = 0x38
            rst_cmd_cur[3] =0x0a 
            close_cmd = [0x00 for i in range(33)]
            close_cmd[1] = 0x02 # Report ID
            close_cmd[2] = 0x33
            close_cmd[3] = 0x0a
            cmd = [0x00 for i in range(33)]
            cmd[1] = 0x02
            cmd[3] = 0x0a
            send_32 = cmd.copy()
            send_32[2] = 0x32
            send_30 = cmd.copy()
            send_30[2] = 0x30
            if self.device:
                if self.report:
                    self.report[0].set_raw_data(close_cmd)
                    self.report[0].send()
                    time.sleep(0.5)

                    # self.report[0].set_raw_data(rst_cmd)
                    # bytes_num = self.report[0].send()
                    # time.sleep(0.5)
                    if mode == "Cur_cnt" or mode == "Both" :
                        self.report[0].set_raw_data(rst_cmd_cur)
                        bytes_num = self.report[0].send()
                        time.sleep(0.5)
                    if mode == "Store_cnt" or mode == "Both" :
                        self.report[0].set_raw_data(rst_cmd_stor)
                        bytes_num = self.report[0].send()
                        time.sleep(0.5)

                    # self.report[0].set_raw_data(rst_cmd_stor)
                    # bytes_num = self.report[0].send()
                    # time.sleep(0.5)

                    # self.report[0].set_raw_data(send_30)
                    # bytes_num = self.report[0].send()

                    self.report[0].set_raw_data(send_32)
                    bytes_num = self.report[0].send()
                    time.sleep(0.5)
            self.usb_temp = []

############################# callback
############################# callback
############################# callback
############################# callback
############################# callback
############################# callback
############################# callback

    def read_char_callback_ble(self, sender, data, debug=False  ):
        if self.mode == "BLE":
            value_data = hexlify(data)


            if self.Sensor_char == 0:
                self.Sensor_char = value_data
            acc_char = value_data[2:4]
            gyr_char = value_data[4:6]
            sam = value_data[16:18]
            # print(value_data)
            # print ("char: %s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s" %(value_data[:2],value_data[2:4],value_data[4:6],value_data[6:8],value_data[8:10],value_data[10:12],value_data[12:14],value_data[14:16],value_data[16:18],value_data[18:20],value_data[20:22],value_data[22:24]))



            # print ("rate " ,value_data[18:20])
            if value_data[0:2] == b'45':
                print( "!!!!!Setting Success!!!!!" )
            elif value_data[0:2] == b'c5':
                print( "!!!!!Setting Fail!!!!! ")
            if acc_char == b'00':
                self.Acc_char = 2 # 2G
            elif acc_char == b'01':
                self.Acc_char = 4 # 4G
            elif acc_char == b'02':
                self.Acc_char = 8 # 8G
            elif acc_char == b'03':
                self.Acc_char = 16 # 16G

            if gyr_char == b'00':
                self.Gyr_char = 250 # 2G
            elif gyr_char == b'01':
                self.Gyr_char = 500 # 4G
            elif gyr_char == b'02':
                self.Gyr_char = 1000 # 8G
            elif gyr_char == b'03':
                self.Gyr_char = 2000 # 16G


            if sam == b'00':
                self.sampling_rate = 10 # 10Hz
            elif sam == b'01':
                self.sampling_rate = 20 # 10Hz
            elif sam == b'02':
                self.sampling_rate = 50 # 10Hz
            elif sam == b'07':
                self.sampling_rate = 1 # 10Hz
            elif sam == b'08':
                self.sampling_rate = 5 # 10Hz
            elif sam == b'09':
                self.sampling_rate = 40 # 10Hz

            if (self.reset ==False):
                print ("Acc_char:",self.Acc_char,"Gyr_char:",self.Gyr_char,"Sampling_Rate: ",self.sampling_rate)
            else :
                if (self.resetMode =="Both"):
                    self.resetMode = "no"
                else :
                    self.reset = False
                    self.resetMode ="Both"
            





    def read_callback_BLE(self,sender, data, debug=False):
        if self.mode == "BLE":
            
            value_data = hexlify(data)
            # print(value_data)
            self.Hex_data = value_data
            self.Accx = convert_acc(value_data[:4],self.Acc_char)
            self.Accy = convert_acc(value_data[4:8],self.Acc_char)
            self.Accz = convert_acc(value_data[8:12],self.Acc_char)
            self.Gyrx = convert_gyro(value_data[12:16],self.Gyr_char)
            self.Gyry = convert_gyro(value_data[16:20],self.Gyr_char)
            self.Gyrz = convert_gyro(value_data[20:24],self.Gyr_char)
            # print("self.Cur_Cnt ",self.Cur_Cnt)
            self.Cur_Cnt  = int(value_data[24:28], 16)
            self.Store_Cnt  = int(value_data[28:], 16)
            self.time_list.append(time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()) )
            self.Accx_list.append(self.Accx)
            self.Accy_list.append(self.Accy)
            self.Accz_list.append(self.Accz)
            self.Gyrx_list.append(self.Gyrx)
            self.Gyry_list.append(self.Gyry)
            self.Gyrz_list.append(self.Gyrz)
            self.Cnt_list.append(self.Cur_Cnt)
            self.data_num +=1 
            if (self.qClass != None):
                acc = [self.Accx,self.Accy,self.Accz]
                gyr = [self.Gyrx,self.Gyry,self.Gyrz]
                self.q_last = self.qClass.Update(self.q_last ,acc, gyr, self.sampling_rate)
                self.q1 = self.q_last[0]
                self.q2 = self.q_last[1]
                self.q3 = self.q_last[2]
                self.q4 = self.q_last[3]
                self.q1_list.append (self.q_last[0])
                self.q2_list.append (self.q_last[1])
                self.q3_list.append (self.q_last[2])
                self.q4_list.append (self.q_last[3])
            if (self.dongle != "Bluegiga"):
                if (self.print == True and self.reset == False):
                    print ("--------------------------------")
                    print ("Acc_x : %f, Acc_y : %f, Acc_z : %f "% (self.Accx,self.Accy,self.Accz))
                    print ("Gyr_x : %f, Gyr_y : %f, Gyr_z : %f "% (self.Gyrx,self.Gyry,self.Gyrz))

                    if (self.qClass != None):
                        print ("Q1 : %f, Q2 : %f, Q3 : %f, Q4 : %f"% (self.q1,self.q2,self.q3,self.q4))
                    print ("Current_Count : %i"% (self.Cur_Cnt ))
                    print ("Store_Count : %i"% (self.Store_Cnt ))
                    


    def read_callback_USB(self,value):
        if self.mode == "USB":
            self.filter_data(value)
            self.get_data()

    def read_callback_USB_char(self,value):
        if self.mode == "USB":
            self.filter_data(value)
            



    def print_data(self):
        self.print = True
        time.sleep(0.05)
        if (self.dongle == "Bluegiga"):
            print ("--------------------------------")
            print ("Acc_x : %f, Acc_y : %f, Acc_z : %f "% (self.Accx,self.Accy,self.Accz))
            print ("Gyr_x : %f, Gyr_y : %f, Gyr_z : %f "% (self.Gyrx,self.Gyry,self.Gyrz))
            if (self.qClass != None):
                print ("Q1 : %f, Q2 : %f, Q3 : %f, Q4 : %f"% (self.q1,self.q2,self.q3,self.q4))
            print ("Current_Count : %i"% (self.Cur_Cnt ))
            print ("Store_Count : %i"% (self.Store_Cnt ))







    def filter_data(self,x):
        t = []
        for i in range( len(x)):
            hex_d = hex(x[i])[2:]
            if len(hex_d)==1:
                hex_d = "0"+hex_d
            t.append(hex_d)
        self.usb_temp.extend(t[2:2+(x[1])])

    def get_data(self):###USB
        # data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        # print ("WW")
        # print ("self.Acc_char",self.Acc_char)
        for i in range(len(self.usb_temp)):
            if self.usb_temp[i] == '10':
                if i+16 < len(self.usb_temp):
                    value_data = "".join (self.usb_temp[i+1:i+17])
                    del self.usb_temp[i:i+17]
                    # print ("data: %s_%s_%s_%s_%s_%s_%s" %(value_data[:4],value_data[4:8],value_data[8:12],value_data[12:16],value_data[16:20],value_data[20:24],value_data[24:]))
                    self.Hex_data = value_data
                    # print (self.Hex_data)
                    self.Accx = convert_acc(value_data[:4],self.Acc_char)
                    self.Accy = convert_acc(value_data[4:8],self.Acc_char)
                    self.Accz = convert_acc(value_data[8:12],self.Acc_char)
                    self.Gyrx = convert_gyro(value_data[12:16],self.Gyr_char)
                    self.Gyry = convert_gyro(value_data[16:20],self.Gyr_char)
                    self.Gyrz = convert_gyro(value_data[20:24],self.Gyr_char)

                    temp = value_data[26:28]
                    temp_ = value_data[24:26]
                    temp__ = temp+temp_
                    self.Cur_Cnt  = int(temp__, 16)## byte由右至左看
                    
                    temp = value_data[26:28]
                    temp_ = value_data[28:30]
                    temp__ = temp+temp_
                    self.Store_Cnt  = int(temp__, 16) ## byte由右至左看

                    self.time_list.append(time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()) )
                    self.Accx_list.append(self.Accx)
                    self.Accy_list.append(self.Accy)
                    self.Accz_list.append(self.Accz)
                    self.Gyrx_list.append(self.Gyrx)
                    self.Gyry_list.append(self.Gyry)
                    self.Gyrz_list.append(self.Gyrz)
                    self.Cnt_list.append(self.Cur_Cnt)
                    self.data_num +=1 
                break   
    def write_csv(self, data,file_name=None):
        if file_name ==None:
            raise("Need File_name!")
        else:
            file_name = file_name+'.csv'
            with open(file_name, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)

    def write_all_data(self, file_name=None,type = "csv",start = 1, end = None):
        if (end == None):
            end = len(self.time_list)
        time_list_temp = [self.time_list[0]]
        Accx_list_temp = [self.Accx_list[0]]
        Accy_list_temp = [self.Accy_list[0]]
        Accz_list_temp = [self.Accz_list[0]]
        Gyrx_list_temp = [self.Gyrx_list[0]]
        Gyry_list_temp = [self.Gyry_list[0]]
        Gyrz_list_temp = [self.Gyrz_list[0]]
        time_list_temp.extend(self.time_list[start:end])
        Accx_list_temp.extend(self.Accx_list[start:end])
        Accy_list_temp.extend(self.Accy_list[start:end])
        Accz_list_temp.extend(self.Accz_list[start:end])
        Gyrx_list_temp.extend(self.Gyrx_list[start:end])
        Gyry_list_temp.extend(self.Gyry_list[start:end])
        Gyrz_list_temp.extend(self.Gyrz_list[start:end])

        
        if file_name ==None:
            raise("Need File_name!")
        else:
            if (type == "csv"):
                file_name = file_name+'.csv'
                with open(file_name, 'w',newline ="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(time_list_temp)
                    writer.writerow(Accx_list_temp)
                    writer.writerow(Accy_list_temp)
                    writer.writerow(Accz_list_temp)
                    writer.writerow(Gyrx_list_temp)
                    writer.writerow(Gyry_list_temp)
                    writer.writerow(Gyrz_list_temp)
            elif (type == "xls"):
                file_name = file_name+'.xls'
                wb = Workbook() 
                # add_sheet is used to create sheet. 
                sheet1 = wb.add_sheet('Data') 
                for row in range(0,len(time_list_temp)):
                    sheet1.write(row, 0, time_list_temp[row]) 
                    sheet1.write(row, 1, Accx_list_temp[row]) 
                    sheet1.write(row, 2, Accy_list_temp[row]) 
                    sheet1.write(row, 3, Accz_list_temp[row]) 
                    sheet1.write(row, 4, Gyrx_list_temp[row]) 
                    sheet1.write(row, 5, Gyry_list_temp[row]) 
                    sheet1.write(row, 6, Gyrz_list_temp[row]) 
                
                wb.save(file_name) 
            else:
                raise("Output data type is not allowed!")


    def plot_pic(self, data, file_name=None,show = True):

        plt.plot(data[1:])
        if file_name != None:
            plt.savefig(file_name )
        if show == True:
            plt.show()






def convert_acc(acc,acc_scale):
    # print ("acc_scale",acc_scale)
    x = int(acc,16)
    x = twos_comp(x,16)
    x = float(x)
    return  x*(acc_scale)/32768 ##x*16/32768
    
def convert_gyro(gyro,gyro_scale):
    x = int(gyro,16)
    x = twos_comp(x,16)
    x = float(x)
    return x*gyro_scale/32768

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

