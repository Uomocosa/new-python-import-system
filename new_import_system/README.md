# PROJECT STRUCUTURE

- `lele\main_*.py` — HIGHER LEVEL WORKFLOWS. ***YOU PROBABLY ONLY NEED TO LOOK AT THESE, INGORING THE REST OF THE REPO***. Each main should have a clear name, after installing this repo you _should_ be able to run each of these mains, from the cli as a standard command: `<file_name_without_starting_main> <args_if_any>`. (_~Ex.:_ `hello_world` will run `main_hello_world.py`)
- `lele\` — ALL MY CODE. Most python files in this folder and subfolders have a python function with the same name as the file, and they should have a test_ in it testing that function. ***YOU CAN USE ANY OF MY FUNCTIONS BY COPYING THE IMPORTS AND THE test_***.
- `datasets\` — DATASETS USED TO TRAIN THE MODELS.
- `output_models\` — MODELS I'VE TRAINED.
- `_helper_dir\` — IGNORE. It contains models I've downloaded and other stuff usefull to this repo, but you should ignore it.

> ***Note***: most `__init__.py` files are **NOT-EMPTY**.

***IMPORTANT***: You might have to change the links in the 'pyproject.toml' file for your specific machine. To do so: instad of just doing 'pip install -e .' Do `pip install -e . --extra-index-url https://download.pytorch.org/whl/<specific cuda number>`, find more on the official torch site. 

----
# Windows Client (Setup)

0. [Install python 3.11.1].(https://www.python.org/downloads/release/python-3111/) (_Newer versions might work, but were not tested!_)
1. `py -3.11 -m venv .lele-3.11`
2. `.lele-3.11\Scripts\activate.bat`
3. INSTALL YOUR SPECIFIC PYTORCH LIBRARY, for me is: `pip3 install torch torchvision`
4. `pip install -e <path_to_this_folder>`
5. open this folder with vscode (I had problems with vscode, solved them by opening it as adminastrator - Windows)
6. Ctrl+Shift+P >> "Python: Select Interpreter" >> If you see the just created venv click it, otherwise search it with "Enter interpreter path..."
7. To test a single file use Ctrl+Shift+P >> "Task: Run Task" >> "Pytest: Run tests in current file"
8. To test the whole package: use Ctrl+Shift+P >> "Task: Run Task" >> "Pytest: Pytest: Run ALL tests"
9. (_Optinal_) configure keybinding to these tasks: Ctrl+Shift+P >> "Preferences: Open Keyboard Shortcut (JSON)"
```json
{
    { 
        "key": "ctrl+b",
        "command": "workbench.action.tasks.runTask",
        "args": "Cargo Test Current Lib File",
        "when": "editorTextFocus && editorLangId == rust"
    },
    { 
        "key": "ctrl+b",
        "command": "workbench.action.tasks.runTask",
        "args": "Pytest: Run tests in current file",
        "when": "editorTextFocus && editorLangId == python"
    },
}
```
10. (_Optinal_) These are my .vscode/settings.json
```json
{
    "editor.detectIndentation": true,
    "editor.insertSpaces": true,
    "workbench.startupEditor": "none", // Stops the "Welcome" page from opening every time you launch VS Code.

    "git.autofetch": true,
    "git.confirmSync": false, // disables the confirmation pop-up.

    "python.terminal.activateEnvironment": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**.egg-info": true,
    },
    "python.REPL.enableREPLSmartSend": false,

    "SSH_USER": "my_username",
    "SSH_HOST": "host_address",
}
```

----
# SSH Client (Setup)

1. `curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
2. `bash Miniconda3-latest-Linux-x86_64.sh`
3. `./miniconda3/bin/conda init`
4. `exec "$SHELL"`
5. `conda create --name .lele-3.11 python=3.11`
6. `conda activate .lele-3.11`
7. INSTALL YOUR SPECIFIC PYTORCH LIBRARY, for me is: `pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu117`
8. `git clone https://github.com/Uomocosa/lele-py`
9. `cd lele-py`
10. `pip install -e .`
11. `main_`

# SSH Client (My Workflow) - This is also in the task "SSH DEPLOY AND RUN 'main_.py'"

0. `cd lele-py`
1. `git fetch origin`
2. `git reset --hard origin/main`
3. `chmod +x ssh_run_main_on_server.sh`
4. `./ssh_run_main_on_server.sh`
