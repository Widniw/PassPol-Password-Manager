import os
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog


class Start(ctk.CTkFrame):
    def __init__(self, parent, controller, wind_width, wind_height):
        ctk.CTkFrame.__init__(self, parent, fg_color="#480900")
        self.controller = controller
        self.width = wind_width
        self.height = wind_height
        # dynamically change size depending on screen size;
        self.y_scale = self.height / 10
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # logo settings
        im = Image.open('./images/PassPol.png')
        width, height = im.size
        width = int(width * (self.y_scale * 1.5 / height))
        height = self.y_scale * 1.5
        Logo = ctk.CTkImage(light_image=im, dark_image=im, size=(width, height))

        self.logo = ctk.CTkButton(master=self, image=Logo, text="", fg_color="transparent", state="disabled")
        self.logo.grid(row=0, column=0, columnspan=3, pady=(10, 10))

        self.frame = ctk.CTkFrame(master=self, height=self.y_scale * 6, width=self.width, fg_color="#480900")
        self.frame.grid(row=1, columnspan=3)
        self.frame.grid_rowconfigure((0, 1), weight=0)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_propagate(True)

        # "choose database" text settings
        self.choose = ctk.CTkLabel(master=self.frame, text="Choose password database: ",
                                   font=ctk.CTkFont(family="Bahnschrift SemiLight", size=27), text_color="#e8cca8")
        self.font_height = ctk.CTkFont(family="Calibri", size=27).metrics('linespace')
        self.choose.grid(row=0)

        # frame with databases - settings
        self.scroll_frame = ctk.CTkScrollableFrame(master=self.frame, width=int(self.width * 0.75),
                                                   height=(self.y_scale * 6 - self.font_height - 20),
                                                   fg_color="#660e00", scrollbar_button_color="#3d0800",
                                                   scrollbar_button_hover_color="#4d0a00")

        self.scroll_frame.grid(row=1, column=0, pady=0)

        self.find_dbs()

        # [Button] Open external db
        self.open_external = ctk.CTkButton(master=self, text="Open external db", cursor="hand2", fg_color="#1a0300",
                                           hover_color="#2f0b04", command=self.open_file_exp)
        self.open_external.grid(row=2, column=0, sticky="nsew",
                                padx=(int(self.width / 4 - self.width * 0.15 / 4), 20), pady=(30, 30))

        # [Button] Create password db
        self.create_db = ctk.CTkButton(master=self, text="Create password db", cursor="hand2", fg_color="#1a0300",
                                       hover_color="#2f0b04", command=self.controller.open_new_database)
        self.create_db.grid(row=2, column=1, sticky="nsew", padx=(20, 20), pady=(30, 30))

        # [Button] Password Generator
        self.passwd = ctk.CTkButton(master=self, text="Generate Password", cursor="hand2", fg_color="#1a0300",
                                    hover_color="#2f0b04", command=self.controller.open_pass_gen)
        self.passwd.grid(row=2, column=2, sticky="nsew", padx=(20, int(self.width / 4 - self.width * 0.15 / 4)),
                         pady=(30, 30))

    # Search for databases to be presented on the start screen.
    def find_dbs(self):
        count = 0
        for file in os.listdir(os.getcwd()):
            if file.endswith(".pass"):
                name = file
                button = ctk.CTkButton(master=self.scroll_frame,
                                       text=name,
                                       fg_color="transparent",
                                       anchor="w",
                                       cursor="hand2",
                                       hover_color="#4d0a00",
                                       command=lambda name_tmp=name: self.controller.add_auth_frame(name_tmp))

                button.grid(row=count, column=0, pady=3, padx=3, sticky="w")
                count += 1

    # What happens when you click [Button] Open external database. It will open a window to pick a .pass file.
    def open_file_exp(self):
        file_path = filedialog.askopenfilename()
        if file_path.endswith(".pass"):
            self.controller.add_auth_frame(file_path)
        else:
            print("Please open a .pass db!")
