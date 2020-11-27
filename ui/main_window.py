import logging
from threading import Thread
from tkinter import *
from tkinter.scrolledtext import ScrolledText

from lib.control_unit.control_core import ControlCore
from lib.control_unit.register import Register

console = logging.getLogger(__name__)


class MainWindow:
    core: ControlCore

    def __init__(self):
        self.last_change = -1
        self.window = Tk()

        self.window.title("ARMaria VM")

        for col in range(2):
            self.window.grid_columnconfigure(col, weight=1)

        self.window.grid_rowconfigure(0, weight=1)

        self.console = ScrolledText(self.window)
        self.memory = ScrolledText(self.window)

        self.registers_text = StringVar()
        self.registers = Label(self.window, bd=1, anchor=W, textvariable=self.registers_text)

        self.btn_frame = Frame(self.window)

        self.next_btn = Button(self.btn_frame, text="Next", command=self.iterate).pack(side=LEFT)
        self.play_btn = Button(self.btn_frame, text="Play", command=self.play).pack(side=LEFT)
        self.pause_btn = Button(self.btn_frame, text="Pause", command=self.pause).pack(side=LEFT)
        self.play_btn = Button(self.btn_frame, text="Reset", command=self.reset).pack(side=LEFT)

        self._disable_textfield(self.console)
        self._disable_textfield(self.memory)
        self._disable_textfield(self.registers)

        self.console.grid(column=0, row=0, sticky=N + S + W + E)
        self.memory.grid(column=1, row=0, sticky=N + S + W + E)
        self.btn_frame.grid(column=0, row=1, sticky=E)
        self.registers.grid(column=1, row=1, sticky=W + E)

    @classmethod
    def _disable_textfield(cls, field):
        field.bind("<Key>", lambda e: "break")

    def print_console(self, text):
        self.console.insert(END, f"{text}\n")
        self.console.see(END)

    def print_memory(self, text):
        lines = text.split('\n')

        change_idx = -1
        for index, line in enumerate(lines):
            if "<<<" in line and index != self.last_change:
                change_idx = index
                self.last_change = change_idx

            self.memory.insert('1.0', f"{text}\n")
            self.memory.delete(f"{len(lines)}.0", END)

        if change_idx > 0:
            self.memory.see(f"{change_idx + 1}.0")

    def iterate(self, auto=False):
        try:
            self.core.iterate()
            if not (auto and self.core.running):
                self.update_data()
        except Exception as e:
            self.core.running = False
            console.error(f"\n\n!!! EXCEPTION: {e} !!!")
            raise e

    def play(self):
        self.core.running = True

        def runner():
            while self.core.running:
                self.iterate(auto=True)
            self.update_data()

        control_thread = Thread(target=runner, daemon=True)
        control_thread.start()

    def pause(self):
        self.core.running = False

    def reset(self):
        self.core.reset()
        self.console.delete('1.0', END)
        self.update_data()
        self.last_change = -1

    def update_data(self):
        self.print_memory(str(self.core.memory_ctrl))
        self.registers_text.set("   ".join([f"{reg.shortName()}: {reg.getValue()}" for reg in Register]))

    def run(self, core: ControlCore):
        self.core = core
        self.reset()
        self.update_data()

        self.window.mainloop()
