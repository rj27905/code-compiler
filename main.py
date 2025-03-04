import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import compiler

class CodeCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Code Compiler")
        self.root.geometry("800x600")

        # Language Selection
        self.language_var = tk.StringVar(value="Python")
        self.create_widgets()

    def create_widgets(self):
        # Language Dropdown
        tk.Label(self.root, text="Select Language:").pack(pady=5)
        language_dropdown = tk.OptionMenu(
            self.root, 
            self.language_var, 
            "Python", 
            "Java"
        )
        language_dropdown.pack(pady=5)

        # Code Input Area
        tk.Label(self.root, text="Enter your code:").pack(pady=5)
        self.code_input = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            width=80, 
            height=15
        )
        self.code_input.pack(pady=10)

        # Output Area
        tk.Label(self.root, text="Output:").pack(pady=5)
        self.output_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            width=80, 
            height=10
        )
        self.output_area.pack(pady=10)

        # Buttons
        compile_button = tk.Button(
            self.root, 
            text="Compile & Run", 
            command=self.compile_and_run
        )
        compile_button.pack(pady=10)

        file_button = tk.Button(
            self.root, 
            text="Open File", 
            command=self.open_file
        )
        file_button.pack(pady=5)

    def compile_and_run(self):
        """Compile and run the code based on selected language"""
        code = self.code_input.get("1.0", tk.END).strip()
        language = self.language_var.get()

        try:
            if language == "Python":
                result = compiler.compile_python(code)
            else:
                result = compiler.compile_java(code)
            
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Compilation Error", str(e))

    def open_file(self):
        """Open and read a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Python Files", "*.py"),
                ("Java Files", "*.java"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            with open(file_path, 'r') as file:
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, file.read())

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = CodeCompilerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()