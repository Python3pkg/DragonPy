#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import Queue
import Tkinter
import os
import sys
import thread
import threading
import time
import tkMessageBox

from dragonpy.Dragon32.dragon_charmap import get_charmap_dict
from dragonpy.Dragon32.dragon_font import CHARS_DICT, TkFont
from dragonpy.utils.logging_utils import log


class TkImgThread(threading.Thread):
    """
    consume display_queue and generate a Tkinter.PhotoImage() from it.
    Put the PhotoImage into img_queue for display it in the main thread.

    Important is that CACHE is used. Without cache the garbage-collection
    by Python will "remove" the created images in Tkinter.Canvas!
    """
    CACHE = {}
    def __init__(self, display_queue, img_queue):
        log.critical("init TkImgThread")
        super(TkImgThread, self).__init__(name="TkImgThread")
        self.display_queue = display_queue
        self.img_queue = img_queue

        self.rows = 32
        self.columns = 16

        #         scale_factor=1
        scale_factor = 2
#         scale_factor=3
#         scale_factor=4
#         scale_factor=8
        self.tk_font = TkFont(CHARS_DICT, scale_factor)

        self.total_width = self.tk_font.width_scaled * self.rows
        self.total_height = self.tk_font.height_scaled * self.columns

        self.charmap = get_charmap_dict()

    def generate_image(self, cpu_cycles, op_address, address, value):
        try:
            img = self.CACHE[value]
        except KeyError:
            char, color = self.charmap[value]
            log.critical("Genrate PhotoImage for $%02x: %r %s", value, char, color)
    #         log.critical(
    #             "%04x| *** Display write $%02x ***%s*** %s at $%04x",
    #             op_address, value, repr(char), color, address
    #         )

            img = self.tk_font.get_char(char, color)
            self.CACHE[value] = img

        position = address - 0x400
        column, row = divmod(position, self.rows)
        x = self.tk_font.width_scaled * row
        y = self.tk_font.height_scaled * column

        return x, y, img

    def _run(self):
        while True:
            cpu_cycles, op_address, address, value = self.display_queue.get(block=True)
#             log.critical("TkImgThread")
            x, y, img = self.generate_image(cpu_cycles, op_address, address, value)
            self.img_queue.put(
                (x, y, img),
                block=True
            )

    def run(self):
        log.critical("start TkImgThread.run()")
        try:
            self._run()
        except:
            thread.interrupt_main()
            raise
        log.critical("end TkImgThread.run()")


class Dragon32TextDisplayTkinter(object):
    """
    The GUI stuff
    """
    def __init__(self, root):
        self.rows = 32
        self.columns = 16

        #         scale_factor=1
        scale_factor = 2
#         scale_factor=3
#         scale_factor=4
#         scale_factor=8
        self.tk_font = TkFont(CHARS_DICT, scale_factor)

        self.total_width = self.tk_font.width_scaled * self.rows
        self.total_height = self.tk_font.height_scaled * self.columns

        self.charmap = get_charmap_dict()

    def write_byte(self, cpu_cycles, op_address, address, value):
        char, color = self.charmap[value]
#         log.critical(
#             "%04x| *** Display write $%02x ***%s*** %s at $%04x",
#             op_address, value, repr(char), color, address
#         )

        img = self.tk_font.get_char(char, color)

        position = address - 0x400
        column, row = divmod(position, self.rows)
        x = self.tk_font.width_scaled * row
        y = self.tk_font.height_scaled * column


