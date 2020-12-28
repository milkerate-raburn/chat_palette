#coding utf-8
import requests, json
import sys

import tkinter
import tkinter as tk
from tkinter import messagebox

class Webhook_Connecter:
    webhook_url : str
    username    : str
    headers = {'Content-Type': 'application/json'}

    @property
    def canPost(self):
        return not (self.webhook_url == None or self.username == None or
                    self.webhook_url == "" or self.username == "")

    def post(self,text:str):
        if not self.canPost:
            return
        main_content = {
                            'username':self.username,
                            'content':text}
        response = requests.post(self.webhook_url, json.dumps(main_content), headers=self.headers)
        print(response)


class MultiInputWindow(tk.Frame):
    def __init__(self, master, username:str, webhook:str):
        super().__init__(master)
        self.pack()
        self.username = tk.StringVar() 
        self.username.set(username)
        self.webhook = tk.StringVar()
        self.webhook.set(webhook)
        self.initUI()

    def initUI(self):
        self.master.title('環境設定')
        self.pack(fill=tk.BOTH)

        frame1 = tk.Frame(self)
        frame1.pack()

        label1 = tk.Label(frame1 , text='名前', width=6)
        label1.grid(row=0,column=0, padx=5,pady=10)

        self.entry1 = tk.Entry(frame1,textvariable=self.username)
        self.entry1.grid(row=0,column=1, padx=5,pady=10)

        frame2 = tk.Frame(self)
        frame2.pack()

        label2 = tk.Label(frame2 , text='webhook', width=6)
        label2.pack(side=tk.LEFT, padx=5,pady=10)

        self.entry2 = tk.Entry(frame2,textvariable=self.webhook)
        self.entry2.pack(fill=tk.X, padx=5,pady=10)

        frame3 = tk.Frame(self)
        frame3.pack()

        btn = tk.Button(frame3,text="決定",command=self.onSubmit)
        btn.pack(padx=5,pady=10)

    def onSubmit(self):
        if self.entry1.get() == "":
            #popup
            messagebox.showinfo('未入力', 'なまえない')
            return
        elif self.entry2.get() == "": 
            tk.messagebox.showinfo('未入力', 'webhookない')
            return
        else:
            self.output_username =  self.entry1.get()
            self.output_webhook =  self.entry2.get()
            self.quit()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.initInfo()
        self.pack()
        self.create_menu()
        self.create_widgets(master)

        
    def initInfo(self):
        self.WC = Webhook_Connecter()
        self.WC.username=""
        self.WC.webhook_url=""

    def create_widgets(self, master):
        main_frame = tk.Frame(master=master)
        main_frame.pack(expand = True, fill = tk.BOTH)
        self.main_frame = main_frame

        add_frame = tk.Frame(main_frame)
        add_frame.pack(anchor=tk.N,side=tk.TOP,expand = True, fill = tk.X)
        
        self.add_text = tk.StringVar()
        add_Entry = tk.Entry(add_frame,textvariable=self.add_text)
        add_Entry.pack(side=tk.LEFT,fill=tk.X,expand=True, padx=5,pady=10)

        add_button = tk.Button(add_frame,text="追加",command=self.add_palette)
        add_button.pack(side=tk.RIGHT, padx=5,pady=10)

        self.palette_frame = tk.Frame(main_frame)
        self.palette_frame.pack(expand = True, fill = tk.BOTH)

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        sub_menu = tk.Menu(menu,tearoff=False)
        menu.add_cascade(label='ファイル',menu=sub_menu)
        sub_menu.add_command(label='環境設定',command=self.set_environment)

    def set_environment(self):
        print('環境設定クリック')
        self.child_window=tk.Toplevel()
        app = MultiInputWindow(self.child_window, self.WC.username,self.WC.webhook_url)
        app.mainloop()
        self.WC.username = app.output_username
        self.WC.webhook_url = app.output_webhook
        print(f"usr:{self.WC.username},wh:{self.WC.webhook_url}")
        self.child_window.destroy()

    def add_palette(self):
        txt = self.add_text.get()
        if not txt == "":
            b = tk.Button(self.palette_frame,text=txt,command=lambda:self.send(txt),bg='gray',fg='white',padx=5,pady=5)
            b.pack(expand = True, fill = tk.BOTH,padx=5,pady=5)
        else:
            print("テキスト空じゃん")

    def send(self,txt):
        print(f"send {txt}")
        if self.WC.canPost:
            try:
                self.WC.post(txt)
            except Exception:
                messagebox.showerror('送信失敗','環境設定あってるか？')
        else:
            messagebox.showinfo('環境未設定','環境設定しろ')
        

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("chat palette")
    app = Application(master=root)
    app.mainloop()
    sys.exit()
    '''
    WC = Webhook_Connecter()
    WC.username = 'てすたろう'
    WC.webhook_url = 'https://discord.com/api/webhooks/791560486801637408/C0CTbmdgjseyKy9N3U0luzFLCxexeu_68uPI0dQZ-K4d1wlMIyhTdMJ9L7GGWZygSAT_'

    WC.post('help')
    '''