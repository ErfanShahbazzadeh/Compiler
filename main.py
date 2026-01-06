import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import threading

class CompilerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler Suite Launcher")
        self.root.geometry("800x600")  # Increased size
        self.root.configure(bg='#1a1a2e')
        
        # Center the window
        self.center_window(800, 600)
        
        # Main container
        main_container = tk.Frame(root, bg='#1a1a2e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#1a1a2e')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with larger font
        title_label = tk.Label(header_frame, 
                              text="🛠️ COMPILER SUITE",
                              font=("Arial", 36, "bold"),
                              fg='#00adb5',
                              bg='#1a1a2e')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                 text="Lexical & Syntax Analysis Tools",
                                 font=("Arial", 16),
                                 fg='#eeeeee',
                                 bg='#1a1a2e')
        subtitle_label.pack(pady=(5, 0))
        
        # Separator
        separator = ttk.Separator(main_container, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Main Content Frame
        content_frame = tk.Frame(main_container, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Frame for Analyzers
        left_frame = tk.Frame(content_frame, bg='#1a1a2e', width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right Frame for File Operations
        right_frame = tk.Frame(content_frame, bg='#1a1a2e', width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # ANALYZER SELECTION (Left Side)
        analyzer_label = tk.Label(left_frame,
                                 text="📊 ANALYZERS",
                                 font=("Arial", 18, "bold"),
                                 fg='#00adb5',
                                 bg='#1a1a2e')
        analyzer_label.pack(anchor="w", pady=(0, 15))
        
        # Lexical Analyzer Card
        lexical_card = self.create_analyzer_card(left_frame,
                                                "🔍 LEXICAL ANALYZER",
                                                "Tokenizes source code into tokens\n"
                                                "Identifies keywords, identifiers,\n"
                                                "numbers, and symbols",
                                                "#00adb5",
                                                self.launch_lexical_analyzer)
        lexical_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Syntax Analyzer Card
        syntax_card = self.create_analyzer_card(left_frame,
                                               "📐 SYNTAX ANALYZER",
                                               "Validates token stream structure\n"
                                               "Checks grammatical correctness\n"
                                               "Builds parse tree visualization",
                                               "#ff2e63",
                                               self.launch_syntax_analyzer)
        syntax_card.pack(fill=tk.BOTH, expand=True)
        
        # FILE OPERATIONS (Right Side)
        file_label = tk.Label(right_frame,
                             text="📁 FILE OPERATIONS",
                             font=("Arial", 18, "bold"),
                             fg='#ff2e63',
                             bg='#1a1a2e')
        file_label.pack(anchor="w", pady=(0, 15))
        
        # Big File Operation Buttons
        file_buttons = [
            ("📝 EDIT SOURCE CODE", "Edit code.txt file", self.edit_code_file, "#393e46"),
            ("📊 VIEW TOKEN RESULTS", "View result.txt file", self.view_result_file, "#00adb5"),
            ("❌ VIEW ERROR LOG", "View error.txt file", self.view_error_file, "#ff2e63"),
            ("🔄 CHECK ALL FILES", "Update file status", self.check_files, "#ffd369"),
            ("📂 OPEN FOLDER", "Open Lexical Analysis folder", self.open_lexical_folder, "#9d65c9"),
            ("⚙️  SETTINGS", "Configure paths", self.show_settings, "#4CAF50"),
        ]
        
        for text, tooltip, command, color in file_buttons:
            btn = self.create_file_button(right_frame, text, tooltip, command, color)
            btn.pack(fill=tk.X, pady=8)
        
        # File Status Panel (at bottom)
        status_panel = tk.LabelFrame(main_container,
                                    text="📋 FILE STATUS PANEL",
                                    font=("Arial", 14, "bold"),
                                    fg='#eeeeee',
                                    bg='#16213e',
                                    relief=tk.GROOVE,
                                    bd=3)
        status_panel.pack(fill=tk.X, pady=(20, 0))
        
        # File status in a grid
        self.status_grid = tk.Frame(status_panel, bg='#16213e')
        self.status_grid.pack(fill=tk.X, padx=20, pady=15)
        
        files_to_check = [
            ("Lexical Analysis/code.txt", "Source Code", "📝"),
            ("Lexical Analysis/result.txt", "Token Results", "📊"),
            ("Lexical Analysis/error.txt", "Error Log", "❌"),
            ("Syntax Analysis/SAGUI3.py", "Syntax Analyzer", "📐"),
            ("Lexical Analysis/Lexical Analysis.py", "Lexical Analyzer", "🔍"),
        ]
        
        for i, (filepath, description, icon) in enumerate(files_to_check):
            self.create_status_row(self.status_grid, filepath, description, icon, i)
        
        # Bottom Status Bar
        status_bar = tk.Frame(main_container, bg='#0f3460', height=50)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        status_bar.pack_propagate(False)
        
        # Status message with larger font
        self.status_message = tk.Label(status_bar,
                                      text="Ready to compile! Select an analyzer to begin.",
                                      font=("Arial", 12),
                                      fg='#eeeeee',
                                      bg='#0f3460')
        self.status_message.pack(side=tk.LEFT, padx=20)
        
        # Version info
        info_label = tk.Label(status_bar,
                             text="Compiler Suite v2.1 | Professional Edition",
                             font=("Arial", 10),
                             fg='#a3a3a3',
                             bg='#0f3460')
        info_label.pack(side=tk.RIGHT, padx=20)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initial file check
        self.update_file_status()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_analyzer_card(self, parent, title, description, color, command):
        """Create an analyzer card"""
        card = tk.Frame(parent,
                       bg='#16213e',
                       relief=tk.RAISED,
                       bd=3)
        
        # Header with larger font
        header = tk.Frame(card, bg=color, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header,
                text=title,
                font=("Arial", 16, "bold"),
                fg='white',
                bg=color).pack(expand=True, pady=20)
        
        # Description with larger font
        desc_frame = tk.Frame(card, bg='#16213e', padx=20, pady=20)
        desc_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(desc_frame,
                text=description,
                font=("Arial", 12),
                fg='#eeeeee',
                bg='#16213e',
                justify=tk.LEFT).pack(anchor="w")
        
        # Launch button with larger font
        button_frame = tk.Frame(card, bg='#16213e', pady=15)
        button_frame.pack(fill=tk.X)
        
        launch_btn = tk.Button(button_frame,
                              text="🚀 LAUNCH ANALYZER",
                              command=command,
                              bg=color,
                              fg='white',
                              font=("Arial", 14, "bold"),
                              relief=tk.RAISED,
                              bd=3,
                              padx=40,
                              pady=12,
                              cursor="hand2")
        launch_btn.pack()
        
        # Hover effects
        def on_enter(e):
            card.configure(relief=tk.SUNKEN, bd=2)
            launch_btn.configure(bg=self.adjust_color(color, -20))
        
        def on_leave(e):
            card.configure(relief=tk.RAISED, bd=3)
            launch_btn.configure(bg=color)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
        
        return card
    
    def create_file_button(self, parent, text, tooltip, command, color):
        """Create a large file operation button"""
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg=color,
                       fg='white',
                       font=("Arial", 13, "bold"),
                       relief=tk.RAISED,
                       bd=3,
                       padx=20,
                       pady=15,
                       cursor="hand2",
                       anchor="w",
                       justify="left")
        
        # Add tooltip
        self.create_tooltip(btn, tooltip)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.adjust_color(color, -20), relief=tk.SUNKEN)
        
        def on_leave(e):
            btn.configure(bg=color, relief=tk.RAISED)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, bg="yellow", fg="black",
                            font=("Arial", 10), relief=tk.SOLID, borderwidth=1)
            label.pack()
            
            def hide_tooltip(event):
                tooltip.destroy()
            
            widget.bind("<Leave>", hide_tooltip)
        
        widget.bind("<Enter>", show_tooltip)
    
    def create_status_row(self, parent, filepath, description, icon, row):
        """Create a status row in the grid"""
        frame = tk.Frame(parent, bg='#16213e')
        frame.grid(row=row, column=0, sticky="ew", pady=5)
        parent.grid_columnconfigure(0, weight=1)
        
        # Icon
        tk.Label(frame, text=icon, font=("Arial", 14), 
                bg='#16213e', fg='white').pack(side=tk.LEFT, padx=(0, 15))
        
        # Description with larger font
        tk.Label(frame, 
                text=description,
                font=("Arial", 11),
                bg='#16213e',
                fg='#eeeeee').pack(side=tk.LEFT)
        
        # File path
        tk.Label(frame,
                text=f"({filepath})",
                font=("Arial", 9),
                bg='#16213e',
                fg='#a3a3a3').pack(side=tk.LEFT, padx=(10, 20))
        
        # Status indicator
        status_label = tk.Label(frame,
                               text="",
                               font=("Arial", 11, "bold"),
                               bg='#16213e')
        status_label.pack(side=tk.RIGHT)
        
        # Store reference
        if not hasattr(self, 'status_widgets'):
            self.status_widgets = {}
        self.status_widgets[filepath] = status_label
    
    def adjust_color(self, color, adjustment):
        """Adjust hex color brightness"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        r = max(0, min(255, r + adjustment))
        g = max(0, min(255, g + adjustment))
        b = max(0, min(255, b + adjustment))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def launch_lexical_analyzer(self):
        """Launch the lexical analyzer - FIXED PATH ISSUE"""
        self.update_status("Launching Lexical Analyzer...")
        
        # Define the correct path
        analyzer_path = "Lexical Analysis/Lexical Analysis.py"
        
        if not os.path.exists(analyzer_path):
            messagebox.showerror("File Not Found", 
                                f"Lexical analyzer not found at:\n{os.path.abspath(analyzer_path)}")
            self.update_status("Lexical analyzer file not found")
            return
        
        # Launch in a separate thread
        def run_lexical():
            try:
                # IMPORTANT: Get the absolute path to ensure we're in the right directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                lexical_dir = os.path.join(current_dir, "Lexical Analysis")
                analyzer_file = os.path.join(lexical_dir, "Lexical Analysis.py")
                
                print(f"Current directory: {current_dir}")
                print(f"Lexical directory: {lexical_dir}")
                print(f"Analyzer file: {analyzer_file}")
                
                # Check if file exists
                if not os.path.exists(analyzer_file):
                    self.root.after(0, lambda: messagebox.showerror(
                        "File Not Found", 
                        f"File not found: {analyzer_file}"
                    ))
                    return
                
                # Launch the analyzer with the correct working directory
                # This ensures relative paths like "code.txt" work correctly
                subprocess.Popen([sys.executable, analyzer_file], 
                                cwd=lexical_dir)
                
                self.root.after(0, lambda: self.update_status(
                    "Lexical Analyzer launched from correct directory"
                ))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Launch Error", 
                    f"Failed to launch lexical analyzer:\n{str(e)}\n\n"
                    f"Make sure the file exists at:\n{analyzer_file}"
                ))
                self.root.after(0, lambda: self.update_status("Launch failed"))
        
        # Start the thread
        thread = threading.Thread(target=run_lexical, daemon=True)
        thread.start()
    

    def launch_syntax_analyzer(self):
        """Launch the syntax analyzer"""
        self.update_status("Launching Syntax Analyzer...")
        
        analyzer_path = "Syntax Analysis/SAGUI3.py"
        
        if not os.path.exists(analyzer_path):
            messagebox.showerror("File Not Found", 
                                f"Syntax analyzer not found at:\n{os.path.abspath(analyzer_path)}")
            self.update_status("Syntax analyzer file not found")
            return
        
        # Launch in a separate thread
        def run_syntax():
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                analyzer_file = os.path.join(current_dir, "Syntax Analysis", "SAGUI3.py")
                
                if not os.path.exists(analyzer_file):
                    self.root.after(0, lambda: messagebox.showerror(
                        "File Not Found", 
                        f"File not found: {analyzer_file}"
                    ))
                    return
                
                # Launch syntax analyzer from its own directory
                subprocess.Popen([sys.executable, analyzer_file])
                
                self.root.after(0, lambda: self.update_status("Syntax Analyzer launched successfully"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Launch Error", 
                    f"Failed to launch syntax analyzer:\n{str(e)}"
                ))
                self.root.after(0, lambda: self.update_status("Launch failed"))
        
        thread = threading.Thread(target=run_syntax, daemon=True)
        thread.start()
    
    def edit_code_file(self):
        """Open code.txt for editing"""
        filepath = "Lexical Analysis/code.txt"
        if os.path.exists(filepath):
            self.open_file_editor(filepath, "Edit Source Code")
        else:
            response = messagebox.askyesno("File Not Found", 
                                          "code.txt not found. Create new file?")
            if response:
                self.open_file_editor(filepath, "Create New Source Code", create_new=True)
    
    def view_result_file(self):
        """View result.txt"""
        filepath = "Lexical Analysis/result.txt"
        if os.path.exists(filepath):
            self.open_file_viewer(filepath, "Tokenized Results")
        else:
            messagebox.showinfo("File Not Found", 
                              "result.txt not found.\n"
                              "Run the lexical analyzer first to generate this file.")
    
    def view_error_file(self):
        """View error.txt"""
        filepath = "Lexical Analysis/error.txt"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if content:
                self.open_file_viewer(filepath, "Error Log")
            else:
                messagebox.showinfo("No Errors", "No errors found in error.txt!")
        else:
            messagebox.showinfo("File Not Found", 
                              "error.txt not found.\n"
                              "No errors have been recorded yet.")
    
    def check_files(self):
        """Check all required files"""
        self.update_file_status()
        self.update_status("File status updated ✓")
    
    def open_lexical_folder(self):
        """Open the Lexical Analysis folder"""
        folder_path = "Lexical Analysis"
        if os.path.exists(folder_path):
            try:
                if sys.platform == "win32":
                    os.startfile(folder_path)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", folder_path])
                else:
                    subprocess.Popen(["xdg-open", folder_path])
                self.update_status("Opened Lexical Analysis folder")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
        else:
            messagebox.showinfo("Folder Not Found", "Lexical Analysis folder not found.")
    
    def show_settings(self):
        """Show settings window"""
        settings = tk.Toplevel(self.root)
        settings.title("Settings - Configure Paths")
        settings.geometry("500x400")
        settings.configure(bg='#1a1a2e')
        
        tk.Label(settings,
                text="⚙️  CONFIGURATION SETTINGS",
                font=("Arial", 18, "bold"),
                fg='#00adb5',
                bg='#1a1a2e').pack(pady=20)
        
        # Current paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        paths = [
            ("Main Directory:", current_dir),
            ("Lexical Analyzer:", os.path.join(current_dir, "Lexical Analysis", "Lexical Analysis.py")),
            ("Syntax Analyzer:", os.path.join(current_dir, "Syntax Analysis", "SAGUI3.py")),
            ("Source Code:", os.path.join(current_dir, "Lexical Analysis", "code.txt")),
        ]
        
        for label, path in paths:
            frame = tk.Frame(settings, bg='#1a1a2e')
            frame.pack(fill=tk.X, padx=30, pady=10)
            
            tk.Label(frame, text=label, font=("Arial", 11, "bold"),
                    fg='white', bg='#1a1a2e').pack(anchor="w")
            
            # Path with copy button
            path_frame = tk.Frame(frame, bg='#16213e', relief=tk.SUNKEN, bd=1)
            path_frame.pack(fill=tk.X, pady=5)
            
            path_label = tk.Label(path_frame, text=path, font=("Consolas", 9),
                                 fg='#eeeeee', bg='#16213e', anchor="w")
            path_label.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            copy_btn = tk.Button(path_frame, text="📋", font=("Arial", 10),
                                command=lambda p=path: self.copy_to_clipboard(p))
            copy_btn.pack(side=tk.RIGHT, padx=5)
        
        # Close button
        tk.Button(settings,
                 text="Close",
                 command=settings.destroy,
                 bg='#ff2e63',
                 fg='white',
                 font=("Arial", 12, "bold"),
                 padx=30,
                 pady=10).pack(pady=30)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.update_status("Copied to clipboard ✓")
    
    def open_file_editor(self, filepath, title, create_new=False):
        """Open file in editor window"""
        editor = tk.Toplevel(self.root)
        editor.title(title)
        editor.geometry("900x650")
        editor.configure(bg='#1a1a2e')
        
        # Title
        tk.Label(editor,
                text=title,
                font=("Arial", 20, "bold"),
                fg='#00adb5',
                bg='#1a1a2e').pack(pady=15)
        
        tk.Label(editor,
                text=f"File: {os.path.abspath(filepath)}",
                font=("Arial", 11),
                fg='#a3a3a3',
                bg='#1a1a2e').pack()
        
        # Text editor
        text_frame = tk.Frame(editor, bg='#16213e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        text_widget = tk.Text(text_frame,
                             wrap=tk.WORD,
                             font=("Consolas", 12),
                             bg='#0f3460',
                             fg='#eeeeee',
                             insertbackground='white',
                             selectbackground='#00adb5')
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
        
        # Load or create content
        if not create_new and os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            text_widget.insert(1.0, content)
        elif create_new:
            text_widget.insert(1.0, "# Enter your source code here\n")
        
        # Button frame
        button_frame = tk.Frame(editor, bg='#1a1a2e')
        button_frame.pack(pady=15)
        
        def save_file():
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text_widget.get(1.0, tk.END).rstrip())
                self.update_status(f"Saved: {filepath}")
                self.update_file_status()
                messagebox.showinfo("Success", f"File saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
        
        tk.Button(button_frame,
                 text="💾 SAVE FILE",
                 command=save_file,
                 bg='#00adb5',
                 fg='white',
                 font=("Arial", 13, "bold"),
                 padx=30,
                 pady=12).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame,
                 text="❌ CLOSE",
                 command=editor.destroy,
                 bg='#ff2e63',
                 fg='white',
                 font=("Arial", 13, "bold"),
                 padx=30,
                 pady=12).pack(side=tk.LEFT, padx=10)
    
    def open_file_viewer(self, filepath, title):
        """Open file in viewer window"""
        viewer = tk.Toplevel(self.root)
        viewer.title(title)
        viewer.geometry("800x550")
        viewer.configure(bg='#1a1a2e')
        
        tk.Label(viewer,
                text=title,
                font=("Arial", 20, "bold"),
                fg='#00adb5',
                bg='#1a1a2e').pack(pady=15)
        
        file_size = os.path.getsize(filepath)
        tk.Label(viewer,
                text=f"File: {os.path.basename(filepath)} | Size: {file_size:,} bytes | Path: {os.path.abspath(filepath)}",
                font=("Arial", 10),
                fg='#a3a3a3',
                bg='#1a1a2e').pack()
        
        # Text viewer
        text_frame = tk.Frame(viewer, bg='#16213e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        text_widget = tk.Text(text_frame,
                             wrap=tk.WORD,
                             font=("Consolas", 11),
                             bg='#0f3460',
                             fg='#eeeeee')
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        line_numbered = ""
        for i, line in enumerate(lines, 1):
            line_numbered += f"{i:4}: {line}\n"
        
        text_widget.insert(1.0, line_numbered)
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(viewer,
                 text="CLOSE",
                 command=viewer.destroy,
                 bg='#ff2e63',
                 fg='white',
                 font=("Arial", 12, "bold"),
                 padx=30,
                 pady=10).pack(pady=15)
    
    def update_file_status(self):
        """Update file status indicators"""
        files_to_check = [
            "Lexical Analysis/code.txt",
            "Lexical Analysis/result.txt", 
            "Lexical Analysis/error.txt",
            "Syntax Analysis/SAGUI3.py",
            "Lexical Analysis/Lexical Analysis.py",
        ]
        
        for filepath in files_to_check:
            if hasattr(self, 'status_widgets') and filepath in self.status_widgets:
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    status_text = f"✓ Found ({file_size:,} bytes)"
                    self.status_widgets[filepath].config(
                        text=status_text,
                        fg="#00adb5"
                    )
                else:
                    self.status_widgets[filepath].config(
                        text="✗ Missing",
                        fg="#ff2e63"
                    )
    
    def update_status(self, message):
        """Update status message"""
        self.status_message.config(text=f"Status: {message}")
        self.root.update()
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the Compiler Suite?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = CompilerLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()