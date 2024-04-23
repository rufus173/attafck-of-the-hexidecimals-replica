import random
import threading
import tkinter
import time
import socket
from tkinter import messagebox
class main():
    def __init__(self):
        self.hexes = []
        self.selected_hex = 0
        self.root = tkinter.Tk()
        self.root.bind("<Key>",self.number_keys)
        self.root.title("hex attack")
        self.root.attributes("-transparentcolor","yellow")
        #self.root.configure(background="yellow")
        self.canvas = tkinter.Canvas()
        self.canvas.grid(row=0,column=0,columnspan=8,sticky=tkinter.NSEW)
        #self.canvas.configure(background="yellow")
        self.bttns = {
            "1":tkinter.Button(self.root,text="0",command=lambda:self.bits(1)),
            "2":tkinter.Button(self.root,text="0",command=lambda:self.bits(2)),
            "4":tkinter.Button(self.root,text="0",command=lambda:self.bits(4)),
            "8":tkinter.Button(self.root,text="0",command=lambda:self.bits(8)),
            "16":tkinter.Button(self.root,text="0",command=lambda:self.bits(16)),
            "32":tkinter.Button(self.root,text="0",command=lambda:self.bits(32)),
            "64":tkinter.Button(self.root,text="0",command=lambda:self.bits(64)),
            "128":tkinter.Button(self.root,text="0",command=lambda:self.bits(128))
        }
        cntr = 7
        for i in range(8):
            self.root.columnconfigure(i, weight=1)
        self.root.rowconfigure(0,weight=1)
        for i in self.bttns:
            self.bttns[i].grid(column=cntr,row=1,columnspan=1,rowspan=1,sticky=tkinter.NSEW)
            cntr -= 1
        self.root.update()
        self.x = self.canvas.create_text(50,0,text="90",font=(12))
        self.root.update()
        self.hexes.append(self.x)
        self.scorecounter = self.canvas.create_text(self.canvas.winfo_width()-20,self.canvas.winfo_height()-20,text="0",fill="green")
        self.hex_indicator = self.canvas.create_text(20,self.canvas.winfo_height()-20,text="0",fill="red")
        self.portal = self.canvas.create_rectangle(-40,-15,0,0,fill="orange")
        self.window_x = self.root.winfo_width()
        threading.Thread(target=self.loop).start()
        threading.Thread(target=self.networking).start()
        self.default_colour = self.bttns[str(1)].cget("background")
        self.sliding_portal = self.canvas.create_rectangle(-40,-15,0,0,fill="orange")
        self.root.mainloop()
    def bits(self,bit):
        if self.bttns[str(bit)]["text"] == "0":
            self.bttns[str(bit)]["text"] = "1"
            self.bttns[str(bit)]["bg"] = "orange"
            
        else:
            self.bttns[str(bit)]["text"] = "0"
            self.bttns[str(bit)]["bg"] = self.default_colour
        counter = 0
        for i in self.bttns:
            if self.bttns[i]["text"] == "1":
                counter += int(i)
        self.selected_hex = str(hex(counter).split('x')[-1])
        self.canvas.itemconfig(self.hex_indicator,text = self.selected_hex)
        #self.canvas.moveto(self.sliding_portal,((self.root.winfo_width()/255)*counter)-20,200)
    def loop(self):
        counter = 0
        while True:
            self.canvas.coords(self.hex_indicator,20,self.canvas.winfo_height()-20)
            self.canvas.coords(self.scorecounter,self.canvas.winfo_width()-20,self.canvas.winfo_height()-20)
            time.sleep(0.25)
            counter += 1
            if counter >= 10:
                counter = 0
                self.hexes.append(self.canvas.create_text(random.randint(20,self.root.winfo_width()-20),0,font=(12),text=str(hex(random.randint(1,255)).split('x')[-1])))
            for i in self.hexes:
                try:
                    if self.canvas.coords(i)[1] >= self.root.winfo_height()-20:
                        self.canvas.delete(i)
                        messagebox.showinfo("info","game over")
                        self.root.destroy()
                except:
                    pass
                if self.selected_hex == self.canvas.itemcget(i,'text'):
                    self.canvas.moveto(self.portal,self.canvas.coords(i)[0]-20,self.canvas.coords(i)[1]) 
                    self.send_buffer = self.canvas.itemcget(i,'text').encode()
                    self.canvas.delete(i)
                    for i in self.bttns:
                        self.bttns[i]["text"] = "0"
                        self.bttns[i]["bg"] = self.default_colour
                    time.sleep(1)
                    self.canvas.moveto(self.portal,-100,-100)
                    self.canvas.itemconfig(self.scorecounter,text = (int(self.canvas.itemcget(self.scorecounter,'text')) + 1))

                self.canvas.move(i,0,4)
    def number_keys(self, keys):
        try:
            self.bits(bit=str(2**(8-(int(keys.char)))))
        except:
            pass
    def networking(self):
        self.send_buffer = b"_"
        server = socket.socket()
        server.connect(("86.160.112.14",8000))
        print("connected to server")
        server.recv(4096)
        print("opponent connected")
        server.sendall(b"_")
        send_buffer = b"_"
        while True:
            time.sleep(0.1)
            recv_buffer = server.recv(4096)
            if not recv_buffer == b"_":
                print(recv_buffer.decode())
                self.hexes.append(self.canvas.create_text(random.randint(10,self.root.winfo_width()-10),0,font=(12),text=recv_buffer.decode()))
            send_buffer = self.send_buffer
            server.sendall(send_buffer)
            self.send_buffer = b"_"            
        
main()
