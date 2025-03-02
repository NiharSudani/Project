import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os


class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("800x600")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both")

        self.create_menu()
        self.new_tab()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Tab", accelerator="Ctrl+T", command=self.new_tab)
        file_menu.add_command(label="New Window", accelerator="Ctrl+N", command=self.new_window)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_command(label="Save All", accelerator="Ctrl+Alt+S", command=self.save_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_app)

        menubar.add_cascade(label="File", menu=file_menu)

        # Edit & View Menus (placeholders for now)
        menubar.add_cascade(label="Edit", menu=tk.Menu(menubar, tearoff=0))
        menubar.add_cascade(label="View", menu=tk.Menu(menubar, tearoff=0))

        # Keyboard Shortcuts
        self.root.bind("<Control-t>", lambda e: self.new_tab())
        self.root.bind("<Control-n>", lambda e: self.new_window())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_as())
        self.root.bind("<Control-Alt-s>", lambda e: self.save_all())
        self.root.bind("<Control-q>", lambda e: self.exit_app())

    def new_tab(self):
        frame = ttk.Frame(self.tabs)
        text_area = tk.Text(frame, wrap="word")
        text_area.pack(expand=1, fill="both")
        self.tabs.add(frame, text="Untitled")

    def new_window(self):
        os.system("python " + __file__)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.new_tab()
            text_widget = self.tabs.winfo_children()[-1].winfo_children()[0]
            text_widget.insert("1.0", content)
            self.tabs.tab("current", text=os.path.basename(file_path))

    def save_file(self):
        current_tab = self.tabs.select()
        text_widget = self.root.nametowidget(current_tab).winfo_children()[0]
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_widget.get("1.0", tk.END))
            self.tabs.tab(current_tab, text=os.path.basename(file_path))

    def save_as(self):
        self.save_file()

    def save_all(self):
        for tab in self.tabs.tabs():
            self.tabs.select(tab)
            self.save_file()

    def exit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()
