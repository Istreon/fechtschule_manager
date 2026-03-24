# Fechtschule manager

A tool to manage the Brest AMHE annual tournament, the Fechtschule.<br>
It allows adding participants, clubs and weapons and to register matches. Registered matches can be modified in case of human error.
<br>
<img src="./Documentation/registering_interface.png">
<br>

Rankings are shown in real time, and can be exported in .csv files, as well as the list of matches.<br>
A generated summary of the tournament can be exported in a .txt file.
<br>
<img src="./Documentation/ranking_interface.png">
<br>

## Using the virtual environment

Using python 3.13.2 in powershell, install the virtual environment:
```bash
python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```


## Build the app 
Use the [```build.bat```](./build.bat)  script to build the app.

## Run the app without build
Use the [```run.bat```](./run.bat) script to run the app.