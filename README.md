# CafeLoader Project Compiler (Cemu Edition)
A set of scripts to compile projects made for [CafeLoader](https://github.com/aboood40091/CafeLoader), but to be loaded on Cemu. With help from [Kinnay](https://github.com/Kinnay) and [Exzap](https://www.reddit.com/user/Exzap/).  
An example can be found [here](https://github.com/aboood40091/NSMBU-haxx). The major difference between this repository and the original is that this one uses virtual addresses in the symbol table instead of physical.

## Usage
You will need [MULTI GreenHills Software](http://letmegooglethat.com/?q=%22MULTI-5_3_27%22) and [wiiurpxtool](https://github.com/0CBH0/wiiurpxtool/releases) to build projects using these scripts. (set their paths in compiler_cemu.py)  
PyYAML and pyelftools are also required; get them using pip:  
`pip install PyYAML`  
`pip install pyelftools`