import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, font, simpledialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("900x600")

        # Tabs
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        # Dictionary to store text areas
        self.text_areas = {}

        # Create the first tab
        self.new_tab()

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Tab", accelerator="Ctrl+T", command=self.new_tab)
        file_menu.add_command(label="New File", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_editor)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_command(label="Delete", accelerator="Del", command=self.delete_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", accelerator="Ctrl+H", command=self.find_replace)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        self.dark_mode = False
        self.show_status_bar = True
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_checkbutton(label="Status Bar", command=self.toggle_status_bar)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Format Menu
        format_menu = tk.Menu(self.menu_bar, tearoff=0)
        format_menu.add_command(label="Font", command=self.choose_font)
        self.menu_bar.add_cascade(label="Format", menu=format_menu)

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Line 1, Column 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_tab(self):
        """Create a new tab with a text area."""
        tab = tk.Frame(self.tab_control)
        text_area = scrolledtext.ScrolledText(tab, undo=True, wrap="word")
        text_area.pack(expand=True, fill="both")

        # Store the text area with its tab
        self.text_areas[tab] = text_area

        # Bind key and mouse events to update the status bar
        text_area.bind("<KeyRelease>", self.update_status)
        text_area.bind("<ButtonRelease-1>", self.update_status)

        # Add tab and switch to it
        self.tab_control.add(tab, text="Untitled")
        self.tab_control.select(tab)

    def new_file(self):
        """Clear the text in the current tab."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.delete(1.0, tk.END)

    def open_file(self):
        """Open a file in the current tab."""
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            text_area = self.get_current_text_area()
            if text_area:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, content)

    def save_file(self):
        """Save the content of the current tab."""
        file_path = filedialog.asksaveasfilename()
        if file_path:
            text_area = self.get_current_text_area()
            if text_area:
                with open(file_path, "w") as file:
                    file.write(text_area.get(1.0, tk.END))

    def save_as(self):
        """Save as a new file."""
        self.save_file()

    def exit_editor(self):
        """Exit the application."""
        self.root.quit()

    def undo(self):
        """Undo the last action."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.edit_undo()

    def redo(self):
        """Redo the last undone action."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.edit_redo()

    def cut_text(self):
        """Cut the selected text."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.event_generate("<<Cut>>")

    def copy_text(self):
        """Copy the selected text."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.event_generate("<<Copy>>")

    def paste_text(self):
        """Paste text from clipboard."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.event_generate("<<Paste>>")

    def delete_text(self):
        """Delete selected text."""
        text_area = self.get_current_text_area()
        if text_area:
            text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def find_replace(self):
        """Find and replace text."""
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        replace_str = simpledialog.askstring("Replace", "Enter replacement text:")
        if find_str and replace_str:
            text_area = self.get_current_text_area()
            content = text_area.get("1.0", tk.END)
            new_content = content.replace(find_str, replace_str)
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, new_content)

    def choose_font(self):
        """Change the font."""
        new_font = font.Font(family="Arial", size=12)
        text_area = self.get_current_text_area()
        if text_area:
            text_area.configure(font=new_font)

    def toggle_status_bar(self):
        """Show or hide the status bar."""
        self.show_status_bar = not self.show_status_bar
        if self.show_status_bar:
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.status_bar.pack_forget()

    def toggle_dark_mode(self):
        """Toggle dark mode for all tabs."""
        self.dark_mode = not self.dark_mode
        bg_color = "black" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        for text_area in self.text_areas.values():
            text_area.config(background=bg_color, foreground=fg_color, insertbackground=fg_color)

    def update_status(self, event=None):
        """Update the status bar with cursor position."""
        text_area = self.get_current_text_area()
        if text_area:
            line, column = text_area.index(tk.INSERT).split(".")
            self.status_bar.config(text=f"Line {line}, Column {column}")

    def show_about(self):
        """Display an about message."""
        messagebox.showinfo("About", "Multi-Tab Text Editor\nCreated with Python and Tkinter.")

if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()
