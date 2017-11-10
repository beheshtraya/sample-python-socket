"""
Socket Programming with multi-threading (client)
beheshtraya@gmail.com
"""

import socket
import threading

try:
    from Tkinter import *
    import tkMessageBox
    import ttk
except:
    # For python 3
    from tkinter import *
    import tkinter.messagebox as tkMessageBox
    import tkinter.ttk as ttk


HOST = '127.0.0.1'
TIME_PORT = 6666
CALC_PORT = 7777
COMMAND_PORT = 8888

class MainScreen(Frame):
    def __init__(self, master=None, width=0.4, height=0.21, useFactor=True):
        Frame.__init__(self, master)
        self.pack(expand=YES, fill=BOTH)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2) 
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.lift()

class SplashScreen(Frame):
    def __init__(self, master=None, width=0.4, height=0.2, useFactor=True):
        Frame.__init__(self, master)
        self.pack(expand=YES, fill=BOTH)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2) 
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.master.overrideredirect(True)
        self.lift()


class App:
    
    def __init__(self, master):
        header = ttk.Label(master, text="\n\nSocket Programming with multi-threading (Client)", font=(30)).pack()
        frame = ttk.Frame(master)
        frame['padding'] = (100, 40, 100, 30)
        frame['borderwidth'] = 20
        frame.pack()

        
        footer1 = ttk.Label(master, text='Seyed Mohamad Javad Beheshtian 8915113').pack()
        footer2 = ttk.Label(master, text='beheshtraya@gmail.com').pack()
        footer3 = ttk.Label(master, text='powered by python').pack()
        frm_btns = Frame(frame)
        btn_time = ttk.Button(frm_btns, text='Get time', command=self.start_time).pack(side=LEFT)
        btn_calc = ttk.Button(frm_btns, text='Calculate', command=self.start_calc).pack(side=LEFT)
        btn_command = ttk.Button(frm_btns, text='Command', command=self.start_command).pack(side=LEFT)
        
        self.calc_string = StringVar()
        self.txt_calc = ttk.Entry(frame, width=37, textvariable=self.calc_string).pack(side=BOTTOM)
        frm_btns.pack()
        
        print (self.calc_string.get())


    def start_time(self):
        self.t1 = threading.Thread(target=self.get_time)
        self.t1.run()

    def start_calc(self):
        self.t2 = threading.Thread(target=self.calc)
        self.t2.run()

    def start_command(self):
        self.t3 = threading.Thread(target=self.command)
        self.t3.run()

    def get_time(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((HOST, TIME_PORT))
        except:
            tkMessageBox.showerror( 'Error', "Cannot connect to server")
            return
            
        t = client.recv(50)
        client.close()
        msg_title = 'current server datetime'
        msg_body = t
        print (msg_title, msg_body)
        tkMessageBox.showinfo( msg_title, msg_body )
        return


    def calc(self):
        i = self.calc_string.get()
        if i.__len__() == 0:
            tkMessageBox.showinfo( '', 'Enter something to calculate' )
            return

        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((HOST, CALC_PORT))
        except:
            tkMessageBox.showerror( 'Error', "Cannot connect to server")
            return        
        
        client.sendall(i.encode())
        o = client.recv(1024)
        client.close()
        tkMessageBox.showinfo( 'Calculate result', o )
        print ('Calculate result', o)
        return

    def command(self):
        i = self.calc_string.get()
        if i.__len__() == 0:
            tkMessageBox.showinfo( '', 'Enter some command' )
            return
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((HOST, COMMAND_PORT))
        except:
            tkMessageBox.showerror( 'Error', "Cannot connect to server")
            return        
        
        client.sendall(i.encode())
        o = client.recv(1024).decode()
        client.close()
        tkMessageBox.showinfo( 'Command Info', o )
        print ('Command Info', o)
        return

x = 0

def func():
    global x
    x += 2
    p.config(padx=x)
    if x > 271:
        root1.after(0, lambda: root1.destroy())
        
    root1.after(2,func)

if __name__ == '__main__':
    root1 = Tk()

    sp = SplashScreen(root1)
    sp.config(bg="#836ff1")

    m = Label(sp, text="Socket Programming")
    m.pack(side=TOP, expand=YES)
    m.config(bg="#836ff1", justify=CENTER, font=("arial", 25), foreground="white")
    m2 = Label(sp, text="client server comiunication with multi-threading")
    m2.pack(side=TOP, expand=YES)
    m2.config(bg="#836ff1", justify=CENTER, font=("arial", 13), foreground="white")
    m3 = Label(sp, text="beheshtraya@gmail.com")
    m3.pack(side=TOP, expand=YES)
    m3.config(bg="#836ff1", justify=CENTER, font=("arial", 10), foreground="white")
    p = Label(sp, text="")
    p.pack(side=LEFT)
    p.config(bg="#0DFF00", justify=CENTER, font=("calibri", 1), relief=FLAT, padx=x, bd=0)    
    
    root1.after(1000,func)
    root1.mainloop()

    root2 = Tk()
    root2.title('Socket Programming')
    sp = MainScreen(root2)
    app = App(sp)
    root2.mainloop()


