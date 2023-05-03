import base64
import os.path
import argon2
from PIL import Image
import customtkinter as ctk
from Database import Database
from Notification import Notification


class NewDatabase(ctk.CTkToplevel):
    def __init__(self, width, height, controller, *args, **kwargs):
        # main window settings
        super().__init__(*args, **kwargs, fg_color="#480900")
        self.scr_width = self.winfo_screenwidth()
        self.scr_height = self.winfo_screenheight()
        self.controller = controller
        x = int((self.scr_width - width) / 2)
        y = int((self.scr_height - height) / 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.title("Create new database")
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=4)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.resizable(False, False)

        # show/hide password images
        show = Image.open('./images/view.png')
        s_width, s_height = show.size
        hide = Image.open('./images/hide.png')
        dice = Image.open('./images/dice.png')
        d_width, d_height = dice.size


        # Notification
        self.notif = None
        self.isset_notif = False

        # Create new database label
        self.label = ctk.CTkLabel(self, text="Create new database",
                                  font=ctk.CTkFont(family='Helvetica', size=18, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, sticky="s", pady=(10, 10))
        self.label.focus_set()

        # Enter name
        self.enter_name = ctk.CTkLabel(self, text="Database name:")
        self.enter_name.grid(row=1, column=0, sticky="")

        # Name database entry
        self.name_entry = ctk.CTkEntry(self, width=170, show="",
                                       font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.name_entry.grid(row=1, column=1, sticky="", padx=(0,72))

        # Enter password
        self.enter_master_pass = ctk.CTkLabel(self, text="Master password:")
        self.enter_master_pass.grid(row=2, column=0, sticky="",)

        # User password entry
        self.master_show_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.master_show_frame.grid(row=2, column=1, sticky="e", padx=(0, 0))

        self.master_pass_entry = ctk.CTkEntry(self.master_show_frame, width=170, show="•",
                                              font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.master_pass_entry.grid(row=0, column=0, sticky="")

        s_width_ = int(s_width / (s_height / self.master_pass_entry.winfo_reqheight()) * 0.75)
        s_height_ = int(s_height / (s_height / self.master_pass_entry.winfo_reqheight()) * 0.75)
        self.Show_ = ctk.CTkImage(light_image=show, dark_image=show, size=(s_width_, s_height_))
        self.Hide_ = ctk.CTkImage(light_image=hide, dark_image=hide, size=(s_width_, s_height_))
        self.show_ = ctk.CTkButton(master=self.master_show_frame, width=0, fg_color="transparent", image=self.Show_,
                                   text="", hover=False, cursor="hand2",
                                   command=lambda: self.show_hide_pass(self.show_, self.master_pass_entry))
        self.show_.grid(row=0, column=1)

        d_width_ = int(d_width / (d_height / self.master_pass_entry.winfo_reqheight()) * 0.75)
        d_height_ = int(d_height / (d_height / self.master_pass_entry.winfo_reqheight()) * 0.75)
        self.Dice_ = ctk.CTkImage(light_image=dice, dark_image=dice, size=(d_width_, d_height_))
        self.dice_ = ctk.CTkButton(master=self.master_show_frame, width=0, fg_color="transparent", image=self.Dice_,
                                   text="", hover=False, cursor="hand2", command=self.controller.open_pass_gen)
        self.dice_.grid(row=0, column=2)

        # Enter password label
        self.first_pass_label = ctk.CTkLabel(self, text="First password (optional):",
                                             font=ctk.CTkFont(family='Helvetica', size=18, weight="bold"))
        self.first_pass_label.grid(row=3, column=0, columnspan=2, sticky="s", pady=(10, 10))

        # Enter title
        self.enter_title = ctk.CTkLabel(self, text="Title:")
        self.enter_title.grid(row=4, column=0, sticky="")

        # Name entry
        self.title_entry = ctk.CTkEntry(self, width=170, show="",
                                        font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.title_entry.grid(row=4, column=1, sticky="", padx=(0,72))

        # Enter login
        self.login_name = ctk.CTkLabel(self, text="Login:")
        self.login_name.grid(row=5, column=0, sticky="")

        # User login entry
        self.login_entry = ctk.CTkEntry(self, width=170, show="",
                                        font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.login_entry.grid(row=5, column=1, sticky="", padx=(0,72))

        # Enter password
        self.pass_name = ctk.CTkLabel(self, text="Password:")
        self.pass_name.grid(row=6, column=0, sticky="")

        # User password entry
        self.pass_entbut_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_entbut_frame.grid(row=6, column=1, sticky="e")

        self.pass_entry = ctk.CTkEntry(self.pass_entbut_frame, width=170, show="•",
                                       font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.pass_entry.grid(row=0, column=0, sticky="")

        d_width = int(d_width / (d_height / self.pass_entry.winfo_reqheight()) * 0.75)
        d_height = int(d_height / (d_height / self.pass_entry.winfo_reqheight()) * 0.75)
        self.Dice = ctk.CTkImage(light_image=dice, dark_image=dice, size=(d_width, d_height))
        self.dice = ctk.CTkButton(master=self.pass_entbut_frame, width=0, fg_color="transparent", image=self.Dice,
                                  text="", hover=False, cursor="hand2", command=self.controller.open_pass_gen)
        self.dice.grid(row=0, column=2)

        s_width = int(s_width / (s_height / self.pass_entry.winfo_reqheight()) * 0.75)
        s_height = int(s_height / (s_height / self.pass_entry.winfo_reqheight()) * 0.75)
        self.Show = ctk.CTkImage(light_image=show, dark_image=show, size=(s_width, s_height))
        self.Hide = ctk.CTkImage(light_image=hide, dark_image=hide, size=(s_width, s_height))
        self.show = ctk.CTkButton(master=self.pass_entbut_frame, width=0, fg_color="transparent", image=self.Show,
                                  text="", hover=False, cursor="hand2",
                                  command=lambda: self.show_hide_pass(self.show, self.pass_entry))
        self.show.grid(row=0, column=1)

        # Enter url
        self.url_name = ctk.CTkLabel(self, text="Url/App:")
        self.url_name.grid(row=7, column=0, sticky="")

        # User url entry
        self.url_entry = ctk.CTkEntry(self, width=170, show="",
                                      font=ctk.CTkFont(family="Bahnschrift SemiLight", size=14))
        self.url_entry.grid(row=7, column=1, sticky="", padx=(0,72))

        # Enter folder
        self.folder_name = ctk.CTkLabel(self, text="Category:")
        self.folder_name.grid(row=8, column=0, sticky="")

        # User folder entry
        self.folder_entry = ctk.CTkEntry(self, width=170, show="",
                                         font=ctk.CTkFont(family="Bahnschrift SemiLight", size=14))
        self.folder_entry.grid(row=8, column=1, sticky="", padx=(0,72))

        # [Button] Create new database
        self.cr_entry = ctk.CTkButton(master=self, text="Create new database", cursor="hand2", fg_color="#1a0300",
                                      hover_color="#2f0b04",
                                      command=lambda: self.create_database(self.name_entry.get(),
                                                                           self.master_pass_entry.get().encode(),
                                                                           self.title_entry.get(),
                                                                           self.login_entry.get(),
                                                                           self.pass_entry.get(),
                                                                           self.url_entry.get(),
                                                                           self.folder_entry.get()))
        self.bind("<Return>", lambda tmp: self.create_database(self.name_entry.get(),
                                                               self.master_pass_entry.get().encode(),
                                                               self.title_entry.get(),
                                                               self.login_entry.get(),
                                                               self.pass_entry.get(),
                                                               self.url_entry.get(),
                                                               self.folder_entry.get()))
        self.cr_entry.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=(20, 20), pady=(10, 10))

    def create_database(self, file_name, m_password, title, login, password, url, folder):
        if os.path.exists(file_name + ".pass"):
            self.popup_noti()
            return

        print("Creating a database")
        open(file_name + ".pass", "w").close()

        entered_password_key = base64.urlsafe_b64encode(argon2.hash_password_raw(
            time_cost=16, memory_cost=2 ** 15, parallelism=2, hash_len=32,
            password=bytes(m_password), salt=b'some salt', type=argon2.low_level.Type.ID))
        x = Database(file_name + ".pass", entered_password_key)
        if folder != "" or title != "" or login != "" or password != "" or url != "":
            if folder == "":
                folder = "Other"
            x.add_password(folder, title, login, password, url)

        print(f'File "{file_name}" created successfully!')

        self.controller.delete_frame("Start")
        self.controller.add_start_frame()
        self.destroy()

    def popup_noti(self):
        if self.isset_notif:
            self.notif.destroy()
            self.isset_notif = False
        self.notif = Notification(self, "This database already exists!", self.winfo_width())
        self.isset_notif = True

    def show_hide_pass(self, show, entry):
        if show.cget("image").cget("light_image").filename == "./images/view.png":
            show.configure(image=self.Hide)
            entry.configure(show="")
        else:
            show.configure(image=self.Show)
            entry.configure(show="•")
