import tkinter as tk
from time import sleep
import math
import threading
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def dict_from_module(module):
    context = {}
    for setting in dir(module):
        # you can write your filter here
        if setting.islower() and setting.isalpha():
            context[setting] = getattr(module, setting)

    return context

def run():
    global close

    out = []
    nums = []
    frames = []

    cmds = []
    hist_pointer = 0

    def pref(event):
        nonlocal hist_pointer

        if -hist_pointer<len(cmds):
            hist_pointer -= 1
            input_box.delete(0, tk.END)
            input_box.insert(index=0, string=cmds[hist_pointer])



    def nxt(event):
        nonlocal hist_pointer

        if -hist_pointer>1:
            hist_pointer+=1
            input_box.delete(0, tk.END)
            input_box.insert(index=0, string=cmds[hist_pointer])
        else:
            hist_pointer = 0
            input_box.delete(0, tk.END)

    var_dict = dict()
    var_dict = dict_from_module(math)

    def close(event):
        root.destroy()

    import ctypes

    #   store some stuff for win api interaction
    set_to_foreground = ctypes.windll.user32.SetForegroundWindow
    keybd_event = ctypes.windll.user32.keybd_event

    alt_key = 0x12
    extended_key = 0x0001
    key_up = 0x0002

    def center():
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
        root.geometry("+{}+{}".format(positionRight, positionDown))

    def steal_focus():
        sleep(0.05)
        while 1:
            keybd_event(alt_key, 0, extended_key | 0, 0)
            set_to_foreground(root.winfo_id())
            keybd_event(alt_key, 0, extended_key | key_up, 0)

            input_box.focus_set()
            sleep(0.5)
            break

    b = threading.Thread(name='background', target=steal_focus)

    root = tk.Tk()
    input_box = tk.Entry(root,width=50)
    input_box.pack()

    root.overrideredirect(1)




    def do(event):
        inp = input_box.get()

        cmds.append(inp)
        nonlocal hist_pointer
        hist_pointer = 0

        input_box.delete(0, tk.END)

        if inp == "/clr":
            for l in out:
                l.destroy()
            for l in nums:
                l.destroy()
            for l in frames:
                l.destroy()

        else:
            frames.append(tk.Frame(root))
            out.append(tk.Label(frames[-1]))
            try:
                with stdoutIO() as s:
                    exec(inp,var_dict)
                printed = s.getvalue()
                if printed:

                    for line in printed.splitlines():
                        out[-1].configure(
                            text=str(line))
                        out[-1].configure(background='blue')
                        out[-1].pack(side=tk.RIGHT, fill='x', expand=True)
                        frames[-1].pack(after=input_box, fill="x")

                        frames.append(tk.Frame(root))
                        out.append(tk.Label(frames[-1]))



                try:
                    txt = eval(inp, var_dict)
                    var_dict["_"] = txt
                    var_dict["__"+str(len(cmds)-1)] = txt
                    out[-1].configure(
                        text=inp + ": " + str(txt))
                    out[-1].configure(background='yellow')
                    out[-1].pack(side=tk.RIGHT, fill='x', expand=True)



                except:

                    out[-1].configure(text=inp)
                    out[-1].configure(background='green')
                    out[-1].pack(side=tk.RIGHT, fill='x', expand=True)



            except Exception as e:
                out[-1].configure(text=str(inp)+": "+str(e))
                out[-1].configure(background='orange')
                out[-1].pack(side=tk.RIGHT, fill='x', expand=True)


            nums.append(tk.Label(frames[-1]))
            nums[-1].configure(text=len(cmds) - 1)
            nums[-1].pack(side=tk.LEFT)

            frames[-1].pack(after=input_box, fill="x")


        #print(inp)
        # root.withdraw()
        root.update_idletasks()
        center()



    root.bind('<Escape>', close)
    input_box.bind('<Return>', do)
    input_box.bind('<Up>', pref)
    input_box.bind('<Down>', nxt)

    root.attributes("-topmost", True)
    input_box.focus_force()

    root.wait_visibility(root)
    center()

    b.start()
    # root.after(10, steal_focus)


    tk.mainloop()

