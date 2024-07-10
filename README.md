# ink_master_5000
 simple script that informs you about remaining ink supply 
 # How does it work?
 It runs ipp script with `ipptool` and returns formatted list.
 
 Output:
 ```
 Black Ink Cartridge: 4%
 Yellow Ink Cartridge: 98%
 Cyan Ink Cartridge: 6%
 Magenta Ink Cartridge: 46%
 ```
 # Requirements
 - python
 - ipptool
 - POSIX compliant system (for saving entered preferences)
# Usage
Copy/download `printscript.py` file and run it with `python printscript.py`. To register new printer delete `$XDG_CONFIG_HOME/inkscript` directory.
