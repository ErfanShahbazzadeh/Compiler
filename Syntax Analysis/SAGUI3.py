import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time

# ====================================================
# SYNTAX ANALYZER CODE
# ====================================================
# Global Variables
tokens = []
index = 0
lookahead = ""
current_line = 1
token_positions = []  # Store line numbers for each token
parse_tree_data = []  # Store parse tree nodes for visualization

# --- Helper Logic for Token Matching ---
def is_type(expected_pattern):
    """
    Checks if the current lookahead matches the expected pattern type.
    Solves the (id,1) == (id,\d+) comparison problem.
    """
    global lookahead
    if lookahead == "": return False

    # Check for ID pattern
    if expected_pattern == "(id,\\d+)":
        return lookahead.startswith("(id,") and lookahead.endswith(")")
    
    # Check for NUM pattern
    elif expected_pattern == "(num,\\d+)":
        return lookahead.startswith("(num,") and lookahead.endswith(")")
    
    # Exact Match for others (e.g., (if), (<--))
    else:
        return lookahead == expected_pattern

def S_match(expected_token):
    global lookahead, index
    
    # Validate match using the same logic as is_type
    if is_type(expected_token):
        index += 1
        if index < len(tokens):
            lookahead = tokens[index]
        else:
            lookahead = "" # End of file
        return True
    else:
        return False

# --- Grammar Functions ---

def START():
    # START -> STATEMENT START | ε
    if (is_type("(if)") or is_type("(func)") or is_type("(loop)") or 
        is_type("(id,\\d+)") or is_type("(sendback)")):
        if not STATEMENT():
            return False
        if not START():
            return False
    else:
        # Epsilon (End of input or end of block)
        pass
    return True

def STATEMENT():
    if is_type("(if)"):
        if not S_match("(if)"): return False
        if not S_match("({)"): return False
        if not COMPARE(): return False
        if not S_match("(})"): return False
        if not S_match("(<)"): return False
        if not CODE(): return False
        if not S_match("(>)"): return False
        if not CONDITIONS(): return False
    
    elif is_type("(func)"):
        if not S_match("(func)"): return False
        if not S_match("(id,\\d+)"): return False
        if not S_match("({)"): return False
        if not PARAM(): return False
        if not S_match("(})"): return False
        if not S_match("(<)"): return False
        if not CODE(): return False
        if not S_match("(>)"): return False

    elif is_type("(loop)"):
        if not S_match("(loop)"): return False
        if not S_match("({)"): return False
        if not COMPARE(): return False
        if not S_match("(})"): return False
        if not S_match("(<)"): return False
        if not CODE(): return False
        if not S_match("(>)"): return False

    elif is_type("(id,\\d+)"):
        if not S_match("(id,\\d+)"): return False
        if not REST_OF_ID(): return False
        
    elif is_type("(sendback)"):
        if not S_match("(sendback)"): return False
        if not S_match("(id,\\d+)"): return False

    else:
        return False
    return True

def REST_OF_ID():
    # Handles the difference between id <-- ... and id { ... }
    if is_type("(<--)"):
        if not S_match("(<--)"): return False
        if not ASSIGN_TAIL(): return False
    elif is_type("({)"):
        if not S_match("({)"): return False
        if not PARAM(): return False
        if not S_match("(})"): return False
    else:
        return False
    return True

def ASSIGN_TAIL():
    if is_type("(ayo)"):
        if not S_match("(ayo)"): return False
        if not S_match("(id,\\d+)"): return False
        if not S_match("({)"): return False
        if not PARAM(): return False
        if not S_match("(})"): return False
    else:
        # Variable Operation (Math)
        if not VARIABLE(): return False
        if not OPERATION(): return False
    return True

def CODE():
    # CODE -> STATEMENT CODE | ε
    # Check First(STATEMENT) to decide whether to continue recursion
    if (is_type("(if)") or is_type("(func)") or is_type("(loop)") or 
        is_type("(id,\\d+)") or is_type("(sendback)")):
        if not STATEMENT(): return False
        if not CODE(): return False
    else:
        pass # Epsilon (Matches empty string, usually before '>')
    return True

