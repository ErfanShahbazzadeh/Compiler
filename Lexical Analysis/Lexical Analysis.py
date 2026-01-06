import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time

identifier_dict = {}

def token_writer(T_type):
    with open("./Lexical Analysis/result.txt","a") as r:
        if T_type == "func":
            r.write("(func) ")
        elif T_type == "ayo":
            r.write("(ayo) ")
        elif T_type == "if":
            r.write("(if) ")
        elif T_type == "elif":
            r.write("(elif) ")
        elif T_type == "else":
            r.write("(else) ")
        elif T_type == "loop":
            r.write("(loop) ")
        elif T_type == "sendback":
            r.write("(sendback) ")
        elif T_type == "&":
            r.write("(&) ")   
        elif T_type == "|":
            r.write("(|) ")   

def id_writer(word, n):
    if word not in identifier_dict:
        identifier_dict[word] = n
        with open("./Lexical Analysis/result.txt","a") as r:
            r.write(f"(id,{n}) ")
        return n + 1
    else:
        existing_id = identifier_dict[word]
        with open("./Lexical Analysis/result.txt","a") as r:
            r.write(f"(id,{existing_id}) ")
        return n

def num_writer(num):
    with open("./Lexical Analysis/result.txt","a") as r:
        r.write(f"(num,{num}) ")


def num_checker(lexeme):
    state = 1
    flag_int = False
    flag_dot = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == '-': 
                    state = 2
                elif '0' <= ch <= '9':
                    flag_int = True
                    state = 3
                else:
                    return False
            case 2: 
                if '0' <= ch <= '9':
                    flag_int = True
                    state = 3
                else:
                    return False
            case 3: 
                if '0' <= ch <= '9':
                    state = 3
                elif ch == ".":
                    flag_dot = True
                    state = 4
                else:
                    return False
            case 4: 
                if '0' <= ch <= '9':
                    state = 5
                else:
                    return False
            case 5: 
                if '0' <= ch <= '9':
                    state = 5
                else:
                    return False
    
    if state == 3 or state == 5:  
        return True
    else:
        return False

def func_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "f":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "u":                        
                    state = 3
                else:
                    return False
            case 3:
                if ch == "n":
                    state = 4
                else:
                    return False
            case 4:
                if ch == "c":
                    flag = True
                    state = 5
                else:
                    return False
            case 5:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True
    

def ayo_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "a":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "y":                        
                    state = 3
                else:
                    return False
            case 3:
                if ch == "o":
                    flag = True
                    state = 4
                else:
                    return False
            case 4:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def if_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "i":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "f":
                    flag = True
                    state = 3
                else:
                    return False
            case 3:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def elif_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "e":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "l":
                    state = 3
                else:
                    return False
            case 3:
                if ch == "i":
                    state = 4
                else:
                    return False
            case 4:
                if ch == "f":
                    flag = True
                    state = 5
                else:
                    return False
            case 5:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def else_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "e":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "l":
                    state = 3
                else:
                    return False
            case 3:
                if ch == "s":
                    state = 4
                else:
                    return False
            case 4:
                if ch == "e":
                    flag = True
                    state = 5
                else:
                    return False
            case 5:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def and_checker(lexeme):
    if lexeme == "&":
        return True
    else:
        return False

def or_checker(lexeme):
    if lexeme == "|":
        return True
    else:
        return False

def loop_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "l":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "o":
                    state = 3
                else:
                    return False
            case 3:
                if ch == "o":
                    state = 4
                else:
                    return False
            case 4:
                if ch == "p":
                    flag = True
                    state = 5
                else:
                    return False
            case 5:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True


def Assignment_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "<":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "-":
                    state = 3
                else:
                    return False
            case 3:
                if ch == "-":
                    flag = True
                    state = 4
                else:
                    return False
            case 4:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True


