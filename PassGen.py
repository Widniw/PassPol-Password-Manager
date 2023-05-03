import customtkinter as ctk
import string
import secrets
import random
from PIL import Image
from Notification import Notification

# A-Z, a-z, 0-9, special
upp = string.ascii_uppercase
low = string.ascii_lowercase
dig = string.digits
spec = string.punctuation

# "category": [characters, status], where status means if chosen in menu
CONDITIONS = {
    "A-Z": [upp, 0],
    "a-z": [low, 0],
    "0-9": [dig, 0],
    "Special chars": [spec, 0]
}
# default password length, at start
length = 20


class PassGen(ctk.CTkToplevel):
    def __init__(self, width, height, *args, **kwargs):

        # main window settings
        super().__init__(*args, **kwargs, fg_color="#480900")
        self.scr_width = self.winfo_screenwidth()
        self.scr_height = self.winfo_screenheight()
        x = int(self.scr_width / 2 - width)
        y = int(self.scr_height / 2 - height)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.title("Password generator")
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # Notification - when password is copied to clipboard
        self.notif = None
        self.isset_notif = False

        # text box settings
        self.txt_box = ctk.CTkTextbox(master=self, width=int(width * 0.8), height=15, fg_color="#660e00",
                                      activate_scrollbars=False, wrap="none",
                                      font=ctk.CTkFont(family="Calibri", size=15))
        self.txt_box.grid(row=0, column=0, pady=(0, 20), sticky="se", padx=(10, 5))

        # Generate and copy buttons settings
        self.frame_gen_copy = ctk.CTkFrame(master=self, fg_color="transparent")
        self.frame_gen_copy.grid_rowconfigure(0, weight=1)
        self.frame_gen_copy.grid_columnconfigure((0, 1), weight=1)
        self.frame_gen_copy.grid(row=0, column=1, sticky="ws")

        # generate button - generating new passwords based on chosen settings
        gen = Image.open('./images/refresh.png')
        g_width = g_height = self.txt_box.cget("height")
        Gen = ctk.CTkImage(light_image=gen, dark_image=gen, size=(g_width, g_height))
        self.gen = ctk.CTkButton(master=self.frame_gen_copy, width=20, fg_color="#7A1000", image=Gen, text="",
                                 hover=False, cursor="hand2", command=self.generate)
        self.gen.grid(row=0, column=0, pady=(0, 23), padx=(0, 0))

        # copy button - copy password to clipboard
        cop = Image.open('./images/copy.png')
        c_width = c_height = self.txt_box.cget("height")
        Copy = ctk.CTkImage(light_image=cop, dark_image=cop, size=(c_width, c_height))
        self.copy = ctk.CTkButton(master=self.frame_gen_copy, width=20, fg_color="#7A1000", image=Copy, text="",
                                  hover=False,
                                  cursor="hand2", command=self.copy)
        self.copy.grid(row=0, column=2, pady=(0, 23), padx=(0, 10))

        # frame containing options settings
        self.options = ctk.CTkFrame(master=self, width=int(width * 0.85), height=int(height * 0.7),
                                    fg_color="#660e00")
        self.options.grid(row=1, column=0, columnspan=3, sticky="n", pady=(0, 0), padx=(10, 10))
        self.options.grid_propagate(False)
        self.options.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.options.grid_rowconfigure((0, 1), weight=1)

        self.txt_and_but = ctk.CTkFrame(self.options, fg_color="transparent")
        self.txt_and_but.grid_columnconfigure((0, 1), weight=1)
        self.txt_and_but.grid_rowconfigure(0, weight=1)
        self.txt_and_but.grid(row=0, column=0, columnspan=4, sticky="ns")

        # slider - length of password
        self.slider = ctk.CTkSlider(master=self.txt_and_but, width=int(self.options.winfo_reqwidth() * 0.9), from_=1,
                                    to=128, number_of_steps=127,
                                    command=self.slider_event, fg_color="#290b05", button_color="#04251C",
                                    button_hover_color="#02120E", progress_color="#084032")
        self.slider.set(length)  # ustawienie defaultowej dlugosci (length)
        self.slider.grid(row=0, column=0, columnspan=3, sticky="s", pady=(0, 5))

        # Length show and input
        self.inp = ctk.StringVar()
        self.inp.trace_add("write", self.on_write)
        self.inp.set(str(length))
        self.input = ctk.CTkEntry(master=self.txt_and_but, width=50, height=0,
                                  font=ctk.CTkFont(family="Calibri", size=15),
                                  textvariable=self.inp, fg_color="#7A1000", corner_radius=0, border_color="#520b00")
        self.input.grid(row=0, column=4, sticky="s")

        # Conditions buttons settings
        self.uppcase = ctk.CTkButton(master=self.options, text="A-Z", cursor="hand2", fg_color="#1a0300",
                                     corner_radius=0,
                                     hover_color="#290b05", command=lambda: self.butt_checked(self.uppcase))
        self.uppcase.grid(row=1, column=0, pady=(20, 0), sticky="n")
        # in order to see that you can click those buttons - and options is chosen right at the start of the program
        self.uppcase.configure(fg_color="#053225")
        self.uppcase.configure(hover_color="#04251C")
        CONDITIONS[self.uppcase.cget("text")][1] = 1
        self.generate()

        self.lowcase = ctk.CTkButton(master=self.options, text="a-z", cursor="hand2", fg_color="#3d0800",
                                     corner_radius=0,
                                     hover_color="#290b05", command=lambda: self.butt_checked(self.lowcase))
        self.lowcase.grid(row=1, column=1, pady=(20, 0), sticky="n")

        self.spec = ctk.CTkButton(master=self.options, text="Special chars", cursor="hand2", fg_color="#3d0800",
                                  corner_radius=0,
                                  hover_color="#290b05", command=lambda: self.butt_checked(self.spec))
        self.spec.grid(row=1, column=3, pady=(20, 0), sticky="n")

        self.dig = ctk.CTkButton(master=self.options, text="0-9", cursor="hand2", fg_color="#3d0800", corner_radius=0,
                                 hover_color="#290b05", command=lambda: self.butt_checked(self.dig))
        self.dig.grid(row=1, column=2, pady=(20, 0), sticky="n")

    # setting max 3 digit numbers as password length
    def on_write(self, *args):
        if len(self.inp.get()) > 3:
            self.inp.set(self.inp.get()[:3])
        else:
            try:
                global length
                length = int(self.inp.get())
                # slider can only reach to 128
                if length <= 128:
                    self.slider.set(length)
                else:
                    self.slider.set(128)
                self.generate()
            except ValueError:
                # if input is something different than a number
                self.inp.set("")

    # slider function - setting the length
    def slider_event(self, value):
        global length
        if length != value:
            length = int(value)
            self.inp.set(str(length))
            self.generate()

    # copying generated password to clipboard
    def copy(self):
        self.copy.clipboard_clear()
        self.copy.clipboard_append(self.txt_box.get("1.0", 'end-1c'))
        self.popup_noti()
        print("Copied password to clipboard!")

    # changing status of options buttons
    def butt_checked(self, button):
        if button.cget("fg_color") == "#3d0800":
            # button is not chosen so we change it upon clicking it to chosen
            button.configure(fg_color="#053225")
            button.configure(hover_color="#04251C")
            CONDITIONS[button.cget("text")][1] = 1
            self.generate()
        else:
            # button is chosen so we change it upon clicking it to not chosen
            button.configure(fg_color="#3d0800")
            button.configure(hover_color="#290b05")
            CONDITIONS[button.cget("text")][1] = 0
            self.generate()

    # generating password
    def generate(self):
        global length
        conditions = ''
        size = 0
        for cond in CONDITIONS:
            if CONDITIONS[cond][1] == 1:
                conditions += CONDITIONS[cond][0]
                size += 1
        pwd = ''
        while size:
            pwd = ''
            for _ in range(length):
                pwd += ''.join(secrets.choice(conditions))

            # at least one character from every chosen option needs to be in the password
            count = 0
            for cond in CONDITIONS:
                if CONDITIONS[cond][1] == 1:
                    if any(char in CONDITIONS[cond][0] for char in pwd):
                        count += 1
                    else:
                        break
            if count == size:
                pwd = list(pwd.split())
                random.shuffle(pwd)
                pwd = ''.join(pwd)
                break
            if length < 4:
                break
        self.txt_box.configure(state="normal")  # enable editing of the entry
        self.txt_box.delete("1.0", 'end-1c')  # delete previous password
        self.txt_box.insert("1.0", pwd)  # set entry with the new password
        self.txt_box.configure(state="disabled")  # disable editing of the entry

    # copying password to clipboard - notification function
    def popup_noti(self):
        if self.isset_notif:
            self.notif.destroy()
            self.isset_notif = False
        self.notif = Notification(self, "Password copied to clipboard!", self.winfo_width())
        self.isset_notif = True
