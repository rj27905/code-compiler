import os
import subprocess
import sys
import tempfile
import re

def compile_python(code):
    """Compile and run Python code"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        # Run Python code with timeout
        result = subprocess.run(
            [sys.executable, temp_file_path], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        # Check for errors or output
        if result.returncode == 0:
            return result.stdout or "Code executed successfully with no output."
        else:
            return f"Error:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Execution timed out. Code took too long to run."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

def compile_java(code):
    """Compile and run Java code"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Find a class name in the code
        class_name = find_java_class_name(code)
        if not class_name:
            class_name = "MainClass"

        # Write Java file
        java_file_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(java_file_path, 'w') as java_file:
            # Ensure class name matches filename
            if not code.startswith(f"public class {class_name}"):
                code = f"public class {class_name} {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}"
            java_file.write(code)

        try:
            # Compile Java code
            compile_result = subprocess.run(
                ['javac', java_file_path], 
                capture_output=True, 
                text=True, 
                cwd=temp_dir
            )

            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"

            # Run Java code
            run_result = subprocess.run(
                ['java', '-cp', temp_dir, class_name], 
                capture_output=True, 
                text=True, 
                timeout=10
            )

            if run_result.returncode == 0:
                return run_result.stdout or "Code executed successfully with no output."
            else:
                return f"Execution Error:\n{run_result.stderr}"
        except subprocess.TimeoutExpired:
            return "Execution timed out. Code took too long to run."
        except Exception as e:
            return f"Unexpected error: {str(e)}"

def find_java_class_name(code):
    """Find the first public class name in Java code"""
    match = re.search(r'public\s+class\s+(\w+)', code)
    return match.group(1) if match else None