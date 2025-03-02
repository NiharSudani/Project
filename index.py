import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        # Text Area
        self.text_area = scrolledtext.ScrolledText(self.root, undo=True, wrap="word")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Tab", accelerator="Ctrl+T", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="New Window", accelerator="Ctrl+N", command=self.new_window)
        file_menu.add_command(label="Save All", accelerator="Ctrl+Alt+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_editor)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_command(label="Delete", accelerator="Del", command=self.delete_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="Font", command=self.choose_font)
        edit_menu.add_command(label="Date/Time", command=self.insert_datetime)

        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_checkbutton(label="Status Bar")
        view_menu.add_checkbutton(label="Word Wrap", command=self.toggle_wrap)
        zoom_menu = tk.Menu(view_menu, tearoff=0)
        zoom_menu.add_command(label="Zoom In", accelerator="Ctrl+Plus")
        zoom_menu.add_command(label="Zoom Out", accelerator="Ctrl+Minus")
        zoom_menu.add_command(label="Default Zoom", accelerator="Ctrl+0")
        view_menu.add_cascade(label="Zoom", menu=zoom_menu)

        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Shortcuts
        self.root.bind("<Control-n>", lambda event: self.new_window())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_as())
        self.root.bind("<Control-q>", lambda event: self.exit_editor())

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def save_as(self):
        self.save_file()

    def new_window(self):
        self.root.destroy()
        root = tk.Tk()
        TextEditor(root)
        root.mainloop()

    def exit_editor(self):
        self.root.quit()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def delete_text(self):
        self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def choose_font(self):
        new_font = font.Font(family="Arial", size=12)
        self.text_area.configure(font=new_font)

    def insert_datetime(self):
        from datetime import datetime
        self.text_area.insert(tk.END, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def toggle_wrap(self):
        self.text_area.config(wrap=tk.WORD if self.text_area.cget("wrap") == "none" else "none")


if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()
