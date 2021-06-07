# convertSyms.py by shibboleet
# takes in an old game.x using physical addresses and converts them all to virtual
# outputs and replaces files/game.x
# note -- this should only be ran once!

with open("clean_game.x", "r") as f:
    lines = f.readlines()

output_file = []

output_file.append("/* ADDRESSES CONVERTED TO VIRTUAL IN THIS FILE! */\n")

for line in lines:
    
    if " = " not in line:
        output_file.append(line)
        continue

    line_split = line.split(" = ")

    # left side is symbol
    # right side is address
    sym = line_split[0].strip()
    addr = line_split[1].strip().replace(";", "")

    # this has no address, as far as we're concerned
    # so we can  just append it and move on
    if addr == "__deleted_virtual_called":
        output_file.append(line)
        continue

    # here we do the conversion from physical => virtual
    addr_int = int(addr, 0)

    if 0xEBC0000 <= addr_int < 0x10502200:
        addr_int -= 0xCBC0000
    else:
        addr_int -= 0x502200

    # and now we output our line
    output_file.append(f"\t{sym} = {hex(addr_int)};\n")

with open("../files/game.x", "w") as w:
    w.writelines(output_file)