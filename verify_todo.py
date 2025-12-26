
import subprocess
import time

def run_test():
    # Start the application process
    process = subprocess.Popen(
        ['python', 'src/todo.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=r'c:\Users\Admin\Desktop\TODO\hackathon-todo'
    )

    # Helper function to send commands
    def send_command(cmd):
        print(f"Sending: {cmd}")
        process.stdin.write(cmd + "\n")
        process.stdin.flush()
        time.sleep(0.1)  # small delay for processing

    try:
        # 1. List empty
        send_command("list")
        
        # 2. Add tasks
        send_command("add Buy Milk")
        send_command("add Walk Dog")
        
        # 3. List
        send_command("list")
        
        # 4. Wait for output to capture IDs manually or via logic? 
        # Since this is a simple run, let's just do a series of ops blindly and check output later, 
        # OR we can just rely on the user to run it. 
        # But wait, I can't interactively parse efficiently in this simple script without complexity.
        # I'll just run a sequence and print the output.
        
        send_command("add Task 3")
        send_command("exit")
        
        stdout, stderr = process.communicate(timeout=5)
        print("STDOUT:", stdout)
        print("STDERR:", stderr)

    except Exception as e:
        print(f"Test failed: {e}")
        process.kill()

if __name__ == "__main__":
    run_test()