class DragonTkinterGUI(object):

    def __init__(self, cfg, display_queue, key_input_queue, cpu_status_queue):
        self.cfg = cfg
        self.display_queue = display_queue
        self.key_input_queue = key_input_queue
        self.cpu_status_queue = cpu_status_queue

        self.last_cpu_cycles = 0
        self.last_cpu_cycle_update = time.time()

        self.root = Tkinter.Tk(className="DragonPy")
        machine_name = self.cfg.MACHINE_NAME
        self.root.title(
            "%s - Text Display 32 columns x 16 rows" % machine_name)

        self.root.bind("<Key>", self.event_key_pressed)
        self.root.bind("<<Paste>>", self.paste_clipboard)

        # Start display_queue to img_queue converter thread
        self.img_queue = Queue.Queue(maxsize=64)
        self.display_write2image_thread = TkImgThread(self.display_queue, self.img_queue)
        self.display_write2image_thread.deamon = True
        self.display_write2image_thread.start()

        # Display the generated img_queue output
        self.display_canvas = Tkinter.Canvas(self.root,
            width=self.display_write2image_thread.total_width,
            height=self.display_write2image_thread.total_height,
            bd=0,  # Border
            bg="#ff0000",
        )
        self.display_canvas.grid(row=0, column=0, columnspan=2)  # , rowspan=2)

        self.status = Tkinter.StringVar()
        self.status_widget = Tkinter.Label(
            self.root, textvariable=self.status, text="Info:", borderwidth=1)
        self.status_widget.grid(row=1, column=0, columnspan=2)

        menubar = Tkinter.Menu(self.root)

        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="load", command=self.load)
        editmenu.add_command(label="dump", command=self.dump)
        menubar.add_cascade(label="edit", menu=editmenu)

        # help menu
        helpmenu = Tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="help", command=self.menu_event_help)
        helpmenu.add_command(label="about", command=self.menu_event_about)
        menubar.add_cascade(label="help", menu=helpmenu)

        # display the menu
        self.root.config(menu=menubar)
        self.root.update()

    def dump(self):
        tkMessageBox.showinfo("TODO", "TODO: dump!")

    def load(self):
        tkMessageBox.showinfo("TODO", "TODO: load!")

    def menu_event_about(self):
        tkMessageBox.showinfo("DragonPy",
            "DragonPy the OpenSource emulator written in python.\n"
            "more info: https://github.com/jedie/DragonPy"
        )

    def menu_event_help(self):
        tkMessageBox.showinfo("Help",
            "Please read the README:"
            "https://github.com/jedie/DragonPy#readme"
        )

    def exit(self):
        log.critical("DragonTkinterGUI.exit()")
        try:
            self.root.destroy()
        except:
            pass
        super(DragonTkinterGUI, self).exit()

    def paste_clipboard(self, event):
        """
        Send the clipboard content as user input to the CPU.
        """
        log.critical("paste clipboard")
        clipboard = self.root.clipboard_get()
        for line in clipboard.splitlines():
            log.critical("paste line: %s", repr(line))
            for char in line:
                self.key_input_queue.put(char)
            self.key_input_queue.put("\r")

    def event_key_pressed(self, event):
        char_or_code = event.char or event.keycode
        self.key_input_queue.put(char_or_code)

    def display_cpu_status_interval(self, interval):
        """
        Update the 'cycles/sec' in the GUI
        """
        try:
            cycles = self.cpu_status_queue.get(block=False)
        except Queue.Empty:
            log.critical("no new cpu_status_queue entry")
            pass
        else:
            new_cycles = cycles - self.last_cpu_cycles
            duration = time.time() - self.last_cpu_cycle_update
            self.last_cpu_cycles = cycles
            self.last_cpu_cycle_update = time.time()
            cycles_per_second = int(new_cycles / duration)

#             msg = "%i cycles/sec - Dragon ~895.000cycles/s (%i cycles in last %0.1fs)" % (
#                 cycles_per_second, new_cycles, duration
#             )
            msg = "%d cycles/sec (Dragon 32 == 895.000cycles/sec)" % cycles_per_second
#             log.critical(msg)
            self.status.set(msg)
            self.root.update()

        self.root.after(interval, self.display_cpu_status_interval, interval)

    def display_queue_interval(self, interval):
        """
        Consume img_queue generated in TkImgThread.
        Display all generated PhotoImage on the display_canvas.
        """
        max_time = time.time() + 0.25
        while True:
            try:
                x, y, img = self.img_queue.get_nowait()
            except Queue.Empty:
                break

            log.critical("Add new PhotoImage to %i x %i", x, y)
            self.display_canvas.create_image(x, y,
                image=img,
                state="normal",
                anchor=Tkinter.NW  # NW == NorthWest
            )
            if time.time() > max_time:
                log.critical(
                    "Abort display_queue_interval() loop. (display_queue._qsize(): %i)",
                    self.display_queue._qsize()
                )
                break
#                 self.root.update()
#                 self.root.after_idle(self.display_queue_interval, interval)
#                 return

#         log.critical(
#             "exit display_queue_interval (display_queue._qsize(): %i)",
#             self.display_queue._qsize()
#         )
        self.root.after(interval, self.display_queue_interval, interval)

    def mainloop(self):
        log.critical("Start display_queue_interval()")
        self.display_queue_interval(interval=50)

        log.critical("Start display_cpu_status_interval()")
        self.display_cpu_status_interval(interval=1000)

        log.critical("Start root.mainloop()")
        self.root.mainloop()
        log.critical("root.mainloop() has quit!")


def test_run_direct():
    import subprocess
    cmd_args = [
        sys.executable,
        #         "/usr/bin/pypy",
        os.path.join("..",
            "Dragon32_test.py"
#             "Dragon64_test.py"
        ),
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()


if __name__ == "__main__":
    #     test_run_cli()
    test_run_direct()
