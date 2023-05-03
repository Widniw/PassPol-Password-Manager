from functools import partial
from PIL import Image
import customtkinter as ctk


def color_on_hover(widget, color, event):
    widget.configure(fg_color=color)


class Folder(ctk.CTkFrame):
    def __init__(self, parent, controller, folder):
        ctk.CTkFrame.__init__(self, parent, fg_color="transparent")
        self.grid_columnconfigure((0, 1), weight=1)
        self.controller = controller
        self.folder_name = folder[0]
        self.ids = folder[1]
        self.display_entries()

    def display_entries(self):
        # key logo, size
        cop = Image.open('./images/passwd.png')
        c_width, c_height = cop.size

        # login logo, size
        log = Image.open('./images/login.png')
        l_width, l_height = log.size

        # delete logo, size
        delete_icon = Image.open('./images/delete.png')
        d_width, d_height = delete_icon.size

        # edit logo, size
        edit = Image.open('./images/edit.png')
        e_width, e_height = edit.size
        try:
            for id_, entry in self.ids.items():
                # frame in which we pack the Title and Login of the entry
                entry_frame = ctk.CTkFrame(self, height=70, fg_color="#5a0b00")
                entry_frame.grid_columnconfigure((0, 1), weight=1)
                entry_frame.grid_rowconfigure((0, 1), weight=1)
                # So that one record frame does not shrink to its data.
                entry_frame.grid_propagate(False)
                # binding function in order to change hover color of the entry frame
                entry_frame.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                entry_frame.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                entry_frame.grid(row=id_, sticky="nsew", pady=(0, 5), columnspan=2)

                # the Title of the entry
                title_label = ctk.CTkLabel(master=entry_frame, text=entry["title"],
                                           font=ctk.CTkFont(family="Bahnschrift SemiLight", size=18))
                # binding function in order to change hover color of the frame
                title_label.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                title_label.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                title_label.grid(row=0, column=0, padx=(10, 10), sticky="ws")

                # the URL of the entry
                login_label = ctk.CTkLabel(master=entry_frame, text=entry["url"],
                                           font=ctk.CTkFont(family="Bahnschrift SemiLight", size=13),
                                           text_color="#ff9180")
                # binding function in order to change hover color of the frame
                login_label.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                login_label.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                login_label.grid(row=1, column=0, padx=(10, 10), sticky="wn")

                # [Button] Copy login
                l_width = int(l_width / (l_height / entry_frame.cget("height")) / 2.25)
                l_height = int(l_height / (l_height / entry_frame.cget("height")) / 2.25)
                Login = ctk.CTkImage(light_image=log,
                                     dark_image=log, size=(l_width, l_height))
                login = ctk.CTkButton(master=entry_frame, width=l_width, height=l_height, fg_color="transparent",
                                      image=Login, text="", hover=False, cursor="hand2",
                                      command=lambda log_=entry["login"], t=title_label.cget("text"),
                                                     op="login": self.copy(log_, t, op))
                # binding function in order to change hover color of the frame
                login.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                login.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                login.grid(row=0, column=1, rowspan=2, sticky="nse", padx=(5, 5))

                # [Button] Copy password
                c_width = int(c_width / (c_height / entry_frame.cget("height")) / 2.5)
                c_height = int(c_height / (c_height / entry_frame.cget("height")) / 2.5)
                Copy = ctk.CTkImage(light_image=cop,
                                    dark_image=cop, size=(c_width, c_height))
                copy = ctk.CTkButton(master=entry_frame, width=c_width, height=c_height, fg_color="transparent",
                                     image=Copy,
                                     text="",
                                     hover=False, cursor="hand2",
                                     command=lambda passwd=entry["password"], t=title_label.cget("text"),
                                                    op="pass": self.copy(passwd, t, op))

                # binding function in order to change hover color of the frame
                copy.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                copy.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                copy.grid(row=0, column=2, rowspan=2, sticky="nse", padx=(5, 5))

                # [Button] Edit password
                e_width = int(e_width / (e_height / entry_frame.cget("height")) / 3)
                e_height = int(e_height / (e_height / entry_frame.cget("height")) / 3)
                edit_image = ctk.CTkImage(light_image=edit,
                                          dark_image=edit, size=(e_width, e_height))
                edit_button = ctk.CTkButton(master=entry_frame, width=e_width, height=e_height, fg_color="transparent",
                                            image=edit_image,
                                            text="",
                                            hover=False, cursor="hand2",
                                            command=lambda ID=id_: self.controller.edit_password_record(
                                                self.folder_name, ID))

                # binding function in order to change hover color of the frame
                edit_button.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                edit_button.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                edit_button.grid(row=0, column=3, rowspan=2, sticky="nse", padx=(5, 5))

                # [Button] Delete password
                d_width = int(d_width / (d_height / entry_frame.cget("height")) / 3.5)
                d_height = int(d_height / (d_height / entry_frame.cget("height")) / 3.5)
                delete_image = ctk.CTkImage(light_image=delete_icon,
                                            dark_image=delete_icon, size=(d_width, d_height))
                delete_button = ctk.CTkButton(master=entry_frame, width=d_width, height=d_height,
                                              fg_color="transparent",
                                              image=delete_image,
                                              text="",
                                              hover=False, cursor="hand2",
                                              command=lambda tmpid=id_: self.controller.delete_record_and_reload(
                                                  self.folder_name, tmpid))

                # binding function in order to change hover color of the frame
                delete_button.bind("<Enter>", partial(color_on_hover, entry_frame, "#4d0a00"))
                delete_button.bind("<Leave>", partial(color_on_hover, entry_frame, "#5a0b00"))
                delete_button.grid(row=0, column=4, rowspan=2, sticky="nse", padx=(5, 5))
        except AttributeError:
            pass

    def copy(self, entry, title, opt):
        self.clipboard_clear()
        self.clipboard_append(entry)
        if opt == "pass":
            print("Copied password for", title)
            self.controller.popup_noti("password", title)
        else:
            print("Copied login for", title)
            self.controller.popup_noti("login", title)
