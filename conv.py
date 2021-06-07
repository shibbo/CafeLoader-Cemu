def getHexOffs(addr):
    if addr >= 0x10502200:
        return 0x00502200
    if addr >= 0x0EBC0000:
        return 0x0CBC0000
    return 0x0

def getHexOffsInv(addr):
    if addr >= 0x10000000:
        return 0x00502200
    if addr >= 0x02000000:
        return 0x0CBC0000
    
    return 0x0

def convGameMapToVirt():
    with open("../files/syms/game_phys.x", "r") as f:
        lines = f.readlines()

    output_file = []

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

        offs = getHexOffs(addr_int)

        addr_int = addr_int - offs

        # and now we output our line
        output_file.append(f"\t{sym} = {hex(addr_int)};\n")

    with open("../files/syms/game_virt.x", "w") as w:
        w.writelines(output_file)

def convGameMapToPhys():
    with open("../files/syms/game_virt.x", "r") as f:
        lines = f.readlines()

    output_file = []

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

        offs = getHexOffsInv(addr_int)

        addr_int = addr_int + offs
            
        lolHack = hex(addr_int).replace("0x", "").upper()

        # and now we output our line
        output_file.append(f"\t{sym} = 0x{lolHack};\n")

    with open("../files/syms/game_phys.x", "w") as w:
        w.writelines(output_file)