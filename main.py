from customtkinter import *
import socket
import threading

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Logitalk")

        self.left_frame = CTkFrame(self, width=200, height=260)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=0)
        self.left_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.width_left_frame = 0

        self.label = CTkLabel(self.left_frame, text="Ваше ім'я:")
        self.label.pack(pady=30)

        self.entry_name = CTkEntry(self.left_frame, fg_color="darkgray")
        self.entry_name.pack()

        self.theme = CTkOptionMenu(self.left_frame, values=["dark", 'light'], command=self.change_theme)
        self.theme.pack(side="bottom", pady=20)
        
        self.field = CTkTextbox(self, width=400, height=260, corner_radius=10)
        self.field.place(x=0, y=0)

        self.button = CTkButton(self, text="▷", width=30, command=self.show_menu)
        self.button.place(x=0, y=0)

        self.entry_message = CTkEntry(self, placeholder_text="Введіть повідомлення:", fg_color="darkgray", height=40, width=360)
        self.entry_message.place(x=0, y=260)

        self.send = CTkButton(self, text="▷", height=40, width=40)
        self.send.place(x=360, y=260)

    def show_menu(self):
        if self.is_show_menu == True:
            self.is_show_menu = False
            self.left_frame.configure(width=0)
            self.field.configure(width=400)
            self.field.place(x=0, y=0)
            self.button.configure(text=">")
        else:
            self.is_show_menu = True
            self.left_frame.configure(width=200)
            self.field.configure(width=200)
            self.field.place(x=200, y=0)
            self.button.configure(text="<")

    def change_theme(self, value):
        set_appearance_mode(value)
            
    #додати повідомлення
    def add_message(self, text):
        self.field.configure(state='normal')
        self.field.insert(END, f"Я: {text} \n")
        self.field.configure(state="disable")
        
    #надіслати повідомлення
        
    #отримати повідомлення

window = MainWindow()
window.mainloop()
