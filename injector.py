import ctypes
import logging

logger = logging.getLogger()

def inject_dll(pid, dll_path):
    try:
        if not dll_path.lower().endswith('.dll'):
            raise ValueError("Selected file is not a DLL.")
        
        dll_path_bytes = dll_path.encode('utf-8')
        kernel32 = ctypes.windll.kernel32
        h_process = kernel32.OpenProcess(0x1F0FFF, False, pid)

        if not h_process:
            raise Exception("Failed to open process")

        arg_address = kernel32.VirtualAllocEx(h_process, 0, len(dll_path_bytes), 0x3000, 0x40)
        if not arg_address:
            raise Exception("Failed to allocate memory in target process")

        written = ctypes.c_size_t(0)
        if not kernel32.WriteProcessMemory(h_process, arg_address, dll_path_bytes, len(dll_path_bytes), ctypes.byref(written)):
            raise Exception("Failed to write DLL path to target process memory")

        h_kernel32 = kernel32.GetModuleHandleW("kernel32.dll")
        h_loadlib = kernel32.GetProcAddress(h_kernel32, b"LoadLibraryA")

        h_thread = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, None)
        if not h_thread:
            raise Exception("Failed to create remote thread in target process")

        kernel32.WaitForSingleObject(h_thread, 0xFFFFFFFF)
        kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
        kernel32.CloseHandle(h_thread)
        kernel32.CloseHandle(h_process)
        logger.info("Successfully injected %s into process %d", dll_path, pid)
        return True
    except Exception as e:
        logger.error(f"Error during DLL injection: {e}")
        return False
