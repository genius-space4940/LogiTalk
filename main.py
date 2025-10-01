from customtkinter import *
from socket import *
import threading

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Logitalk")
        self.label = None

        self.left_frame = CTkFrame(self, width=30, height=300)
        self.left_frame.pack_propagate(False)
        self.left_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -5

        self.button = CTkButton(self, text='▶️', command=self.toogle_show_menu, width=30)
        self.button.place(x=0, y=0)

        self.chat_field = CTkTextbox(self, width=400, height=260, corner_radius=10)
        self.chat_field.place(x=0, y=0)

        self.label_name = CTkLabel(self.left_frame, text="Ваше ім'я:")
        self.label_name.pack(pady=30)

        self.entry_name = CTkEntry(self.left_frame, fg_color="darkgray")
        self.entry_name.pack()

        self.theme = CTkOptionMenu(self.left_frame, values=["dark", 'light'], command=self.change_theme)
        self.theme.pack(side="bottom", pady=20)

        self.entry_message = CTkEntry(self, placeholder_text="Введіть повідомлення:", fg_color="darkgray", height=40, width=360)
        self.entry_message.place(x=0, y=260)

        self.send = CTkButton(self, text=">", height=40, width=40, command=self.send_message)
        self.send.place(x=0, y=0)
        
        self.username = "Stepan"

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 8888))
            hello_msg = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лася), до чату!\n"
            self.sock.send(hello_msg.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитися до сервера: {e}")

        self.adaptive.ui()

    def toggle_show_menu(self):     
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.button.configure(text="▶️")
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.button.configure(text="◀️")
            self.show_menu()
            self.label = CTkLabel(self.left_frame, text="Ім'я")
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.left_frame)
            self.entry.pack()

    def show_menu(self):
        self.left_frame.configure(width=self.left_frame.winfo_width() + self.speed_animate_menu)
        if not self.left_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.left_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.label and self.entry:
                self.label.destroy()
                self.entry.destroy()

    def adaptive_ui(self):
        self.left_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.left_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.left_frame.winfo_width(),
                                  height=self.winfo_height() - 40)
        self.send.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)
        self.entry_message.place(x=self.left_frame.winfo_width(), y=self.send.winfo_y())
        self.entry_message.configure(width=self.winfo_width() - self.left_frame.winfo_width() - self.send.winfo_width())

        self.after(50, self.adaptive_ui)

    def change_theme(self, value):
        set_appearance_mode(value)
            
    #додати повідомлення
    def add_message(self, text):
        self.chat_field.configure(state='normal')
        self.chat_field.insert(END, f"Я: {text} \n")
        self.chat_field.configure(state="disable")
        
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
