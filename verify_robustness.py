
import sys
import os
import io

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from todo import TodoApp, STATUS_COMPLETED, STATUS_PENDING

def test_app():
    print("Starting Enhanced Verification...")
    app = TodoApp()
    
    # Capture stdout
    captured_output = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output

    try:
        # TEST 1: ADD & ID UNIQUENESS
        # Add two tasks
        app.handle_add(["Task", "1"])
        output = captured_output.getvalue()
        
        import re
        ids = re.findall(r'\[([a-f0-9\-]+)\]', output)
        if len(ids) < 1:
            print("FAILED: No ID found in add output", file=original_stdout)
            return
        id1 = ids[-1]
        
        captured_output.truncate(0); captured_output.seek(0)
        
        app.handle_add(["Task", "2"])
        output = captured_output.getvalue()
        ids = re.findall(r'\[([a-f0-9\-]+)\]', output)
        id2 = ids[-1]
        
        if id1 == id2:
            print("FAILED: IDs are not unique", file=original_stdout)

        # TEST 2: EMPTY TITLE
        captured_output.truncate(0); captured_output.seek(0)
        app.handle_add([])
        if "Error: Missing title" not in captured_output.getvalue():
            print("FAILED: Empty args not caught", file=original_stdout)
            
        captured_output.truncate(0); captured_output.seek(0)
        app.handle_add(["   "])
        if "Error: Title cannot be empty" not in captured_output.getvalue():
            print("FAILED: Whitespace title not caught", file=original_stdout)

        # TEST 3: ALREADY COMPLETED
        captured_output.truncate(0); captured_output.seek(0)
        app.handle_complete([id1]) # First completion
        
        captured_output.truncate(0); captured_output.seek(0)
        app.handle_complete([id1]) # Second completion
        if "Task is already completed" not in captured_output.getvalue():
            print("FAILED: Did not catch already completed task", file=original_stdout)

        # TEST 4: UPDATE STATUS vs TITLE
        captured_output.truncate(0); captured_output.seek(0)
        app.handle_update([id2, "COMPLETED"]) # Case insensitive status
        if app.tasks[id2].status != STATUS_COMPLETED:
            print(f"FAILED: Case insensitive status update failed. Got {app.tasks[id2].status}", file=original_stdout)

        captured_output.truncate(0); captured_output.seek(0)
        app.handle_update([id2, "New Title"]) # Title update
        if app.tasks[id2].title != "New Title":
            print("FAILED: Title update failed", file=original_stdout)

        # TEST 5: SHOW INCLUDES UPDATED_AT
        captured_output.truncate(0); captured_output.seek(0)
        app.handle_show([id2])
        if "Updated At:" not in captured_output.getvalue():
            print("FAILED: Show does not include Updated At", file=original_stdout)
            
        # TEST 6: UNKNOWN COMMAND
        captured_output.truncate(0); captured_output.seek(0)
        app.process_command("foo bar")
        if "Unknown command: 'foo'" not in captured_output.getvalue():
            print("FAILED: Unknown command handling", file=original_stdout)

        print("ALL ENHANCED TESTS PASSED!", file=original_stdout)

    except Exception as e:
        print(f"EXCEPTION: {e}", file=original_stdout)
        import traceback
        traceback.print_exc(file=original_stdout)
    finally:
        sys.stdout = original_stdout

if __name__ == "__main__":
    test_app()
