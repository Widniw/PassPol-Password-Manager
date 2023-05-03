import customtkinter as ctk
from Start import Start
from Authorization import Authorization
from DatabaseContent import DatabaseContent
from PassGen import PassGen
from NewDatabase import NewDatabase

class PasswordManager(ctk.CTk):

    # Heart of the program, which holds all the frames and switches between them.

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title_font = ctk.CTkFont(family='Helvetica', size=18, weight="bold", slant="italic")
        self.scr_width = self.winfo_screenwidth()
        self.scr_height = self.winfo_screenheight()
        self.width = self.scr_width / 2
        self.height = self.scr_height / 2
        if self.width < 960:
            self.width = 960
        if self.height < 540:
            self.height = 540
        # x and y so that we put the main window in the center
        x = int((self.scr_width - self.width) / 2)
        y = int((self.scr_height - self.height) / 2)
        self.geometry(f'{int(self.width)}x{int(self.height)}+{x}+{y}')  # cenetring the main window on screen
        self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.title("PassPol")

        self.frames = {}
        self.pass_gen = None
        self.new_database = None
        self.new_password = None
        self.add_start_frame()

    def add_start_frame(self):
        self.frames["Start"] = Start(parent=self.container, controller=self, wind_width=self.width,
                                     wind_height=self.height)
        self.frames["Start"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("Start")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def add_auth_frame(self, page_name):
        self.frames[page_name] = Authorization(parent=self.container, controller=self, db=page_name)
        self.frames[page_name].grid(row=0, column=0, sticky="nsew")
        self.frames[page_name].tkraise()

    def add_database_content_frame(self, page_name, database):
        self.frames[page_name] = DatabaseContent(parent=self.container, controller=self, db=database)
        self.frames[page_name].grid(row=0, column=0, sticky="nsew")
        self.frames[page_name].tkraise()

    def delete_frame(self, page_name):
        del self.frames[page_name]

    def open_pass_gen(self):
        if self.pass_gen is None or not self.pass_gen.winfo_exists():
            self.pass_gen = PassGen(750, 350)
            # so that we don't create new instances of PassGen any time we close and open it
            self.pass_gen.protocol("WM_DELETE_WINDOW", lambda: (self.pass_gen.grab_release(), self.pass_gen.withdraw()))
        else:
            self.pass_gen.deiconify()
        self.pass_gen.grab_set()

    def open_new_database(self):
        self.new_database = NewDatabase(400, 400, controller=self)
        self.new_database.grab_set()

    def go_to_start_page(self, page_name):
        self.show_frame("Start")
        self.title("PassPol")
        self.delete_frame(page_name)


if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()
