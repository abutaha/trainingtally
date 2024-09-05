
# TrainingTally Athletes and Gym Management Web Application

TrainingTally is a sample web application built using Python, Flask, and SQLAlchemy. It helps manage gym memberships, competitions, track athletes and log training schedules. You can install and run the application on Ubuntu Linux or Windows. A pre-built `.exe` file is also available for Windows users who want to get started quickly.

## Table of Contents
- [Running the Pre-Created .exe on Windows](#running-the-pre-created-exe-on-windows)
- [Requirements](#requirements)
- [Installation on Ubuntu Linux](#installation-on-ubuntu-linux)
- [Installation on Windows](#installation-on-windows)
- [Running the Application](#running-the-application)
- [Running via Docker](#running-via-docker)
- [License](#license)

## Running the Pre-Created .exe on Windows

If you want to get started quickly on Windows, you can use the pre-built `.exe` file without installing Python or other dependencies:

1. **Download the `.exe` file:**
   - [Download Windows Executable version](https://github.com/abutaha/trainingtally/releases/download/v1-demo/trainingtally.exe)

2. **Run the `.exe`:**
   - Double-click the `.exe` to start the application.
   - Open your browser and access the application on `http://127.0.0.1:5000/`.
   - Access `http://127.0.0.1:5000/create-database` to create the local database file and load initial data.

## Requirements

Ensure you have the following installed:
- Python 3.8+
- Pip
- Virtualenv (optional but recommended)
- Flask 2.0+
- SQLAlchemy

## Installation on Ubuntu Linux

1. **Update System Packages:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```

2. **Install Python and Pip:**
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Clone the Repository:**
   ```bash
   git clone https://github.com/abutaha/trainingtally.git
   cd trainingtally
   ```

4. **Create a Virtual Environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application:**
   ```bash
   flask --app trainingtally.py --debug run
   ```

   The application will now be running on `http://127.0.0.1:5000/`.

   If you want to allow remote users access it, you need to make it listen on `0.0.0.0`

   ```bash
   flask --app trainingtally.py --debug run --host=0.0.0.0
   ```

7. **Initiate the database:**
   
   Access `http://127.0.0.1:5000/create-database` to create the local database file and load initial data.

## Installation on Windows

1. **Install Python and Pip:**
   - Download and install Python from [python.org](https://www.python.org/downloads/windows/).
   - Ensure you check "Add Python to PATH" during installation.

2. **Clone the Repository:**
   Open the Command Prompt or PowerShell:
   ```bash
   git clone https://github.com/abutaha/trainingtally.git
   cd trainingtally
   ```

3. **Create a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```bash
   flask --app trainingtally.py --debug run
   ```

   The application will now be running on `http://127.0.0.1:5000/`.
   If you want to allow remote users access it, you need to make it listen on `0.0.0.0`

   ```bash
   flask --app trainingtally.py --debug run --host=0.0.0.0
   ```

6. **Initiate the database:**
   
   Access `http://127.0.0.1:5000/create-database` to create the local database file and load initial data.


## License

This project is licensed under the Apache2 License - see the [LICENSE](LICENSE) file for details.

