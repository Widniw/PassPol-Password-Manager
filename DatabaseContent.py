import customtkinter as ctk
from Folder import Folder
from Notification import Notification
from NewPassword import NewPassword
from EditEntry import EditEntry


def butt_checked(button):
    if button.cget("fg_color") == "#3d0800":
        # button is not chosen so we change it upon clicking it to chosen
        button.configure(fg_color="#053225")
        button.configure(hover_color="#04251C")
    else:
        # button is chosen so we change it upon clicking it to not chosen
        button.configure(fg_color="#3d0800")
        button.configure(hover_color="#4d0a00")


class DatabaseContent(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        self.controller = controller
        self.db = db
        title = '.'.join(list(str.split(self.db.file, ".")[0:-1]))
        self.controller.title(title.split("/")[-1])

        ctk.CTkFrame.__init__(self, parent, fg_color="#480900")
        self.scr_width = self.winfo_screenwidth()
        self.scr_height = self.winfo_screenheight()
        self.width = self.scr_width / 1.4
        self.height = self.scr_height / 1.4
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # folder that's open at the moment
        self.open_folder = None

        # Open new password window
        self.new_password = None
        self.edit_password = None

        # Notification
        self.notif = None
        self.isset_notif = False

        # top menu frame
        self.menu = ctk.CTkFrame(self, fg_color="transparent")
        self.menu.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.menu.grid_columnconfigure((0, 1, 2), weight=1)
        self.menu.grid_rowconfigure(0, weight=1)

        # [Button] Go to the start page
        self.back_button = ctk.CTkButton(self.menu, text="Start page", command=self.start_page, height=50,
                                         fg_color="#053225", hover_color="#04251C")
        self.back_button.grid(row=0, column=0, pady=(30, 30))

        # [Button] Open password generator button
        self.passwd_gen = ctk.CTkButton(master=self.menu, text="Generate Password", cursor="hand2", fg_color="#1a0300",
                                        hover_color="#2f0b04", command=self.controller.open_pass_gen, height=50)
        self.passwd_gen.grid(row=0, column=1)

        # [Button] Add New password
        self.passwd = ctk.CTkButton(master=self.menu, text="New password", cursor="hand2", fg_color="#1a0300",
                                    hover_color="#2f0b04", command=self.open_new_password, height=50)
        self.passwd.grid(row=0, column=2)

        # container in which we show content of a folder
        self.container = ctk.CTkScrollableFrame(self, fg_color="#660e00", scrollbar_button_color="#3d0800",
                                                scrollbar_button_hover_color="#4d0a00")
        self.container.grid(row=1, column=1, sticky="nsew", pady=(0, 10), padx=(0, 10))
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # column containing folders - buttons that correspond to them
        self.column = ctk.CTkScrollableFrame(self, width=200, fg_color="#660e00", scrollbar_button_color="#660e00",
                                             scrollbar_button_hover_color="#660e00")
        self.column.grid(row=1, column=0, sticky="nsew", padx=(10, 10), pady=(0, 10))
        self.column.grid_columnconfigure(0, weight=1)

        # dictionary for frames (folder contents)
        self.folders = {}

        # i guess we need a dictionary of buttons :(((
        self.buttons = {}

        self.create_folders()
        if self.folders != {}:
            self.show_frame(list(self.folders.keys())[0])
            self.open_folder = list(self.folders.keys())[0]

    def show_frame(self, folder_):
        if self.open_folder is not None:
            butt_checked(self.buttons[self.open_folder])
        frame = self.folders[folder_]
        self.open_folder = folder_
        butt_checked(self.buttons[self.open_folder])
        frame.tkraise()

    def create_folders(self):
        self.folders = {}
        self.open_folder = None
        for widget in self.column.winfo_children():
            widget.destroy()
        folder_count = 0
        choose_folder = None
        for folder, ids in self.db.password_dict.items():
            if self.db.password_dict[folder] != "":
                choose_folder = ctk.CTkButton(self.column, text=folder,
                                              command=lambda fold=folder: self.show_frame(fold),
                                              fg_color="#3d0800", hover_color="#4d0a00")
                self.buttons[folder] = choose_folder
                choose_folder.grid(row=folder_count, column=0, padx=(10, 2), pady=(5, 0), sticky="nsew")
                folder_count += 1
                self.folders[folder] = Folder(parent=self.container, controller=self, folder=[folder, ids])
                self.folders[folder].grid(row=0, column=0, sticky="nsew")

        if choose_folder is not None:
            self.column.configure(width=choose_folder.winfo_reqwidth() + 15)

    def start_page(self):
        self.folders.clear()  # deletes folders so to not create new ones every time
        self.buttons.clear()  # deletes buttons so to not create new ones every time
        self.controller.go_to_start_page(self.db.file)

    def popup_noti(self, opt, title):
        if self.isset_notif:
            self.notif.destroy()
            self.isset_notif = False
        self.notif = Notification(self, f'Copied {opt} from {title}', self.winfo_width())
        self.isset_notif = True

    def delete_record_and_reload(self, folder, id_):
        self.db.delete_record(folder, id_)
        self.create_folders()

        if folder not in self.folders:
            if self.folders == {}:
                for widget in self.container.winfo_children():
                    widget.destroy()
                return
            try:
                self.show_frame(list(self.folders.keys())[0])
            except IndexError:
                pass
            return

        self.show_frame(folder)

    def edit_record_and_reload(self, folder):

        self.create_folders()
        self.show_frame(folder)

    def open_new_password(self):
        if self.new_password is None or not self.new_password.winfo_exists():
            self.new_password = NewPassword(400, 400, self.db, controller=self)
        else:
            self.new_password.focus_set()
        self.new_password.grab_set()

    def edit_password_record(self, folder, id_):
        if self.edit_password is None or not self.edit_password.winfo_exists():
            self.edit_password = EditEntry(width=400, height=400, database=self.db, controller=self, id_=id_,
                                           folder=folder)
        else:
            self.edit_password.focus_set()
        self.edit_password.grab_set()
