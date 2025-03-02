import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, simpledialog
import keyword


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        # Tabs
        self.tab_control = tk.ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        # Create the first tab (new file)
        self.new_file()

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
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_editor)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Replace", accelerator="Ctrl+H", command=self.replace_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_command(label="Delete", accelerator="Del", command=self.delete_text)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Dark Mode", command=self.toggle_dark_mode)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Line 1, Column 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Update the status bar when the cursor moves
        self.text_area.bind("<KeyRelease>", self.update_status)
        self.text_area.bind("<ButtonRelease-1>", self.update_status)

        # Auto-save functionality
        self.auto_save_interval = 300  # 5 minutes
        self.auto_save()

    def new_file(self):
        tab = tk.Frame(self.tab_control)
        self.text_area = scrolledtext.ScrolledText(tab, undo=True, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.tab_control.add(tab, text="Untitled")

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

    def find_text(self):
        search_term = simpledialog.askstring("Find", "Enter text to search:")
        if search_term:
            start_idx = '1.0'
            while True:
                start_idx = self.text_area.search(search_term, start_idx, stopindex=tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(search_term)}c"
                self.text_area.tag_add('found', start_idx, end_idx)
                self.text_area.tag_config('found', background='yellow')
                start_idx = end_idx

    def replace_text(self):
        search_term = simpledialog.askstring("Find", "Enter text to search:")
        replace_term = simpledialog.askstring("Replace", "Enter replacement text:")
        if search_term and replace_term:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(search_term, replace_term)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)

    def toggle_dark_mode(self):
        current_bg = self.text_area.cget("background")
        if current_bg == "black":
            self.text_area.config(background="white", foreground="black")
        else:
            self.text_area.config(background="black", foreground="white")

    def auto_save(self):
        self.save_file()  # Call the save method
        self.root.after(self.auto_save_interval * 1000, self.auto_save)  # Repeat every interval

    def update_status(self, event=None):
        line, column = self.text_area.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Line {line}, Column {column}")


if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()