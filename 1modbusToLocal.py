from pymodbus.client.sync import ModbusTcpClient
import mysql.connector
import struct
from time import sleep
import ctypes


def main():
    #set window title
    ctypes.windll.kernel32.SetConsoleTitleA("1modbusToLocal.py")
    
    #establish Modbus cnxn to PLC
    ModbusCnxn = ModbusTcpClient('192.168.100.151')

    #establish SQL cnxn to localhost
    try:
        SQLCnxn = mysql.connector.connect(user='root', password='',
                                          host='localhost',
                                          database='prototype')
        SQLCursor = SQLCnxn.cursor()
    except Error as error:
        print(error)

    #loop process of reading and inserting into SQL table
    while True:
        #read and interpret HOLDING COILS (0XXXXX) [binary memory]
        holdingCoils = ModbusCnxn.read_coils(0, 125)
        
        SystemIsOn = holdingCoils.bits[0]
        MassInv_Active = holdingCoils.bits[1]
        Compressor_Active = holdingCoils.bits[2]
        Heater_Ready = holdingCoils.bits[3]
        Expander_Ready = holdingCoils.bits[4]
        Expander_EVsOpen = holdingCoils.bits[5]
        
        
        #read and interpret INPUT COILS (1XXXXX) [binary input]
        inputCoils = ModbusCnxn.read_discrete_inputs(0, 125)
        
        MOV001isOpen = not inputCoils.bits[0]
        MOV002isOpen = not inputCoils.bits[1]
        MOV003isOpen = not inputCoils.bits[2]
        MOV004isOpen = not inputCoils.bits[3]
        MOV005isOpen = not inputCoils.bits[4]
        MOV006isOpen = not inputCoils.bits[5]
        MOV007isOpen = not inputCoils.bits[6]
        MOV008isOpen = not inputCoils.bits[7]
        Heater_ElementOn = inputCoils.bits[8]

        
        #read and interpret INPUT REGISTERS (3XXXXX) [16-bit input]
        inputRegisters = ModbusCnxn.read_input_registers(0, 125)
        
        TE001 = wordToFloat(inputRegisters.getRegister(0), inputRegisters.getRegister(1))
        TE002 = wordToFloat(inputRegisters.getRegister(2), inputRegisters.getRegister(3))
        TE003 = wordToFloat(inputRegisters.getRegister(4), inputRegisters.getRegister(5))
        TE005 = wordToFloat(inputRegisters.getRegister(6), inputRegisters.getRegister(7))
        TE006 = wordToFloat(inputRegisters.getRegister(8), inputRegisters.getRegister(9))
        TE007 = wordToFloat(inputRegisters.getRegister(10), inputRegisters.getRegister(11))
        TE008 = wordToFloat(inputRegisters.getRegister(12), inputRegisters.getRegister(13))
        TE009 = wordToFloat(inputRegisters.getRegister(14), inputRegisters.getRegister(15))
        TE011 = wordToFloat(inputRegisters.getRegister(16), inputRegisters.getRegister(17))
        TE012 = wordToFloat(inputRegisters.getRegister(18), inputRegisters.getRegister(19))
        TE013 = wordToFloat(inputRegisters.getRegister(20), inputRegisters.getRegister(21))
        TE014 = wordToFloat(inputRegisters.getRegister(22), inputRegisters.getRegister(23))
        TE015 = wordToFloat(inputRegisters.getRegister(24), inputRegisters.getRegister(25))
        TE016 = wordToFloat(inputRegisters.getRegister(26), inputRegisters.getRegister(27))

        
        #read and interpret HOLDING REGISTERS (4XXXXX) [16-bit memory]
        holdingRegisters = ModbusCnxn.read_holding_registers(0, 125)
        
        TE004 = wordToFloat(holdingRegisters.getRegister(0), holdingRegisters.getRegister(1))
        TE010 = wordToFloat(holdingRegisters.getRegister(2), holdingRegisters.getRegister(3))
        PT001 = wordToFloat(holdingRegisters.getRegister(4), holdingRegisters.getRegister(5))
        PT002 = wordToFloat(holdingRegisters.getRegister(6), holdingRegisters.getRegister(7))
        PT003 = wordToFloat(holdingRegisters.getRegister(8), holdingRegisters.getRegister(9))
        PT004 = wordToFloat(holdingRegisters.getRegister(10), holdingRegisters.getRegister(11))
        PT006 = wordToFloat(holdingRegisters.getRegister(12), holdingRegisters.getRegister(13))
        PT007 = wordToFloat(holdingRegisters.getRegister(14), holdingRegisters.getRegister(15))
        PT008 = wordToFloat(holdingRegisters.getRegister(16), holdingRegisters.getRegister(17))
        PT009 = wordToFloat(holdingRegisters.getRegister(18), holdingRegisters.getRegister(19))
        PT010 = wordToFloat(holdingRegisters.getRegister(20), holdingRegisters.getRegister(21))
        PT011 = wordToFloat(holdingRegisters.getRegister(22), holdingRegisters.getRegister(23))
        AmbientTemp = wordToFloat(holdingRegisters.getRegister(24), holdingRegisters.getRegister(25))
        DPT001 = wordToFloat(holdingRegisters.getRegister(26), holdingRegisters.getRegister(27))
        DPT002 = wordToFloat(holdingRegisters.getRegister(28), holdingRegisters.getRegister(29))
        DPT003 = wordToFloat(holdingRegisters.getRegister(30), holdingRegisters.getRegister(31))
        MassInv_TargetBias = wordToFloat(holdingRegisters.getRegister(32), holdingRegisters.getRegister(33))
        MassInv_TargetLimitLO = wordToFloat(holdingRegisters.getRegister(34), holdingRegisters.getRegister(35))
        MassInv_TargetLimitHI = wordToFloat(holdingRegisters.getRegister(36), holdingRegisters.getRegister(37))
        MassInv_TargetLimitMID = wordToFloat(holdingRegisters.getRegister(38), holdingRegisters.getRegister(39))
        Compressor_Density = wordToFloat(holdingRegisters.getRegister(40), holdingRegisters.getRegister(41))
        Compressor_CurrentFlow = wordToFloat(holdingRegisters.getRegister(42), holdingRegisters.getRegister(43))
        Compressor_FlowSetPt = wordToFloat(holdingRegisters.getRegister(44), holdingRegisters.getRegister(45))
        Compressor_FlowSetPtLimitLO = wordToFloat(holdingRegisters.getRegister(46), holdingRegisters.getRegister(47))
        Compressor_FlowSetPtLimitHI = wordToFloat(holdingRegisters.getRegister(48), holdingRegisters.getRegister(49))
        PM_EXP_HZ = wordToFloat(holdingRegisters.getRegister(50), holdingRegisters.getRegister(51))
        PM_EXP_L1_AMPS = wordToFloat(holdingRegisters.getRegister(52), holdingRegisters.getRegister(53))
        PM_EXP_L1_VOLTS = wordToFloat(holdingRegisters.getRegister(54), holdingRegisters.getRegister(55))
        PM_EXP_L2_AMPS = wordToFloat(holdingRegisters.getRegister(56), holdingRegisters.getRegister(57))
        PM_EXP_L2_VOLTS = wordToFloat(holdingRegisters.getRegister(58), holdingRegisters.getRegister(59))
        PM_EXP_L3_AMPS = wordToFloat(holdingRegisters.getRegister(60), holdingRegisters.getRegister(61))
        PM_EXP_L3_VOLTS = wordToFloat(holdingRegisters.getRegister(62), holdingRegisters.getRegister(63))
        PM_EXP_PF = wordToFloat(holdingRegisters.getRegister(64), holdingRegisters.getRegister(65))
        PM_EXP_PWR = wordToFloat(holdingRegisters.getRegister(66), holdingRegisters.getRegister(67))
        PM_ACC1_Power_Avg = wordToFloat(holdingRegisters.getRegister(68), holdingRegisters.getRegister(69))
        PM_ACC2_Power_Avg = wordToFloat(holdingRegisters.getRegister(70), holdingRegisters.getRegister(71))
        PM_Comp_Power_Avg = wordToFloat(holdingRegisters.getRegister(72), holdingRegisters.getRegister(73))
        Subcooling = wordToFloat(holdingRegisters.getRegister(74), holdingRegisters.getRegister(75))
        MassInv_TargetPressure = wordToFloat(holdingRegisters.getRegister(76), holdingRegisters.getRegister(77))
        LB_Log_P1_Amps = wordToFloat(holdingRegisters.getRegister(78), holdingRegisters.getRegister(79))
        LB_Log_P2_Amps = wordToFloat(holdingRegisters.getRegister(80), holdingRegisters.getRegister(81))
        LB_Log_P3_Amps = wordToFloat(holdingRegisters.getRegister(82), holdingRegisters.getRegister(83))
        LB_Log_Avg_Amps = wordToFloat(holdingRegisters.getRegister(84), holdingRegisters.getRegister(85))
        LB_Log_Avg_Line_Volts = wordToFloat(holdingRegisters.getRegister(86), holdingRegisters.getRegister(87))
        LB_Log_L1_Volts = wordToFloat(holdingRegisters.getRegister(88), holdingRegisters.getRegister(89))
        LB_Log_L2_Volts = wordToFloat(holdingRegisters.getRegister(90), holdingRegisters.getRegister(91))
        LB_Log_L3_Volts = wordToFloat(holdingRegisters.getRegister(92), holdingRegisters.getRegister(93))
        LB_Log_Avg_Phase_Volts = wordToFloat(holdingRegisters.getRegister(94), holdingRegisters.getRegister(95))
        LB_Log_L1_Active_Power = wordToFloat(holdingRegisters.getRegister(96), holdingRegisters.getRegister(97))
        LB_Log_L2_Active_Power = wordToFloat(holdingRegisters.getRegister(98), holdingRegisters.getRegister(99))
        LB_Log_L3_Active_Power = wordToFloat(holdingRegisters.getRegister(100), holdingRegisters.getRegister(101))
        LB_Log_Total_Active_Power = wordToFloat(holdingRegisters.getRegister(102), holdingRegisters.getRegister(103))
        LB_Log_L1_Apparent_Power = wordToFloat(holdingRegisters.getRegister(104), holdingRegisters.getRegister(105))
        LB_Log_L2_Apparent_Power = wordToFloat(holdingRegisters.getRegister(106), holdingRegisters.getRegister(107))
        LB_Log_L3_Apparent_Power = wordToFloat(holdingRegisters.getRegister(108), holdingRegisters.getRegister(109))
        LB_Log_Total_Apparent_Power = wordToFloat(holdingRegisters.getRegister(110), holdingRegisters.getRegister(111))
        LB_Log_L1_Power_Factor = wordToFloat(holdingRegisters.getRegister(112), holdingRegisters.getRegister(113))
        LB_Log_L2_Power_Factor = wordToFloat(holdingRegisters.getRegister(114), holdingRegisters.getRegister(115))
        LB_Log_L3_Power_Factor = wordToFloat(holdingRegisters.getRegister(116), holdingRegisters.getRegister(117))
        LB_Log_Total_Power_Factor = wordToFloat(holdingRegisters.getRegister(118), holdingRegisters.getRegister(119))
        LB_Log_Frequency = wordToFloat(holdingRegisters.getRegister(120), holdingRegisters.getRegister(121))
        
        
        #generate query and insert into SQL Table
        query = "INSERT INTO logdata(SystemIsOn, MassInv_Active, Compressor_Active, " \
                    "Heater_Ready, Expander_Ready, Expander_EVsOpen, MOV001isOpen, " \
                    "MOV002isOpen, MOV003isOpen, MOV004isOpen, MOV005isOpen, " \
                    "MOV006isOpen, MOV007isOpen, MOV008isOpen, Heater_ElementOn, " \
                    "TE001, TE002, TE003, TE004, TE005, TE006, TE007, TE008, TE009, " \
                    "TE010, TE011, TE012, TE013, TE014, TE015, TE016, PT001, PT002, " \
                    "PT003, PT004, PT006, PT007, PT008, PT009, PT010, PT011, " \
                    "AmbientTemp, DPT001, DPT002, DPT003, MassInv_TargetBias, MassInv_TargetLimitLO, " \
                    "MassInv_TargetLimitHI, MassInv_TargetLimitMID, " \
                    "Compressor_Density, Compressor_CurrentFlow, Compressor_FlowSetPt, " \
                    "Compressor_FlowSetPtLimitLO, Compressor_FlowSetPtLimitHI, " \
                    "PM_EXP_HZ, PM_EXP_L1_AMPS, PM_EXP_L1_VOLTS, PM_EXP_L2_AMPS, " \
                    "PM_EXP_L2_VOLTS, PM_EXP_L3_AMPS, PM_EXP_L3_VOLTS, PM_EXP_PF, " \
                    "PM_EXP_PWR, PM_ACC1_Power_Avg, PM_ACC2_Power_Avg, " \
                    "PM_Comp_Power_Avg, Subcooling, MassInv_TargetPressure, LB_Log_P1_Amps, " \
                    "LB_Log_P2_Amps, LB_Log_P3_Amps, LB_Log_Avg_Amps, LB_Log_Avg_Line_Volts, " \
                    "LB_Log_L1_Volts, LB_Log_L2_Volts, LB_Log_L3_Volts, LB_Log_Avg_Phase_Volts, " \
                    "LB_Log_L1_Active_Power, LB_Log_L2_Active_Power, LB_Log_L3_Active_Power, " \
                    "LB_Log_Total_Active_Power, LB_Log_L1_Apparent_Power, LB_Log_L2_Apparent_Power, " \
                    "LB_Log_L3_Apparent_Power, LB_Log_Total_Apparent_Power, LB_Log_L1_Power_Factor, " \
                    "LB_Log_L2_Power_Factor, LB_Log_L3_Power_Factor, LB_Log_Total_Power_Factor, " \
                    "LB_Log_Frequency) " \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, " \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #90 vals
        args = (SystemIsOn, MassInv_Active, Compressor_Active,
                    Heater_Ready, Expander_Ready, Expander_EVsOpen, MOV001isOpen,
                    MOV002isOpen, MOV003isOpen, MOV004isOpen, MOV005isOpen,
                    MOV006isOpen, MOV007isOpen, MOV008isOpen, Heater_ElementOn,
                    TE001, TE002, TE003, TE004, TE005, TE006, TE007, TE008, TE009,
                    TE010, TE011, TE012, TE013, TE014, TE015, TE016, PT001, PT002,
                    PT003, PT004, PT006, PT007, PT008, PT009, PT010, PT011,
                    AmbientTemp, DPT001, DPT002, DPT003, MassInv_TargetBias, MassInv_TargetLimitLO,
                    MassInv_TargetLimitHI, MassInv_TargetLimitMID,
                    Compressor_Density, Compressor_CurrentFlow, Compressor_FlowSetPt,
                    Compressor_FlowSetPtLimitLO, Compressor_FlowSetPtLimitHI,
                    PM_EXP_HZ, PM_EXP_L1_AMPS, PM_EXP_L1_VOLTS, PM_EXP_L2_AMPS,
                    PM_EXP_L2_VOLTS, PM_EXP_L3_AMPS, PM_EXP_L3_VOLTS, PM_EXP_PF,
                    PM_EXP_PWR, PM_ACC1_Power_Avg, PM_ACC2_Power_Avg,
                    PM_Comp_Power_Avg, Subcooling, MassInv_TargetPressure, LB_Log_P1_Amps,
                    LB_Log_P2_Amps, LB_Log_P3_Amps, LB_Log_Avg_Amps, LB_Log_Avg_Line_Volts,
                    LB_Log_L1_Volts, LB_Log_L2_Volts, LB_Log_L3_Volts, LB_Log_Avg_Phase_Volts,
                    LB_Log_L1_Active_Power, LB_Log_L2_Active_Power, LB_Log_L3_Active_Power,
                    LB_Log_Total_Active_Power, LB_Log_L1_Apparent_Power, LB_Log_L2_Apparent_Power,
                    LB_Log_L3_Apparent_Power, LB_Log_Total_Apparent_Power, LB_Log_L1_Power_Factor,
                    LB_Log_L2_Power_Factor, LB_Log_L3_Power_Factor, LB_Log_Total_Power_Factor,
                    LB_Log_Frequency)
        
        SQLCursor.execute(query, args)
        
        try:
            if SQLCursor.lastrowid:
                print(SQLCursor.lastrowid, "local row inserted")
            else:
                print("last insert id not found!")
     
            SQLCnxn.commit()
        except Error as error:
            print(error)

        if (SystemIsOn):
            sleep(0.5)
        else:
            sleep(5)


def wordToFloat(word1, word2):
    packed = struct.pack('HH', word1, word2)
    unpacked = struct.unpack('f', packed)
    return unpacked[0]

if __name__ == '__main__':
    main()
