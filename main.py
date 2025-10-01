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
        self.speed_animate_menu = -5

        self.label_name = CTkLabel(self.left_frame, text="Ваше ім'я:")
        self.label_name.pack(pady=30)

        self.entry_name = CTkEntry(self.left_frame, fg_color="darkgray")
        self.entry_name.pack()

        self.theme = CTkOptionMenu(self.left_frame, values=["dark", 'light'], command=self.change_theme)
        self.theme.pack(side="bottom", pady=20)
        
        self.field = CTkTextbox(self, width=400, height=260, corner_radius=10)
        self.field.place(x=0, y=0)

        self.button = CTkButton(self, text=">", width=30, command=self.show_menu)
        self.button.place(x=0, y=0)

        self.entry_message = CTkEntry(self, placeholder_text="Введіть повідомлення:", fg_color="darkgray", height=40, width=360)
        self.entry_message.place(x=0, y=260)

        self.send = CTkButton(self, text=">", height=40, width=40)
        self.send.place(x=360, y=260)

    def show_menu(self):
        self.left_frame.configure(width=self.left_frame.winfo_width() + self.speed_animate_menu)
        if not self.left_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.left_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.label and self.entry:
                self.label.destroy()
                self.entry.destroy()

    def toggle_show_menu(self):     
        if self.is_show_menu == True:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.button.configure(text=">")
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.button.configure(text="<")
            self.show_menu()
            self.label = CTkLabel(self.left_frame, text="Ім'я")
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.left_frame)
            self.entry.pack()

    def change_theme(self, value):
        set_appearance_mode(value)
            
    #додати повідомлення
    def add_message(self, text):
        self.field.configure(state='normal')
        self.field.insert(END, f"Я: {text} \n")
        self.field.configure(state="disable")
        
    #надіслати повідомлення
    def send_message(self):
        get_message = self.entry_message.get()
        if get_message:
            self.add_message(f"{self.username}: {get_message}")
            data = f"{self.username}: {get_message} \n"

            try:
                self.client.sendall(data.encode())
            except:
                pass

            self.entry_message.delete(0, END)

    #отримати повідомлення
    def recv_message(self):
        buffer = ""

        while True:
            try:
                word = self.client.recv(4096)
                if not word:
                    break
                buffer += word.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
            except:
                break
            
        self.client.close()
    
    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]

        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]

                self.add_message(f"{author} надіслав(ла) зображення: {filename}")
            else:
                self.add_message(line)

window = MainWindow()
window.mainloop()