def CONDITIONS():
    if is_type("(elif)"):
        if not S_match("(elif)"): return False
        if not S_match("({)"): return False
        if not COMPARE(): return False
        if not S_match("(})"): return False
        if not S_match("(<)"): return False
        if not CODE(): return False
        if not S_match("(>)"): return False
        if not CONDITIONS(): return False
    elif is_type("(else)"):
        if not S_match("(else)"): return False
        if not S_match("(<)"): return False
        if not CODE(): return False
        if not S_match("(>)"): return False
    else:
        pass # Epsilon
    return True

def COMPARE():
    # COMPARE -> AND_EXPR COMPARE_TAIL
    if not AND_EXPR(): return False
    if not COMPARE_TAIL(): return False
    return True

def COMPARE_TAIL():
    # COMPARE_TAIL -> / AND_EXPR COMPARE_TAIL | ε
    if is_type("(|)"): # Logical OR
        if not S_match("(|)"): return False
        if not AND_EXPR(): return False
        if not COMPARE_TAIL(): return False
    else:
        pass
    return True

def AND_EXPR():
    # AND_EXPR -> UNIT_COMP UNIT_TAIL
    if not UNIT_COMP(): return False
    if not UNIT_TAIL(): return False
    return True

def UNIT_TAIL():
    # UNIT_TAIL -> & UNIT_COMP UNIT_TAIL | ε
    if is_type("(&)"):
        if not S_match("(&)"): return False
        if not UNIT_COMP(): return False
        if not UNIT_TAIL(): return False
    else:
        pass
    return True

# def UNIT_COMP():
#     if not VARIABLE(): return False
#     if not COMPARATOR(): return False
#     if not VARIABLE(): return False
#     return True

def UNIT_COMP():
    if not VARIABLE(): return False
    if not OPERATION(): return False  # Added this
    if not COMPARATOR(): return False
    if not VARIABLE(): return False
    if not OPERATION(): return False  # Added this
    return True


def COMPARATOR():
    if is_type("(<<)"):
        if not S_match("(<<)"): return False
    elif is_type("(>>)"):
        if not S_match("(>>)"): return False
    elif is_type("(?=)"):
        if not S_match("(?=)"): return False
    else:
        return False
    return True

def PARAM():
    # PARAM -> TERM PARAM_TAIL | ε
    if is_type("(id,\\d+)") or is_type("(num,\\d+)"):
        if not TERM(): return False
        if not PARAM_TAIL(): return False
    else:
        pass
    return True

def PARAM_TAIL():
    # PARAM_TAIL -> , TERM PARAM_TAIL | ε
    if is_type("(,)"):
        if not S_match("(,)"): return False
        if not TERM(): return False
        if not PARAM_TAIL(): return False
    else:
        pass
    return True

def TERM():
    if is_type("(id,\\d+)"):
        if not S_match("(id,\\d+)"): return False
    elif is_type("(num,\\d+)"):
        if not S_match("(num,\\d+)"): return False
    else:
        return False
    return True

def VARIABLE():
    # Same as TERM in this context
    return TERM()

def OPERATION():
    if is_type("(+)") or is_type("(-)") or is_type("(*)") or is_type("(/)"):
        if not S_match(lookahead): return False # Matches whatever operator it found
        if not VARIABLE(): return False
    else:
        pass # Epsilon
    return True

def parse_tokens_with_animation(tokens_list, token_positions_list, update_callback):
    """Parse tokens with animation callback"""
    global tokens, index, lookahead, current_line
    
    tokens = tokens_list
    index = 0
    lookahead = tokens[0] if tokens else ""
    current_line = 1
    
    # Call START
    success = START()
    
    if success and lookahead == "":
        return True, "Syntax Correct - All tokens processed successfully!"
    elif not success:
        # Find the line number of the error
        error_line = 1
        if index < len(token_positions_list):
            error_line = token_positions_list[index]
        return False, f"Syntax Error at line {error_line}: Unexpected token '{lookahead}'"
    else:
        error_line = 1
        if index < len(token_positions_list):
            error_line = token_positions_list[index]
        return False, f"Syntax Error at line {error_line}: Unconsumed tokens remaining: {lookahead}"

