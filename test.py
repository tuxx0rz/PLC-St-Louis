from pymodbus.client.sync import ModbusTcpClient
import mysql.connector
import struct


def main():
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

        
    #read and interpret HOLDING COILS (0XXXXX)
    holdingCoils = ModbusCnxn.read_coils(0, 125)
    SystemIsOn = holdingCoils.bits[0]
    MassInv_Active = holdingCoils.bits[1]
    
    #read and interpret INPUT COILS (1XXXXX)
    inputCoils = ModbusCnxn.read_discrete_inputs(0, 125)
    MOV001isOpen = inputCoils.bits[0]
    MOV002isOpen = inputCoils.bits[1]
    MOV003isOpen = inputCoils.bits[2]
    MOV004isOpen = inputCoils.bits[3]
    MOV005isOpen = inputCoils.bits[4]
    MOV006isOpen = inputCoils.bits[5]
    MOV007isOpen = inputCoils.bits[6]
    MOV008isOpen = inputCoils.bits[7]

    #read and interpret INPUT REGISTERS (3XXXXX)
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

    #read and interpret HOLDING REGISTERS (4XXXXX)
    holdingRegisters = ModbusCnxn.read_holding_registers(0, 125)
    TE004 = wordToFloat(holdingRegisters.getRegister(0), holdingRegisters.getRegister(1))
    TE010 = wordToFloat(holdingRegisters.getRegister(2), holdingRegisters.getRegister(3))
    PT001 = wordToFloat(holdingRegisters.getRegister(4), holdingRegisters.getRegister(5))
    PT002 = wordToFloat(holdingRegisters.getRegister(6), holdingRegisters.getRegister(7))
    PT003 = wordToFloat(holdingRegisters.getRegister(8), holdingRegisters.getRegister(9))
    PT004 = wordToFloat(holdingRegisters.getRegister(10), holdingRegisters.getRegister(11))
    PT005 = wordToFloat(holdingRegisters.getRegister(12), holdingRegisters.getRegister(13))
    PT006 = wordToFloat(holdingRegisters.getRegister(14), holdingRegisters.getRegister(15))
    PT007 = wordToFloat(holdingRegisters.getRegister(16), holdingRegisters.getRegister(17))
    PT008 = wordToFloat(holdingRegisters.getRegister(18), holdingRegisters.getRegister(19))
    PT009 = wordToFloat(holdingRegisters.getRegister(20), holdingRegisters.getRegister(21))
    PT010 = wordToFloat(holdingRegisters.getRegister(22), holdingRegisters.getRegister(23))
    PT011 = wordToFloat(holdingRegisters.getRegister(24), holdingRegisters.getRegister(25))
    
    #generate INPUT REGISTER query and insert into SQL Table
    query = "INSERT INTO logdata(TE001, TE002, TE003, TE004, TE005, TE006, TE007, TE008, " \
            "TE009, TE010, TE011, TE012, TE013, TE014, TE015, TE016) " \
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    args = (TE001, TE002, TE003, TE014, TE005, TE006, TE007, TE008,
            TE009, TE010, TE011, TE012, TE013, TE014, TE015, TE016)

    
    SQLCursor.execute(query, args)
    
    try:
        if SQLCursor.lastrowid:
            print('last insert id', SQLCursor.lastrowid)
        else:
            print('last insert id not found')
 
        SQLCnxn.commit()
    except Error as error:
        print(error)



def wordToFloat(word1, word2):
    packed = struct.pack('HH', word1, word2)
    unpacked = struct.unpack('f', packed)
    return unpacked[0]

if __name__ == '__main__':
    main()
