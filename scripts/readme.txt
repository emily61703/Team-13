install.bat: Windows install script.
install.sh: Linux install script.

Do not move either out of /scripts/ directory!

Either script will download the needed dependencies to run the project.

For Linux, since that is what we care the most about:

Follow the instructions exactly! That means run: 'source venv/bin/activate && python3 main.py'
You have to tell the program where the dependencies are; that's done with the 'source venv/bin/activate' part.