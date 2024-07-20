# config.py
import ctypes
import logging
import json
import sys
from tkinter import filedialog, messagebox, Toplevel, Label, TclError, Entry, Button
from tkinter.scrolledtext import ScrolledText
import psutil
from injector import inject_dll

logger = logging.getLogger()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"Admin check failed: {e}")
        return False

def elevate_privileges():
    if not is_admin():
        print("Elevating to admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def list_processes(process_listbox, filter_text=""):
    try:
        process_listbox.delete(0, 'end')
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].endswith('.exe'):
                proc_entry = f"{proc.info['pid']} - {proc.info['name']}"
                if filter_text.lower() in proc_entry.lower():
                    process_listbox.insert('end', proc_entry)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list processes: {e}")
        logger.error(f"Failed to list processes: {e}")

def save_config(dll_path_entry, process_listbox):
    try:
        config = {
            'dll_path': dll_path_entry.get(),
            'selected_process': process_listbox.get(process_listbox.curselection())
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as config_file:
                json.dump(config, config_file)
            messagebox.showinfo("Success", "Configuration saved successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration: {e}")
        logger.error(f"Failed to save configuration: {e}")

def load_config(dll_path_entry, process_listbox):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as config_file:
                config = json.load(config_file)
                dll_path_entry.delete(0, 'end')
                dll_path_entry.insert(0, config['dll_path'])
                process_listbox.selection_clear(0, 'end')
                process_listbox.insert('end', config['selected_process'])
                messagebox.showinfo("Success", "Configuration loaded successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load configuration: {e}")
        logger.error(f"Failed to load configuration: {e}")

def show_about(root):
    about_window = Toplevel(root)
    about_window.title("About")
    about_window.configure(bg='#FFFFFF')
    Label(about_window, text="DLL Injector v2.0\nDeveloped by karabatik\nDiscord: karabatik", padx=10, pady=10, bg='#FFFFFF', font=('Arial', 12)).grid(row=0, column=0)

def toggle_dark_mode(root, top_frame, middle_frame, bottom_frame, dark_mode_var):
    def configure_widget(widget, bg_color, fg_color):
        try:
            widget.configure(bg=bg_color, fg=fg_color)
        except TclError:
            try:
                widget.configure(bg=bg_color)
            except TclError:
                pass

    if dark_mode_var.get():
        root.configure(bg='#2E2E2E')
        for frame in [top_frame, middle_frame, bottom_frame]:
            frame.configure(bg='#2E2E2E')
        for widget in root.winfo_children():
            configure_widget(widget, '#2E2E2E', '#FFFFFF')
    else:
        root.configure(bg='#F5F5F5')
        for frame in [top_frame, middle_frame, bottom_frame]:
            frame.configure(bg='#F5F5F5')
        for widget in root.winfo_children():
            configure_widget(widget, '#F5F5F5', '#000000')

def show_system_info(root):
    info = (
        f"CPU Usage: {psutil.cpu_percent()}%\n"
        f"Memory Usage: {psutil.virtual_memory().percent}%\n"
    )
    sys_info_window = Toplevel(root)
    sys_info_window.title("System Information")
    Label(sys_info_window, text=info, padx=10, pady=10).grid(row=0, column=0)

def manual_pid_entry(root, dll_path_entry):
    def on_inject():
        try:
            pid = int(pid_entry.get())
            dll_path = dll_path_entry.get()
            if not dll_path:
                raise ValueError("DLL path is empty")
            if inject_dll(pid, dll_path):
                messagebox.showinfo("Success", "DLL Injected successfully")
            else:
                messagebox.showerror("Error", "DLL Injection failed")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid PID or DLL path: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to inject DLL: {e}")
            logger.error(f"Failed to inject DLL: {e}")

    pid_window = Toplevel(root)
    pid_window.title("Enter PID")
    Label(pid_window, text="Enter PID:", padx=10, pady=10).grid(row=0, column=0)
    pid_entry = Entry(pid_window)
    pid_entry.grid(row=0, column=1, padx=10, pady=10)
    Button(pid_window, text="Inject", command=on_inject).grid(row=1, column=0, columnspan=2, pady=10)

def auto_refresh_processes(root, process_listbox, filter_var):
    list_processes(process_listbox, filter_var.get())
    root.after(10000, lambda: auto_refresh_processes(root, process_listbox, filter_var))  # Refresh every 10 seconds

def show_help(root):
    help_text = (
        "How to use DLL Injector:\n\n"
        "1. Select the DLL file you want to inject.\n"
        "2. Select the target process from the list or enter the PID manually.\n"
        "3. Click 'Inject' to perform the injection.\n"
        "4. Use the 'Save Config' and 'Load Config' options to save/load your settings.\n"
        "5. Toggle Dark Mode for a different UI theme.\n"
    )
    help_window = Toplevel(root)
    help_window.title("Help")
    help_window.geometry("500x300")
    help_text_box = ScrolledText(help_window, wrap='word', width=60, height=20)
    help_text_box.grid(row=0, column=0, padx=10, pady=10)
    help_text_box.insert('end', help_text)
    help_text_box.config(state='disabled')
