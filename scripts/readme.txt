install.bat: Windows install script.
install.sh: Linux install script.

Do not move either out of /scripts/ directory!

---< For Linux, since that is what we care the most about... >---

Follow the instructions exactly! To run this project on the Debain Virtual Machine, open the terminal and:
    1. Navigate to /scripts/
    2. Run the Linux script with: './install.sh' or 'bash install.sh'
    3. Once completed, navigate to the main project directory.
    4. Run the command: 'source venv/bin/activate && python3 main.py'

To be 100% clear:
  'source venv/bin/activate': Tells the computer to use the virtual environment with all the dependencies you just downloaded
  'python3 main.py': Runs the program