def bgt_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "<":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "<":
                    flag = True
                    state = 3
                else:
                    return False
            case 3:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def lst_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == ">":
                    state = 2
                else:
                    return False
            case 2:
                if ch == ">":
                    flag = True
                    state = 3
                else:
                    return False
            case 3:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def eql_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "?":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "=":
                    flag = True
                    state = 3
                else:
                    return False
            case 3:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def sendback_checker(lexeme):
    state = 1
    flag = False
    for ch in lexeme:
        match state:
            case 1:
                if ch == "s":
                    state = 2
                else:
                    return False
            case 2:
                if ch == "e":
                    state = 3
                else:
                    return False
            case 3:
                if ch == "n":
                    state = 4
                else:
                    return False
            case 4:
                if ch == "d":
                    state = 5
                else:
                    return False
            case 5:
                if ch == "b":
                    state = 6
                else:
                    return False
            case 6:
                if ch == "a":
                    state = 7
                else:
                    return False
            case 7:
                if ch == "c":
                    state = 8
                else:
                    return False
            case 8:
                if ch == "k":
                    flag = True
                    state = 9
                else:
                    return False
            case 9:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_" or "0" <= ch <= "9":
                    return False
    if flag:
        return True

def identifier_checker(lexeme):
    state = 1
    for ch in lexeme:
        match state:
            case 1:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == "_":
                    state = 2
                else:
                    return False
            case 2:
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or "0" <= ch <= "9" or ch == "_":
                    state = 2
                else:
                    return False
    return True

def symbol_writer(symbol):
    with open("./Lexical Analysis/result.txt","a") as r:
        r.write(f"({symbol}) ")

def symbol_checker(lexeme):
    if lexeme == "<":
        symbol_writer("<")
        return True
    elif lexeme == ">":
        symbol_writer(">")
        return True
    elif lexeme == ",":
        symbol_writer(",")
        return True
    elif lexeme == "+":
        symbol_writer("+")
        return True
    elif lexeme == "-":
        symbol_writer("-")
        return True
    elif lexeme == "*":
        symbol_writer("*")
        return True
    elif lexeme == "/":
        symbol_writer("/")
        return True
    elif Assignment_checker(lexeme):
        symbol_writer("<--")
        return True
    elif eql_checker(lexeme):
        symbol_writer("?=")
        return True
    elif bgt_checker(lexeme):
        symbol_writer("<<")
        return True
    elif lst_checker(lexeme):
        symbol_writer(">>")
        return True
    elif lexeme == "{":
        symbol_writer("{")
        return True
    elif lexeme == "}":
        symbol_writer("}")
        return True

