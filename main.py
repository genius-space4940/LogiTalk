from customtkinter import *

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Logitalk")

        self.left_frame = CTkFrame(self, width=self.winfo_width()/2, height=self.winfo_height(), fg_color="black")
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=0)
        self.left_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.width_left_frame = 0

        self.label = CTkLabel(self.left_frame, text="Ваше ім'я:", text_color="white")
        self.label.pack(pady=30)

        self.entry_name = CTkEntry(self.left_frame, fg_color="darkgray")
        self.entry_name.pack()

        self.theme = CTkOptionMenu(self.left_frame, values=["dark", 'light'], command=self.change_theme)
        self.theme.pack(side="bottom", pady=20)

        self.button = CTkButton(self, text="▷", width=30, command=self.show_menu)
        self.button.place(x=0, y=0)
        
        self.field = CTkScrollableFrame(self, width=380)
        self.field.place(x=0, y=30)

        self.entry_message = CTkEntry(self, placeholder_text="Введіть повідомлення:", fg_color="darkgray", height=40, width=360)
        self.entry_message.place(x=0, y=260)

        self.send = CTkButton(self, text="▷", height=40, width=40)
        self.send.place(x=360, y=260)

    def show_menu(self):
        if self.is_show_menu == True:
            self.left_frame.pack_propagate(False)
            self.button.place(x=0, y=0)
            self.is_show_menu = False
        else:
            self.left_frame.pack_propagate(True)
            self.button.place(x=0, y=0)
            self.is_show_menu = True

    def change_theme(self, value):
        if self.value == "dark":
            set_appeareance_mode = 'dark'
        
        elif self.value == "light":
            set_appeareance_mode = 'light'

    def adaptation_ui(self):
        pass
        # if self.is_show_menu == True:
            

window = MainWindow()
window.mainloop()
