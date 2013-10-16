#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================


    :created: 2013 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import logging
import sys
import Tkinter
import os
import pty
import serial

log = logging.getLogger("DragonPy.Periphery")

handler = logging.StreamHandler()
handler.level = logging.DEBUG
log.handlers = (handler,)



class Simple6809PeripheryBase(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.address2func_map = {
            0xbffe: self.reset_vector,
        }

    def read_byte(self, cpu_cycles, op_address, address):
        log.debug(
            "%04x| Periphery.read_byte from $%x (cpu_cycles: %i)" % (
            op_address, address, cpu_cycles
        ))
        if 0xa000 <= address <= 0xbfef:
            return self.read_rs232_interface(cpu_cycles, op_address, address)

        try:
            func = self.address2func_map[address]
        except KeyError, err:
            msg = "TODO: read byte from $%x" % address
            log.error(msg)
            raise NotImplementedError(msg)
        else:
            return func(address)

        raise NotImplementedError

    read_word = read_byte

    def write_byte(self, cpu_cycles, op_address, address, value):
        if 0xa000 <= address <= 0xbfef:
            return self.write_rs232_interface(cpu_cycles, op_address, address, value)

        msg = "%04x| TODO: write byte $%x to $%x" % (op_address, value, address)
        log.error(msg)
        raise NotImplementedError(msg)
    write_word = write_byte

    def cycle(self, cpu_cycles, op_address):
        log.debug("TODO: Simple6809Periphery.cycle")


    def read_rs232_interface(self, cpu_cycles, op_address, address):
        raise NotImplementedError

    def write_rs232_interface(self, cpu_cycles, op_address, address, value):
        raise NotImplementedError

    def reset_vector(self, address):
        return 0xdb46


class Simple6809PeripherySerial(Simple6809PeripheryBase):
    def __init__(self, cfg):
        super(Simple6809PeripherySerial, self).__init__(cfg)

        self.master, slave = pty.openpty()
        s_name = os.ttyname(slave)

        print "Serial name: %s" % s_name

        # http://pyserial.sourceforge.net/pyserial_api.html
        self.serial = serial.Serial(
            port=s_name, # Device name or port number number or None.
            baudrate=115200, # Baud rate such as 9600 or 115200 etc.
#             bytesize=serial.SEVENBITS, # Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
#             parity= ... #Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
#             stopbits= ... #Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
#              timeout=0, # non-blocking mode (return immediately on read)
#              timeout=None, # wait forever
#             xonxoff= ... #Enable software flow control.
#             rtscts=True, # Enable hardware (RTS/CTS) flow control.
#             dsrdtr= ... #Enable hardware (DSR/DTR) flow control.
#             writeTimeout= ... #Set a write timeout value.
#             interCharTimeout= ... #Inter-character timeout, None to disable (default).
        )
        log.log(100, repr(self.serial.getSettingsDict()))
        print "Please connect, e.g.: 'screen %s'" % s_name
        print "(ENTER to continue!)"
        sys.stdout.flush() # for eclipse :(
        raw_input()

        self.serial.write("Welcome to DragonPy") # write to pty
        self.serial.flush() # wait until all data is written


    def read_rs232_interface(self, cpu_cycles, op_address, address):
        """
        $00   0  NUL (Null Prompt)
        $01   1  SOH (Start of heading)
        $02   2  STX (Start of Text)
        $03   3  ETX (End of Text)
        $04   4  EOT (End of transmission)
        $05   5  ENQ (Enqiry)
        $06   6  ACK (Acknowledge)
        $07   7  BEL (Bell)
        $08   8  BS  (Backspace)
        $09   9  HT  (Horizontal Tab)
        $0a  10  LF  (LineFeed)
        $0b  11  VT  (Vertical Tab)
        $0c  12  FF  (Form Feed)
        $0d  13  CR  (Carriage Return)
        $0e  14  SO  (Shift Out)
        $0f  15  SI  (Shift In)
        $10  16  DLE (Data link Escape)
        $11  17  DC1 (X-On)
        $12  18  DC2 (X-On)
        $13  19  DC3 (X-Off)
        $14  20  DC4 (X-Off)
        $15  21  NAK (No Acknowledge)
        $16  22  SYN (Synchronous idle)
        $17  23  ETB (End transmission blocks)
        $18  24  CAN (Cancel)
        $19  25  EM  (End of Medium)
        $1a  26  SUB (Substitute)
        $1b  27  ESC (Escape)
        $1c  28  FS  (File Separator)
        $1d  29  GS  (Group Separator)
        $1e  30  RS  (Record Seperator)
        $1f  31  US  (Unit Seperator)
        $20  32  BLA (Blank)
        """
        log.error("%04x| (%i) read from RS232 address: $%x",
            op_address, cpu_cycles, address,
        )
        if address == 0xa000:
            return 0x02


#         char = self.serial.read()
        char = os.read(self.master, 1) # read from pty
        if char == "":
            value = 0x0
        else:
            value = ord(char)

        log.error("%04x| (%i) get from RS232 (address: $%x): %r ($%x)",
            op_address, cpu_cycles, address, char, value
        )
        return value

    def write_rs232_interface(self, cpu_cycles, op_address, address, value):
        """
                        * CONSOLE OUT
db14 8d 24              PUTCHR    BSR  WAITACIA
db16 34 02                        PSHS A
db18 81 0d                        CMPA #000d(CR)                  IS IT CARRIAGE RETURN?
db1a 27 0b                        BEQ  NEWLINE                    YES
db1c b7 a0 01                     STA  a001(TRANS)
db1f 0c 79                        INC  0079(LPTPOS)               INCREMENT CHARACTER COUNTER
db21 96 79                        LDA  0079(LPTPOS)               CHECK FOR END OF LINE PRINTER LINE
db23 91 78                        CMPA 0078(LPTWID)               AT END OF LINE PRINTER LINE?
db25 25 10                        BLO  PUTEND                     NO
db27 0f 79              NEWLINE   CLR  0079(LPTPOS)               RESET CHARACTER COUNTER
db29 8d 0f                        BSR  WAITACIA
db2b 86 0d                        LDA  #13
db2d b7 a0 01                     STA  a001(TRANS)
db30 8d 08                        BSR  WAITACIA
db32 86 0a                        LDA  #10                        DO LINEFEED AFTER CR
db34 b7 a0 01                     STA  a001(TRANS)
db37 35 02              PUTEND    PULS A
db39 39                           RTS

db3a 34 02              WAITACIA  PSHS A
db3c b6 a0 00           WRWAIT    LDA  a000(USTAT)
db3f 85 02                        BITA #2
db41 27 f9                        BEQ  db3c(WRWAIT)
db43 35 02                        PULS A
db45 39                           RTS

                        * INITIALISE ACIA
dbb0 86 95                        LDA  #0095(RTS_LOW)             DIV16 CLOCK -> 7372800 / 4 / 16 = 115200
dbb2 b7 a0 00                     STA  a000(UCTRL)
dbb5 8e dc 03                     LDX  #LA147-1                   POINT X TO COLOR BASIC COPYRIGHT MESSAGE
dbb8 bd eb e5                     JSR  LB99C                      PRINT 'COLOR BASIC'
dbbb 8e db c6                     LDX  #BAWMST                    WARM START ADDRESS
dbbe 9f 6f                        STX  006f(RSTVEC)               SAVE IT
dbc0 86 55                        LDA  #$55                       WARM START FLAG
dbc2 97 6e                        STA  006e(RSTFLG)               SAVE IT
dbc4 20 04                        BRA  LA0F3                      GO TO BASIC'S MAIN LOOP
        """
        if address == 0xa000:
            return 0xff
        
        if value == 0x95:
            # RTS low:
            log.error("%04x| (%i) set RTS low",
                op_address, cpu_cycles
            )
            try:
                self.serial.setRTS(True)
            except Exception, err:
                log.error("Error while serial.setRTS: %s" % err)
            return

        log.error("%04x| (%i) write to RS232 address: $%x value: $%x (dez.: %i) ASCII: %r" % (
            op_address, cpu_cycles, address, value, value, chr(value)
        ))
        self.serial.write(chr(value)) # write to pty
        self.serial.flush() # wait until all data is written


class Simple6809PeripheryTk(Simple6809PeripheryBase):
    def __init__(self, cfg):
        super(Simple6809PeripheryTk, self).__init__(cfg)
        self.root = Tkinter.Tk()
        self.root.title("DragonPy - Simple 6809")

        # http://www.tutorialspoint.com/python/tk_text.htm
        self.text = Tkinter.Text(self.root)

        self.text.pack()
        self.text.bind("<Return>", self.from_console)
        self.root.update()

        self.last_line = None

    def from_console(self, event):
        cursor = self.text.index("insert")
        line, pos = cursor.split(".")
        line = self.text.get("%s.0" % line, "%s.end" % line)
        self.last_line = list(line)
        log.error("Set last line to: %s", repr(self.last_line))

    def cycle(self, cpu_cycles, op_address):
        self.root.update()

    def read_rs232_interface(self, cpu_cycles, op_address, address):
        """
                        *
                        * THIS ROUTINE GETS A KEYSTROKE FROM THE KEYBOARD IF A KEY
                        * IS DOWN. IT RETURNS ZERO TRUE IF THERE WAS NO KEY DOWN.
                        *
                        *
                        LA1C1
db05 b6 a0 00           KEYIN     LDA  a000(USTAT)
db08 85 01                        BITA #1
db0a 27 06                        BEQ  NOCHAR
db0c b6 a0 01                     LDA  a001(RECEV)
db0f 84 7f                        ANDA #$7F
db11 39                           RTS
db12 4f                 NOCHAR    CLRA
db13 39                           RTS
        """
        log.debug(
#         log.error(
            "%04x| (%i) read from RS232 address: $%x",
            op_address, cpu_cycles, address,
        )

        if address == 0xa000:
            return 0xff
#             if self.last_line is None:
#                 self.last_line = []
#                 log.error("RS232: init")
#                 return 0xff
#
#             if self.last_line:
#                 log.info(
# #                 log.error(
#                     "RS232: chars in buffer: %s", repr(self.last_line)
#                 )
#                 return 0xff
#             else:
#                 log.debug(
# #                 log.error(
#                     "RS232: no char to send."
#                 )
#                 # no char to send
#                 return 0x0

        if self.last_line:
            char = self.last_line.pop(0)
            value = ord(char)
            log.error("%04x| (%i) read from RS232 address: $%x, send back %r $%x",
                op_address, cpu_cycles, address, char, value
            )
            return value

        return 0x0
        
    def write_rs232_interface(self, cpu_cycles, op_address, address, value):
        log.error("%04x| (%i) write to RS232 address: $%x value: $%x (dez.: %i) ASCII: %r" % (
            op_address, cpu_cycles, address, value, value, chr(value)
        ))
        if address == 0xa000:
            return 0xff

        char = chr(value)
        if char == "\r": # ignore
            return

        self.text.insert("end", char)


# Simple6809Periphery = Simple6809PeripherySerial
Simple6809Periphery = Simple6809PeripheryTk


def test_run():
    import subprocess
    cmd_args = [sys.executable,
        "DragonPy_CLI.py",
#         "--verbosity=5",
#         "--verbosity=10",
#         "--verbosity=20",
        "--verbosity=30",
#         "--verbosity=40",
#         "--verbosity=50",
        "--cfg=Simple6809Cfg",
#         "--max=100000",
#         "--max=30000",
#         "--max=20000",
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()

if __name__ == "__main__":
    test_run()
