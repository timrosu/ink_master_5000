# ink_master_5000
 simple script that informs you about remaining ink supply 
 # How does it work?
 It runs ipp script with `ipptool` and returns formatted list in this form: `Black Ink Cartidge: 69%`.
 # Requirements
 - python
 - ipptool
 - POSIX compliant system (for saving entered preferences)
# Usage
Copy/download `printscript.py` file and run it with `python printscript.py`. To register new printer delete `$XDG_CONFIG_HOME/inkscript` directory.
