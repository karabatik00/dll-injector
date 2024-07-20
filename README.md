# DLL Injector

## Overview

DLL Injector is a Python application designed to inject DLL files into running processes. The application provides both a graphical user interface (GUI) and a command-line interface (CLI) for users to select the target process and DLL file, and perform the injection. It includes various features such as process listing, manual PID entry, dark mode, and configuration saving/loading.

## Features

- Graphical User Interface (GUI) for easy DLL injection
- Command-Line Interface (CLI) for advanced users
- List running processes with filtering options
- Manual PID entry for precise targeting
- Dark mode for comfortable usage in low light conditions
- Save and load configuration files
- System information display

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/dll-injector.git
    cd dll-injector
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    - For GUI:
      ```sh
      python main.py
      ```
    - For CLI:
      ```sh
      python main.py --pid <PID> --dll <path_to_dll>
      ```

## Usage

### Graphical User Interface (GUI)

1. Run the GUI application:
    ```sh
    python main.py
    ```

2. Use the "Browse" button to select the DLL file you want to inject.

3. Select the target process from the list or use the "Manual PID Entry" button to enter the PID manually.

4. Click "Inject" to perform the injection.

5. Use the "Save Config" and "Load Config" options to save and load your settings.

6. Toggle Dark Mode for a different UI theme.

### Command-Line Interface (CLI)

1. Run the CLI application with the required arguments:
    ```sh
    python main.py --pid <PID> --dll <path_to_dll>
    ```

2. The application will perform the DLL injection and provide feedback in the terminal.

## Configuration

You can save your current configuration (selected DLL and process) to a JSON file using the "Save Config" button in the GUI. Similarly, you can load a previously saved configuration using the "Load Config" button.

## Screenshots

![Main GUI](![image](https://github.com/user-attachments/assets/312b3bc9-c75a-4aee-b441-bfa6c2873dc4)
)

## Requirements

- Python 3.x
- Required libraries are listed in the `requirements.txt` file

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any feature enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the project maintainer at your_email@example.com.
