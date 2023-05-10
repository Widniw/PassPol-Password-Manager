from PIL import Image
import customtkinter as ctk


class EditEntry(ctk.CTkToplevel):
    def __init__(self, width, height, database, controller, id_, folder, *args, **kwargs):
        # main window settings
        super().__init__(*args, **kwargs, fg_color="#480900")
        self.scr_width = self.winfo_screenwidth()
        self.scr_height = self.winfo_screenheight()
        x = int((self.scr_width - width) / 2)
        y = int((self.scr_height - height) / 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.title("Edit password entry")
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)
        self.db = database
        self.controller = controller
        self.folder_name = folder
        self.id_ = id_

        # show/hide password images
        show = Image.open('./images/view.png')
        s_width, s_height = show.size
        hide = Image.open('./images/hide.png')
        dice = Image.open('./images/dice.png')
        d_width, d_height = dice.size

        # Enter password label
        self.first_pass_label = ctk.CTkLabel(self, text="Edit password entry",
                                             font=ctk.CTkFont(family='Helvetica', size=18, weight="bold"))
        self.first_pass_label.grid(row=0, column=0, columnspan=2, sticky="s", pady=(10, 10))

        # Enter title
        self.enter_title = ctk.CTkLabel(self, text="Title:")
        self.enter_title.grid(row=1, column=0, sticky="")

        # Name entry
        self.title_entry = ctk.CTkEntry(self, width=150, show="",
                                        font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.title_entry.insert(0, self.db.password_dict[self.folder_name][id_]["title"])
        self.title_entry.grid(row=1, column=1, sticky="", padx=(0, 80))

        # Enter login
        self.login_name = ctk.CTkLabel(self, text="Login:")
        self.login_name.grid(row=2, column=0, sticky="")

        # User password entry
        self.login_entry = ctk.CTkEntry(self, width=150, show="",
                                        font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.login_entry.insert(0, self.db.password_dict[self.folder_name][id_]["login"])
        self.login_entry.grid(row=2, column=1, sticky="", padx=(0, 80))

        # Enter password
        self.pass_name = ctk.CTkLabel(self, text="Password:")
        self.pass_name.grid(row=3, column=0, sticky="")

        # User password entry
        self.pass_show_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_show_frame.grid(row=3, column=1)

        self.pass_entry = ctk.CTkEntry(self.pass_show_frame, width=150, show="•",
                                       font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.pass_entry.insert(0, self.db.password_dict[self.folder_name][id_]["password"])
        self.pass_entry.grid(row=0, column=0, sticky="")

        s_width_ = int(s_width / (s_height / self.pass_entry.winfo_reqheight()) * 0.75)
        s_height_ = int(s_height / (s_height / self.pass_entry.winfo_reqheight()) * 0.75)
        self.Show = ctk.CTkImage(light_image=show, dark_image=show, size=(s_width_, s_height_))
        self.Hide = ctk.CTkImage(light_image=hide, dark_image=hide, size=(s_width_, s_height_))
        self.show = ctk.CTkButton(master=self.pass_show_frame, width=0, fg_color="transparent", image=self.Show,
                                  text="", hover=False, cursor="hand2",
                                  command=self.show_hide_pass)
        self.show.grid(row=0, column=1)

        d_width = int(d_width / (d_height / self.pass_entry.winfo_reqheight()) * 0.75)
        d_height = int(d_height / (d_height / self.pass_entry.winfo_reqheight()) * 0.75)
        self.Dice = ctk.CTkImage(light_image=dice, dark_image=dice, size=(d_width, d_height))
        self.dice = ctk.CTkButton(master=self.pass_show_frame, width=0, fg_color="transparent", image=self.Dice,
                                  text="", hover=False, cursor="hand2", command=lambda: (
            self.controller.controller.open_pass_gen(), self.controller.controller.pass_gen.focus_set()))
        self.dice.grid(row=0, column=2)

        # Enter url
        self.url_name = ctk.CTkLabel(self, text="Url/App:")
        self.url_name.grid(row=4, column=0, sticky="")

        # User url entry
        self.url_entry = ctk.CTkEntry(self, width=150, show="",
                                      font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13))
        self.url_entry.insert(0, self.db.password_dict[self.folder_name][id_]["url"])
        self.url_entry.grid(row=4, column=1, sticky="", padx=(0, 80))

        # [Button] Edit password
        self.edit_entry = ctk.CTkButton(master=self, text="Edit", cursor="hand2", fg_color="#1a0300",
                                        hover_color="#2f0b04",
                                        command=self.edit_pass)
        self.edit_entry.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=(20, 20), pady=(10, 10))
        # Binding the "Enter" key in order to add password when pressed
        self.bind("<Return>", lambda tmp: self.edit_pass())

    def show_hide_pass(self):
        if self.show.cget("image").cget("light_image").filename == "./images/view.png":
            self.show.configure(image=self.Hide)
            self.pass_entry.configure(show="")
        else:
            self.show.configure(image=self.Show)
            self.pass_entry.configure(show="•")

    def edit_pass(self):
        if (self.title_entry.get() != "" or self.login_entry.get() != ""
                or self.pass_entry.get() != "" or self.url_entry.get() != ""):
            self.db.password_dict[self.folder_name][self.id_]["title"] = self.title_entry.get()
            self.db.password_dict[self.folder_name][self.id_]["login"] = self.login_entry.get()
            self.db.password_dict[self.folder_name][self.id_]["password"] = self.pass_entry.get()
            self.db.password_dict[self.folder_name][self.id_]["url"] = self.url_entry.get()
            self.controller.create_folders()
            self.controller.show_frame(self.folder_name)
            self.db.save_file()
        self.destroy()
