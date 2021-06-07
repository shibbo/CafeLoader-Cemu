from elf import round_up

symbols = {}
diffs = []

# new function -- this takes the game.x given and will convert all of those addresses back to physical - shibbo
def convertToPhysical():
    with open("../files/game.x", "r") as f:
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

        if addr == "__deleted_virtual_called":
            output_file.append(line)
            continue

        addr_int = int(addr, 0)

        if 0xEBC0000 <= addr_int < 0x10502200:
            addr_int += 0x00502200
        else:
            addr_int += 0xCBC0000

        output_file.append(f"\t{sym} = {hex(addr_int)};\n")

    with open("../files/game_physc.x", "w") as w:
        w.writelines(output_file)

def parseAddrFile(lines):
    global text, data
    for line in lines:
        line = line.strip().replace(' ', '')

        if not line or line.startswith('#'):
            pass
        
        elif line.startswith('-'):
            symentry = line.split('=')
            symbol, address = symentry[0][1:], eval(symentry[1])
            symbols[symbol] = address

        else:
            old, new = line.split(':Addr')
            starthex, endhex = old.split('-')
            start = int(starthex, 16)
            end = int(endhex, 16)
            diff = eval(new)
            diffs.append((start, end, diff))

    symbols['textAddr'] = round_up(symbols['textAddr'], 32)
    symbols['dataAddr'] = round_up(symbols['dataAddr'], 32)
    assert symbols['textAddr'] < symbols['dataAddr']

def loadAddrFile(name):
    global region
    region = name
    
    symbols.clear()
    del diffs[:]

    with open('addr_%s.txt' %name) as f:
        parseAddrFile(f.readlines())

def convert(address, fixWriteProtection=False):
    for diff in diffs:
        if diff[0] <= address < diff[1]:
            addr = address + diff[2]
            return addr

    raise ValueError("Invalid or unimplemented address: 0x%x" %address)

def convertTable(oldfile, newfile):
    with open(oldfile) as f:
        lines = f.readlines()
    
    newlines = []
    for line in lines:
        line = line.strip()
        
        if line.endswith(';'):
            name, addr = line.strip(';').split(' = ')

            if name == '__deleted_virtual_called':
                __deleted_virtual_called = eval(addr)
            
            newaddr = convert(eval(addr))
            newlines.append('%s = 0x%x;\n' %(name, newaddr))
        else:
            newlines.append(line+'\n')

    with open(newfile, 'w') as f:
        f.writelines(newlines)
