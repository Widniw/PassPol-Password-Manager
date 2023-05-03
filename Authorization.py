import base64
import cryptography
import cryptography.fernet
import customtkinter as ctk
from PIL import Image
from Database import Database
from Notification import Notification
import argon2


class Authorization(ctk.CTkFrame):

    def __init__(self, parent, controller, db):
        ctk.CTkFrame.__init__(self, parent)
        self.db = db
        self.controller = controller
        self.grid_rowconfigure((1, 3), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # Notification - if we type in the wrong password
        self.notif = None
        self.isset_notif = False

        # Enter password label
        self.label = ctk.CTkLabel(self, text="Enter password for " + db.split("/")[-1] + ":", font=controller.title_font)
        self.label.grid(row=1, column=0, columnspan=2, sticky="s", pady=(0,30))

        # frame containing entry and show/hide pass button
        self.ent_but = ctk.CTkFrame(self, fg_color="transparent")
        self.ent_but.grid_columnconfigure((0,1), weight=1)
        self.ent_but.grid(row=2, column=0, columnspan=2)

        # User password entry
        self.entry = ctk.CTkEntry(self.ent_but, width=325, show="•", font=ctk.CTkFont(family="Bahnschrift SemiLight", size=18))
        self.entry.update()
        self.entry.grid(row=0, column=0)
        # In order to enter password with the "Enter" keyboard key
        self.entry.bind("<Return>", lambda tmp: self.check_password(self.entry.get().encode()))
        self.entry.focus_set()

        # show/hide password button
        show = Image.open('./images/view.png')
        hide = Image.open('./images/hide.png')
        s_width, s_height = show.size
        s_width = int(s_width / (s_height / self.entry.winfo_reqheight()) * 0.75)
        s_height = int(s_height / (s_height / self.entry.winfo_reqheight()) * 0.75)
        self.Show = ctk.CTkImage(light_image=show, dark_image=show, size=(s_width, s_height))
        self.Hide = ctk.CTkImage(light_image=hide, dark_image=hide, size=(s_width, s_height))
        self.show = ctk.CTkButton(master=self.ent_but, width=20, fg_color="transparent", image=self.Show, text="",
                                 hover=False, cursor="hand2", command=self.show_hide_pass)
        self.show.grid(row=0, column=1, sticky="es")

        # [Button] Go to the start page
        self.back_button = ctk.CTkButton(self, text="Go to the start page",
                               command=lambda: self.go_to_start_page(self.db))
        self.back_button.grid(row=3, column=0, sticky="ne", pady=(30, 0), padx=(0, 25))

        # [Button] Enter database
        self.enter_button = ctk.CTkButton(self, text="Enter database",
                               command=lambda: self.check_password(self.entry.get().encode()))
        self.enter_button.grid(row=3, column=1, sticky="nw", pady=(30, 0), padx=(25, 0))

    # Checks whether the password entered by the user is correct
    def check_password(self, entered_password):

        # Entered password is translated to a key
        entered_password_key = base64.urlsafe_b64encode(argon2.hash_password_raw(
            time_cost=16, memory_cost=2 ** 15, parallelism=2, hash_len=32,
            password=bytes(entered_password), salt=b'some salt', type=argon2.low_level.Type.ID))
        try:
            # If the wrong key is entered, load_file function from Database.__init__ will fail at Fernet.decrypt line
            # Invalid Token error.
            tmp = Database(self.db, entered_password_key)
        except cryptography.fernet.InvalidToken:
            self.popup_noti()
            return

        print("Password correct.")
        self.controller.add_database_content_frame(self.db, tmp)

    def go_to_start_page(self, page_name):
        self.controller.delete_frame(page_name)
        self.controller.show_frame("Start")

    def popup_noti(self):
        if self.isset_notif:
            self.notif.destroy()
            self.isset_notif = False
        self.notif = Notification(self, "Wrong password!", self.winfo_width())
        self.isset_notif = True

    def show_hide_pass(self):
        if self.show.cget("image").cget("light_image").filename == "./images/view.png":
            self.show.configure(image=self.Hide)
            self.entry.configure(show="")
        else:
            self.show.configure(image=self.Show)
            self.entry.configure(show="•")