# GUI Code
class CodeAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Analyzer")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Code Analyzer", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Code input label
        code_label = tk.Label(main_frame, text="Code Input:", font=("Arial", 12))
        code_label.pack(anchor="w")
        
        # Text box for code input
        self.code_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, font=("Consolas", 10))
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Write button
        self.write_button = tk.Button(button_frame, text="Write", command=self.start_write_animation, 
                                     bg="lightblue", font=("Arial", 10, "bold"), width=10)
        self.write_button.pack(side=tk.LEFT, padx=5)
        
        # Compile button
        self.compile_button = tk.Button(button_frame, text="Compile", command=self.compile_code,
                                      bg="lightgreen", font=("Arial", 10, "bold"), width=10)
        self.compile_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button (optional)
        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_text,
                                    bg="lightcoral", font=("Arial", 10, "bold"), width=10)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Ready", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=5)
    
    def start_write_animation(self):
        """Start the writing animation in a separate thread"""
        self.write_button.config(state=tk.DISABLED)
        self.compile_button.config(state=tk.DISABLED)
        self.status_label.config(text="Writing code...", fg="orange")
        
        # Run the animation in a separate thread to avoid freezing the GUI
        thread = threading.Thread(target=self.write_animation)
        thread.daemon = True
        thread.start()


    def write_animation(self):
        """Animate writing code from code.txt to the text box"""
        try:
            # Clear the text box first
            self.code_text.delete(1.0, tk.END)
            
            # Read the content from code.txt
            with open("./Lexical Analysis/code.txt", "r") as f:
                content = f.read()
            
            # Write character by character with a small delay
            for char in content:
                self.code_text.insert(tk.END, char)
                self.code_text.see(tk.END)  # Auto-scroll
                self.root.update()
                time.sleep(0.01)  # Adjust speed here (smaller = faster)
            
            self.status_label.config(text="Code written successfully!", fg="green")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "code.txt file not found!")
            self.status_label.config(text="Error: code.txt not found", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
        finally:
            self.write_button.config(state=tk.NORMAL)
            self.compile_button.config(state=tk.NORMAL)
    
    def compile_code(self):
        """Compile the code and show results in a new window"""
        try:
            # Clear previous results and errors
            open("result.txt", "w").close()
            open("Error.txt", "w").close()
            identifier_dict.clear()
            
            # Get code from text box and save to code.txt
            code_content = self.code_text.get(1.0, tk.END)
            with open("./Lexical Analysis/code.txt", "w") as f:
                f.write(code_content)
            
            # Run your existing analysis code
            self.run_analysis()
            
            # Show results in a new window
            self.show_results()
            
            self.status_label.config(text="Compilation completed!", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Compilation error: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
    
    def run_analysis(self):
        """Run your existing analysis code"""
        n = 1
        line_count = 0
        with open("./Lexical Analysis/code.txt", "r") as f:
            while True:
                line = f.readline()
                line_count += 1
                if not line:
                    break

                split_line = line.split()
                for word in split_line:
                    if func_checker(word):
                        token_writer("func")
                    elif ayo_checker(word):
                        token_writer("ayo")
                    elif if_checker(word):
                        token_writer("if")
                    elif elif_checker(word):
                        token_writer("elif")
                    elif else_checker(word):
                        token_writer("else")
                    elif loop_checker(word):
                        token_writer("loop")
                    elif sendback_checker(word):
                        token_writer("sendback")
                    elif and_checker(word):
                        token_writer("&")
                    elif or_checker(word):
                        token_writer("|")
                    elif symbol_checker(word):
                        continue
                    elif identifier_checker(word):
                        n = id_writer(word, n)
                    elif num_checker(word):
                        num_writer(word)
                    else:
                        with open("./Lexical Analysis/result.txt","a") as r:
                            r.write(f"(error) ")

                        with open("./Lexical Analysis/Error.txt","a") as E:
                            E.write(f"In line{line_count}, '{word}' is not recognizable\n")
                with open("./Lexical Analysis/result.txt","a") as r:
                    r.write("\n")
    
    def show_results(self):
        """Show compilation results in a new window"""
        # Create new window
        result_window = tk.Toplevel(self.root)
        result_window.title("Compilation Results")
        result_window.geometry("700x500")
        
        # Main frame
        main_frame = tk.Frame(result_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Compilation Results", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Result text area
        result_label = tk.Label(main_frame, text="Tokenized Result:", font=("Arial", 12))
        result_label.pack(anchor="w")
        
        result_text = scrolledtext.ScrolledText(main_frame, height=10, width=80, font=("Consolas", 10))
        result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Read and display result.txt
        try:
            with open("./Lexical Analysis/result.txt", "r") as f:
                result_content = f.read()
            result_text.insert(1.0, result_content)
        except FileNotFoundError:
            result_text.insert(1.0, "No results found.")
        
        # Error text area
        error_label = tk.Label(main_frame, text="Errors:", font=("Arial", 12))
        error_label.pack(anchor="w", pady=(10, 0))
        
        error_text = scrolledtext.ScrolledText(main_frame, height=5, width=80, font=("Consolas", 10))
        error_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Read and display Error.txt
        try:
            with open("./Lexical Analysis/Error.txt", "r") as f:
                error_content = f.read()
            error_text.insert(1.0, error_content if error_content else "No errors found.")
        except FileNotFoundError:
            error_text.insert(1.0, "No error file found.")
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=result_window.destroy,
                               bg="lightcoral", font=("Arial", 10, "bold"))
        close_button.pack(pady=10)
    
    def clear_text(self):
        """Clear the text box"""
        self.code_text.delete(1.0, tk.END)
        self.status_label.config(text="Text cleared", fg="blue")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerGUI(root)
    root.mainloop()