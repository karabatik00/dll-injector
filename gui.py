import logging
import psutil
from tkinter import Tk, filedialog, Label, Entry, Button, Listbox, Scrollbar, messagebox, Frame, Toplevel, Menu, BooleanVar, StringVar
from tkinter.scrolledtext import ScrolledText
from injector import inject_dll
from config import list_processes, save_config, load_config, show_about, toggle_dark_mode, show_system_info, manual_pid_entry, auto_refresh_processes, show_help

logger = logging.getLogger()

def run_gui():
    global root, dll_path_entry, process_listbox, filter_var, dark_mode_var, top_frame, middle_frame, bottom_frame

    root = Tk()
    root.title("DLL Injector")
    root.geometry("739x574")
    root.resizable(False, False)  # Pencereyi sabitle

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Config", command=lambda: save_config(dll_path_entry, process_listbox))
    file_menu.add_command(label="Load Config", command=lambda: load_config(dll_path_entry, process_listbox))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    view_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="View", menu=view_menu)
    dark_mode_var = BooleanVar()
    view_menu.add_checkbutton(label="Dark Mode", onvalue=True, offvalue=False, variable=dark_mode_var, command=lambda: toggle_dark_mode(root, top_frame, middle_frame, bottom_frame, dark_mode_var))

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=lambda: show_help(root))
    help_menu.add_command(label="About", command=lambda: show_about(root))

    top_frame = Frame(root)
    top_frame.grid(row=0, column=0, padx=20, pady=10, sticky='ew')

    Label(top_frame, text="DLL Path:", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    dll_path_entry = Entry(top_frame, width=60)
    dll_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    Button(top_frame, text="Browse", command=select_dll, bg='#6200EE', fg='#FFFFFF', font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=10, sticky='e')

    middle_frame = Frame(root)
    middle_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')

    Label(middle_frame, text="Select Process:", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    filter_var = StringVar()
    filter_entry = Entry(middle_frame, textvariable=filter_var, width=30)
    filter_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    Button(middle_frame, text="Filter", command=lambda: list_processes(process_listbox, filter_var.get()), bg='#6200EE', fg='#FFFFFF', font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=10, sticky='e')

    scrollbar = Scrollbar(middle_frame, orient="vertical")
    process_listbox = Listbox(middle_frame, yscrollcommand=scrollbar.set, width=60, height=15)
    scrollbar.config(command=process_listbox.yview)
    process_listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')
    scrollbar.grid(row=1, column=2, padx=(0, 10), pady=10, sticky='ns')
    Button(middle_frame, text="Refresh", command=lambda: list_processes(process_listbox, filter_var.get()), bg='#6200EE', fg='#FFFFFF', font=('Arial', 12)).grid(row=2, column=1, padx=10, pady=10, sticky='e')

    bottom_frame = Frame(root)
    bottom_frame.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

    Button(bottom_frame, text="Inject", command=inject, bg='#03DAC6', fg='#000000', font=('Arial', 12), width=20).grid(row=0, column=0, padx=10, pady=10)
    Button(bottom_frame, text="Manual PID Entry", command=lambda: manual_pid_entry(root, dll_path_entry), bg='#03DAC6', fg='#000000', font=('Arial', 12), width=20).grid(row=0, column=1, padx=10, pady=10)
    Button(bottom_frame, text="System Info", command=lambda: show_system_info(root), bg='#03DAC6', fg='#000000', font=('Arial', 12), width=20).grid(row=0, column=2, padx=10, pady=10)

    root.grid_columnconfigure(0, weight=1)
    middle_frame.grid_columnconfigure(1, weight=1)
    middle_frame.grid_rowconfigure(1, weight=1)

    list_processes(process_listbox)
    auto_refresh_processes(root, process_listbox, filter_var)

    root.mainloop()

def select_dll():
    global dll_path_entry
    try:
        file_path = filedialog.askopenfilename(filetypes=[("DLL Files", "*.dll")])
        if file_path:
            dll_path_entry.delete(0, 'end')
            dll_path_entry.insert(0, file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to select DLL: {e}")
        logger.error(f"Failed to select DLL: {e}")

def inject():
    global dll_path_entry, process_listbox
    try:
        selected_process = process_listbox.get(process_listbox.curselection())
        pid = int(selected_process.split(' - ')[0])
        dll_path = dll_path_entry.get()
        if inject_dll(pid, dll_path):
            messagebox.showinfo("Success", "DLL Injected successfully")
        else:
            messagebox.showerror("Error", "DLL Injection failed")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to inject DLL: {e}")
        logger.error(f"Failed to inject DLL: {e}")