# ====================================================
# PARSE TREE VISUALIZATION
# ====================================================
class ParseTreeVisualizer:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Parse Tree Visualization")
        self.window.geometry("1200x800")
        
        # Canvas for drawing tree
        self.canvas = tk.Canvas(self.window, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Control frame
        control_frame = tk.Frame(self.window)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(control_frame, text="Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Reset View", command=self.reset_view).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        self.zoom_level = 1.0
        self.nodes = []
        self.edges = []
        
    def zoom_in(self):
        self.zoom_level *= 1.2
        self.redraw_tree()
    
    def zoom_out(self):
        self.zoom_level /= 1.2
        self.redraw_tree()
    
    def reset_view(self):
        self.zoom_level = 1.0
        self.redraw_tree()
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
    
    def draw_tree(self, tokens):
        """Draw parse tree based on tokens"""
        self.canvas.delete("all")
        self.nodes = []
        self.edges = []
        
        if not tokens:
            self.canvas.create_text(600, 400, text="No tokens to visualize", font=("Arial", 16))
            return
        
        # Calculate tree layout
        tree_structure = self.build_tree_structure(tokens)
        
        # Draw tree
        self.draw_node(tree_structure, 600, 50, 150)
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def build_tree_structure(self, tokens):
        """Build a simplified parse tree structure from tokens"""
        # This is a simplified representation
        # In a real implementation, you would parse the tokens and build the actual parse tree
        
        root = {"name": "PROGRAM", "children": []}
        current = root
        
        for token in tokens:
            if token in ["(if)", "(func)", "(loop)"]:
                node = {"name": token[1:-1].upper(), "children": []}
                current["children"].append(node)
                current = node
            elif token in ["(<)", "(>)"]:
                # Move back up in tree
                pass
            elif token.startswith("(id,") or token.startswith("(num,"):
                node = {"name": token[1:-1], "children": []}
                current["children"].append(node)
            else:
                node = {"name": token[1:-1], "children": []}
                current["children"].append(node)
        
        return root
    
    def draw_node(self, node, x, y, x_offset):
        """Recursively draw tree nodes"""
        # Draw current node
        node_id = self.canvas.create_oval(x-40*self.zoom_level, y-20*self.zoom_level,
                                         x+40*self.zoom_level, y+20*self.zoom_level,
                                         fill="lightblue", outline="black", width=2)
        text_id = self.canvas.create_text(x, y, text=node["name"], font=("Arial", int(10*self.zoom_level)))
        
        self.nodes.append((node_id, text_id, node["name"]))
        
        # Draw children
        if node["children"]:
            child_y = y + 100 * self.zoom_level
            child_count = len(node["children"])
            
            # Calculate starting x position for children
            start_x = x - ((child_count - 1) * x_offset * self.zoom_level) / 2
            
            for i, child in enumerate(node["children"]):
                child_x = start_x + (i * x_offset * self.zoom_level)
                
                # Draw edge to child
                edge_id = self.canvas.create_line(x, y+20*self.zoom_level, child_x, child_y-20*self.zoom_level,
                                                 width=2, fill="black")
                self.edges.append(edge_id)
                
                # Draw child
                self.draw_node(child, child_x, child_y, x_offset * 0.7)
    
    def redraw_tree(self):
        """Redraw tree with current zoom level"""
        # Store current view
        current_nodes = self.nodes.copy()
        
        # Clear and redraw
        self.canvas.delete("all")
        self.nodes = []
        self.edges = []
        
        # Recreate tree structure and draw
        # This would need the original tree data to be stored
        
        # For now, just show a message
        self.canvas.create_text(600, 400, text="Use the main analysis to generate parse tree", 
                               font=("Arial", int(16*self.zoom_level)))

# ====================================================
# GUI CODE
# ====================================================
class SyntaxAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Analyzer")
        self.root.geometry("1000x750")
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(root, text="Syntax Analyzer", font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Main frame with left and right panels
        main_frame = tk.Frame(root)
        main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Left Panel - Input
        left_frame = tk.LabelFrame(main_frame, text="Input Tokens", font=("Arial", 12, "bold"))
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # File selection frame
        file_frame = tk.Frame(left_frame)
        file_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        
        tk.Label(file_frame, text="Token File:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.file_entry = tk.Entry(file_frame, width=35)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        self.file_entry.insert(0, "./Lexical Analysis/result.txt")
        
        load_button = tk.Button(file_frame, text="Load File", command=self.load_file,
                               bg="lightblue", font=("Arial", 10))
        load_button.pack(side=tk.LEFT, padx=5)
        
        # Input text area
        input_label = tk.Label(left_frame, text="Or paste tokens below:", font=("Arial", 10))
        input_label.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 0))
        
        self.input_text = scrolledtext.ScrolledText(left_frame, height=25, width=45, 
                                                   font=("Consolas", 10))
        self.input_text.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Example button
        example_button = tk.Button(left_frame, text="Load Example", command=self.load_example,
                                  bg="lightgreen", font=("Arial", 10))
        example_button.grid(row=3, column=0, pady=5)
        
        # Right Panel - Output
        right_frame = tk.LabelFrame(main_frame, text="Analysis Results", font=("Arial", 12, "bold"))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.grid_rowconfigure(0, weight=1)  # Results area
        right_frame.grid_rowconfigure(1, weight=1)  # Token stream area
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Results area with equal height
        results_subframe = tk.Frame(right_frame)
        results_subframe.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        results_subframe.grid_rowconfigure(0, weight=1)
        results_subframe.grid_columnconfigure(0, weight=1)
        
        tk.Label(results_subframe, text="Analysis Output:", font=("Arial", 10)).pack(anchor="w", padx=5)
        
        self.result_text = scrolledtext.ScrolledText(results_subframe, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5)
        self.result_text.config(state=tk.DISABLED)
        
        # Token stream area with equal height
        token_subframe = tk.Frame(right_frame)
        token_subframe.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        token_subframe.grid_rowconfigure(0, weight=1)
        token_subframe.grid_columnconfigure(0, weight=1)
        
        tk.Label(token_subframe, text="Token Stream:", font=("Arial", 10)).pack(anchor="w", padx=5)
        
        self.token_display = scrolledtext.ScrolledText(token_subframe, font=("Consolas", 10))
        self.token_display.pack(fill=tk.BOTH, expand=True, padx=5)
        self.token_display.config(state=tk.DISABLED)
        
        # Status label
        self.status_label = tk.Label(right_frame, text="Ready", font=("Arial", 10), fg="blue")
        self.status_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        # Button frame at bottom
        button_frame = tk.Frame(root)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Analyze button
        self.analyze_button = tk.Button(button_frame, text="Analyze Syntax", 
                                       command=self.start_analysis,
                                       bg="green", fg="white", 
                                       font=("Arial", 12, "bold"), width=15)
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_button = tk.Button(button_frame, text="Clear All", 
                                command=self.clear_all,
                                bg="orange", font=("Arial", 12), width=10)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Parse Tree button
        self.tree_button = tk.Button(button_frame, text="Show Parse Tree", 
                                    command=self.show_parse_tree,
                                    bg="purple", fg="white", 
                                    font=("Arial", 12), width=15,
                                    state=tk.DISABLED)  # Disabled until analysis
        self.tree_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", 
                               command=root.quit,
                               bg="red", fg="white", font=("Arial", 12), width=10)
        exit_button.pack(side=tk.LEFT, padx=5)
        
        # Animation control
        self.animation_speed = tk.DoubleVar(value=0.1)
        speed_frame = tk.Frame(button_frame)
        speed_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(speed_frame, text="Speed:", font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Scale(speed_frame, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL,
                variable=self.animation_speed, length=100).pack(side=tk.LEFT, padx=5)
        
        # Variables for analysis results
        self.current_tokens = []
        self.analysis_successful = False
        
        # Load initial example
        self.load_example()
    
    def load_file(self):
        """Load tokens from a file"""
        try:
            filename = self.file_entry.get()
            with open(filename, "r") as f:
                content = f.read()
            
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(1.0, content)
            self.status_label.config(text=f"Loaded {filename}", fg="green")
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' not found!")
            self.status_label.config(text="File not found", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {str(e)}")
            self.status_label.config(text="Load error", fg="red")
    
    def load_example(self):
        """Load an example token stream"""
        example = """(func) (id,1) ({) (id,2) (,) (id,3) (}) (<) 
(loop) ({) (id,2) (<<) (id,3) (}) (<) 
(if) ({) (id,2) (/) (num,3) (?=) (num,0) (}) (<) 
(id,2) (<--) (id,2) (+) (num,1) 
(>) 
(elif) ({) (id,2) (/) (num,3) (?=) (num,1) (|) (id,2) (/) (num,3) (?=) (num,2) (}) (<) 
(id,2) (<--) (id,2) (+) (num,2) 
(>) 
(else) (<) 
(id,3) (<--) (id,3) (+) (num,1) 
(>) 
(>) 
(sendback) (id,2) 
(>) 

(id,4) (<--) (num,-43) 
(id,5) (<--) (num,-5.3) 

(id,6) (<--) (ayo) (id,1) ({) (num,3) (,) (num,10) (})"""
        
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, example)
        self.status_label.config(text="Example loaded", fg="blue")
    
    def start_analysis(self):
        """Start syntax analysis in a separate thread"""
        self.analyze_button.config(state=tk.DISABLED)
        self.tree_button.config(state=tk.DISABLED)
        self.status_label.config(text="Analyzing...", fg="orange")
        
        # Clear previous results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        self.token_display.config(state=tk.NORMAL)
        self.token_display.delete(1.0, tk.END)
        self.token_display.config(state=tk.DISABLED)
        
        # Run analysis in separate thread
        thread = threading.Thread(target=self.run_analysis_thread)
        thread.daemon = True
        thread.start()
    
    def run_analysis_thread(self):
        """Run the syntax analysis (in thread)"""
        try:
            # Get input tokens
            input_content = self.input_text.get(1.0, tk.END)
            
            # Parse tokens with line numbers
            tokens_list = []
            token_positions = []
            lines = input_content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                tokens_in_line = [t for t in line.split(" ") if t.strip() != ""]
                tokens_list.extend(tokens_in_line)
                token_positions.extend([line_num] * len(tokens_in_line))
            
            # Store tokens for tree visualization
            self.current_tokens = tokens_list
            
            # Display tokens initially
            self.root.after(0, self.display_tokens_initial, tokens_list)
            time.sleep(0.5)  # Small delay for visual effect
            
            # Animate token checking
            self.root.after(0, self.animate_token_checking, tokens_list)
            
            # Run actual analysis
            success, message = parse_tokens_with_animation(tokens_list, token_positions, None)
            
            # Update final results
            self.analysis_successful = success
            self.root.after(0, self.update_final_results, success, message, token_positions)
            
            # Animate token checking
            self.root.after(0, self.animate_token_checking, tokens_list)
        
            # IMPORTANT: Wait for animation to complete
            # Calculate animation time based on number of tokens
            animation_time = len(tokens_list) * self.animation_speed.get() * 1000
            
            # Wait for animation to finish before running actual analysis
            self.root.after(int(animation_time + 500), 
                        lambda: self.run_actual_analysis(tokens_list, token_positions))
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def run_actual_analysis(self, tokens_list, token_positions):
        """Run the actual syntax analysis after animation"""
        # Run actual analysis
        success, message = parse_tokens_with_animation(tokens_list, token_positions, None)
        
        # Update final results
        self.analysis_successful = success
        self.update_final_results(success, message, token_positions)

    
    def display_tokens_initial(self, tokens_list):
        """Display tokens initially before animation"""
        self.token_display.config(state=tk.NORMAL)
        self.token_display.delete(1.0, tk.END)
        
        # Display tokens
        token_text = ""
        for i, token in enumerate(tokens_list):
            token_text += f"{token} "
            if (i + 1) % 8 == 0:  # New line every 8 tokens
                token_text += "\n"
        
        self.token_display.insert(1.0, token_text)
        
        # Store token positions for highlighting
        self.token_positions = []
        pos = 1.0
        for token in tokens_list:
            end_pos = f"{pos}+{len(token)}c"
            self.token_positions.append((pos, end_pos))
            pos = end_pos + "+1c"  # +1 for space
        
        self.token_display.config(state=tk.DISABLED)
    
    def animate_token_checking(self, tokens_list):
        """Animate the token checking process"""
        def animate_next_token(i=0):
            if i < len(tokens_list):
                # Highlight current token
                start_pos, end_pos = self.token_positions[i]
                
                self.token_display.config(state=tk.NORMAL)
                self.token_display.tag_remove("checking", "1.0", tk.END)
                self.token_display.tag_add("checking", start_pos, end_pos)
                self.token_display.tag_config("checking", background="yellow", foreground="black")
                self.token_display.see(start_pos)
                self.token_display.config(state=tk.DISABLED)
                
                # Update status
                self.status_label.config(text=f"Checking token {i+1}/{len(tokens_list)}: {tokens_list[i]}", fg="orange")
                
                # Schedule next token
                self.root.after(int(self.animation_speed.get() * 1000), lambda: animate_next_token(i+1))
            else:
                # All tokens checked
                self.token_display.config(state=tk.NORMAL)
                self.token_display.tag_remove("checking", "1.0", tk.END)
                
                # Mark all as passed (green)
                for start_pos, end_pos in self.token_positions:
                    self.token_display.tag_add("passed", start_pos, end_pos)
                self.token_display.tag_config("passed", background="lightgreen", foreground="black")
                self.token_display.config(state=tk.DISABLED)
                
                self.status_label.config(text="All tokens processed", fg="green")
        
        # Start animation
        animate_next_token()
    
    def update_final_results(self, success, message, token_positions):
        """Update the GUI with final analysis results"""
        # Enable analyze button
        self.analyze_button.config(state=tk.NORMAL)
        
        # Enable tree button if analysis was successful
        if success:
            self.tree_button.config(state=tk.NORMAL)
        
        # Update result text
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if success:
            self.result_text.insert(1.0, "✓ SYNTAX ANALYSIS PASSED\n\n")
            self.result_text.insert(tk.END, f"Message: {message}\n\n")
            self.status_label.config(text="Syntax Correct!", fg="green")
            
            # Color the result text
            self.result_text.tag_add("success", "1.0", "1.24")
            self.result_text.tag_config("success", foreground="green", font=("Consolas", 10, "bold"))
        else:
            self.result_text.insert(1.0, "✗ SYNTAX ANALYSIS FAILED\n\n")
            self.result_text.insert(tk.END, f"Error: {message}\n\n")
            self.status_label.config(text="Syntax Error", fg="red")
            
            # Color the result text
            self.result_text.tag_add("error", "1.0", "1.24")
            self.result_text.tag_config("error", foreground="red", font=("Consolas", 10, "bold"))
            
            # Highlight error line in input
            self.highlight_error_line(message)
        
        self.result_text.config(state=tk.DISABLED)
    
    def highlight_error_line(self, error_message):
        """Highlight the line with error in input text"""
        try:
            # Extract line number from error message
            import re
            match = re.search(r'line (\d+)', error_message)
            if match:
                line_num = int(match.group(1))
                
                self.input_text.config(state=tk.NORMAL)
                
                # Highlight the line
                start_pos = f"{line_num}.0"
                end_pos = f"{line_num}.end"
                
                self.input_text.tag_add("error_line", start_pos, end_pos)
                self.input_text.tag_config("error_line", background="red", foreground="white")
                
                # Scroll to error line
                self.input_text.see(start_pos)
                self.input_text.config(state=tk.NORMAL)
        except:
            pass
    
    def show_parse_tree(self):
        """Show parse tree visualization window"""
        if not self.current_tokens:
            messagebox.showwarning("No Data", "Please run syntax analysis first!")
            return
        
        visualizer = ParseTreeVisualizer(self.root)
        visualizer.draw_tree(self.current_tokens)
    
    def show_error(self, error_msg):
        """Show error message"""
        self.analyze_button.config(state=tk.NORMAL)
        self.status_label.config(text="Analysis Error", fg="red")
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, f"Error: {error_msg}")
        self.result_text.config(state=tk.DISABLED)
    
    def clear_all(self):
        """Clear all input and output"""
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(1.0, tk.END)
        self.input_text.tag_remove("error_line", "1.0", tk.END)
        self.input_text.config(state=tk.NORMAL)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        self.token_display.config(state=tk.NORMAL)
        self.token_display.delete(1.0, tk.END)
        self.token_display.config(state=tk.DISABLED)
        
        self.status_label.config(text="Ready", fg="blue")
        self.tree_button.config(state=tk.DISABLED)
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, "./Lexical Analysis/result.txt")
        self.current_tokens = []
        self.analysis_successful = False

# ====================================================
# MAIN EXECUTION
# ====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxAnalyzerGUI(root)
    root.mainloop()