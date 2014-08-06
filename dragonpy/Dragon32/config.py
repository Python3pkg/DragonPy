# coding: utf-8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2013-2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2013-2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import logging

from dragonpy.core.configs import BaseConfig

from dragonpy.Dragon32.mem_info import get_dragon_meminfo
from dragonpy.utils.logging_utils import log


class Dragon32Cfg(BaseConfig):
    """
    see:
     * http://dragon32.info/info/memmap.html
     * http://dragon32.info/info/romref.html
    """
    MACHINE_NAME = "Dragon 32"
    
    RAM_START = 0x0000
    
    # 1KB RAM is not runnable and raise a error
    # 2-8 KB - BASIC Interpreter will be initialized. But every
    #          statement will end with a OM ERROR (Out of Memory)
    # 16 KB - Is usable

#     RAM_END = 0x03FF # 1KB
#     RAM_END = 0x07FF # 2KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x0FFF # 4KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x1FFF # 8KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x3FFF # 16KB # usable
    RAM_END = 0x7FFF # 32KB

    ROM_START = 0x8000
    ROM_END = 0xBFFF
    ROM_SIZE = 0x4000 # 16384 Bytes

    DEFAULT_ROM = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "d32.rom"
    )

    def __init__(self, cmd_args):
        self.ROM_SIZE = (self.ROM_END - self.ROM_START) + 1
        self.RAM_SIZE = (self.RAM_END - self.RAM_START) + 1
        super(Dragon32Cfg, self).__init__(cmd_args)

        if self.verbosity <= logging.ERROR:
            self.mem_info = get_dragon_meminfo()

        self.periphery_class = None# Dragon32Periphery
        
        self.memory_byte_middlewares = {
#             (0x0152, 0x0159): (None, self.keyboard_matrix_state),
        }

    def keyboard_matrix_state(self, cpu, addr, value):
        log.critical(
            "%04x|      Set keyboard matrix state $%04x to $%02x %s\t\t\t|%s",
            cpu.last_op_address, addr, value, '{0:08b}'.format(value),
            self.mem_info.get_shortest(addr)
        )
        # cpu.memory.ram.print_dump(0x004f, 0x0054)
        return value

    def get_initial_RAM(self):
        """
        init the Dragon RAM
        See: http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4444
        """
        mem_FF = [0xff for _ in xrange(4)]
        mem_00 = [0x00 for _ in xrange(4)]

        mem = []
        for _ in xrange(self.RAM_SIZE / 8):
            mem += mem_FF
            mem += mem_00

        return mem


config = Dragon32Cfg
