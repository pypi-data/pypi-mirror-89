#-*- coding: utf-8 -*-

import snap7
import random
import sys
from datetime import datetime
from enum import Enum

from EasyS7.Utility import *
from EasyS7.DataTypes.DTdint import  DTdint
from EasyS7.DataTypes.DTbool import  DTbool
from EasyS7.DataTypes.DTtime import  DTtime
from EasyS7.DataTypes.DTint import  DTint
from EasyS7.DataTypes.DTstring import  DTstring


class Areas(Enum):
    Input = 1
    Output = 2
    Merker = 3
    DB = 4
    Counter = 5
    Timer = 6

class DataTypes(Enum):
    Real = 1
    Bool = 2
    DInt = 3
    UDInt = 4
    Int = 5
    DTime = 6
    String = 7


class DataBlockObj(object):
		pass





def dbRead(plc,db_num,length,dbitems):

    data=plc.db_read(db_num,0,length)
    obj = DataBlockObj()

    for item in dbitems:
        value = (None,item['name'])
        offset = int(item['bytebit'].split('.')[0])

        if item['datatype']=='Real':
            value = (snap7.util.get_real(data,offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='Bool':
            bit =int(item['bytebit'].split('.')[1])
            BoolObj=DTbool(data,bit)
            value = (snap7.util.get_bool(data,offset,bit),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='DInt' :

            DintObj=DTdint(data)
            value=(DintObj.readValue(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='UDInt':

            DintObj=DTdint(data)
            value=(DintObj.readValueU(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='Int':

            IntObj=DTint(data)
            value=(IntObj.readValue(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])


        """if item['datatype']=='Time':

            TimeObj=DTtime() # burası düzeltilecek
            value=(TimeObj.readValue(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])"""



        if item['datatype'].startswith('String'):
            value = snap7.util.get_string(data, offset,int(item['datatype'].split('[')[1][:-1])+1)
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value)

        #obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])


    return obj


def dbWrite(plc, db_num,item):
    pass


def dbWriteArea(plc,area_type, address ,item_data_type, item, db_num = -1, bool_index = -1, string_max_size = -1):

    address_integer = int(address)
    address_fraction = (address-address_integer)*10

    if area_type == Areas.Input:
        area = snap7.snap7types.S7AreaPE
        offset = address_integer*8 + address_fraction
    elif area_type == Areas.Output:
        area = snap7.snap7types.S7AreaPA
        offset = address_integer*8 + address_fraction
    elif area_type == Areas.Merker:
        area = snap7.snap7types.S7AreaMK
        offset = address_integer*8 + address_fraction
    elif area_type == Areas.DB:
        if db_num < 0:
            print("[Error] : Data Block Number Not Defined. Use Optional Argument db_num.")
            sys.exit()
        area = snap7.snap7types.S7AreaDB
        offset = address
    elif area_type == Areas.Counter:
        area = snap7.snap7types.S7AreaCT
        offset = address_integer*16 + address_fraction
    elif area_type == Areas.Timer:
        area = snap7.snap7types.S7AreaTM
        offset = address_integer*16 + address_fraction

    


    if item_data_type == DataTypes.Real:
        byte_array = bytearray(4)
        snap7.util.set_real(byte_array,0,item)

    elif item_data_type == DataTypes.Bool:
        if bool_index <0 : 
            print("[Error] : Bool Index Not Defined. Use Optional Argument bool_index")
            sys.exit()
        else:
            byte_array = plc.read_area(area,db_num,offset,1)
            snap7.util.set_bool(byte_array,0,bool_index,item)

    elif item_data_type == DataTypes.DInt:
        byte_array = bytearray(4)
        DIntObj = DTdint(byte_array)
        byte_array = DIntObj.set_dint(byte_array,0,item)

    elif item_data_type == DataTypes.UDInt:
        byte_array = bytearray(4)
        DIntObj = DTdint(byte_array)
        byte_array = DIntObj.set_udint(byte_array,0,item)

    elif item_data_type == DataTypes.Int:
        byte_array = bytearray(4)
        snap7.util.set_int(byte_array,0,item)

    elif item_data_type == DataTypes.DTime:

        print("[ERROR] : Time Not Implemented")
        sys.exit()
        """dtl = plc.db_read(db_num,16, 8)
        
        pdb.set_trace()
        
        DTimeObject = DTtime()
        byte_array1 = (DTimeObject.set_dtime(item))
        byte_array = dtl
        pdb.set_trace()"""
        
        

    elif item_data_type == DataTypes.String:
        if string_max_size <= 0 :
            print("[Error] : Max String Size Not Defined. Use Optional Argument string_max_size")
            sys.exit()
        else:
            
            StringObj = DTstring()
            byte_array = plc.read_area(area,db_num,offset,string_max_size)

            StringObj.set_string(byte_array,0,item,string_max_size)

        
        


          

   

    plc.write_area(area,db_num,offset,byte_array)


