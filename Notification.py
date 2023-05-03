import customtkinter as ctk


class Notification(ctk.CTkFrame):
    def __init__(self, parent, text_, width):
        ctk.CTkFrame.__init__(self, master=parent, fg_color="#E59500")
        self.text = ctk.CTkLabel(master=self, text=text_, height=30)
        self.text.pack(anchor="center", padx=(10, 10), pady=(5, 5))
        self.update()
        self.width = width
        self.x = (self.width - self.winfo_reqwidth()) / 2
        self.y = 10
        self.current_y = -50
        self.show_anim()
        self.after(1800, self.hide_anim)

    def show_anim(self):
        if self.current_y < self.y:
            self.current_y += 1
            self.place(x=self.x, y=self.current_y)
            self.after(3, self.show_anim)

    def hide_anim(self):
        if self.current_y > self.y - 50:
            self.current_y -= 1
            self.place(x=self.x, y=self.current_y)
            self.after(6, self.hide_anim)
        else:
            self.destroy()
