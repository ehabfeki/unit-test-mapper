"""Unit tests retriever
    - [x] list all spec files under path
    - [x] fetch all it(), test()
        - [x] del id > , 'C  > [C
        - [x] del nonrelevant
    - [x] trim testcase names > it( > @Test(
"""


import glob
import mmap
from cli_args_system import Args

args = Args(convert_numbers=False)

# "/home/cerebral/cs/app-frontends/apps/"
path = args.flag_str('p','path')

def units_fetcher():
    raw_units = []
    specs = glob.glob(path+'**/*.spec.ts', recursive=True)

    for spec in specs:
        with open(spec, 'rb') as file:
            f = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            for line in iter(f.readline, b""):
                if (b"it('") in line:
                    raw_units.append(line)
                if (b"@Test(") in line:
                    raw_units.append(line)
    return raw_units, len(raw_units)

def units_cleaner(raw_units):
    units = []

    for r_u in raw_units:
        if (b"$emit") in r_u:
            raw_units.remove(r_u)
        elif (b"submit(") in r_u:
            raw_units.remove(r_u)
        elif (b"commit(") in r_u:
            raw_units.remove(r_u)
        elif (b"split(") in r_u:
            raw_units.remove(r_u)
        elif (b"@Test(\n") in r_u:
            raw_units.remove(r_u)
        elif (b"[C") in r_u:
            raw_units.remove(r_u)
        elif (b", 'C") in r_u:
            raw_units.remove(r_u)
        else:
            if (b', async () => {') in r_u:
                r_u = r_u.replace(b', async () => {', b'')
                units.append(r_u.strip())
            elif (b', assert') in r_u:
                r_u_index = r_u.find(b', assert')
                r_u = r_u.rstrip(r_u[r_u_index:])
                units.append(r_u.strip())
            elif (b', () => {') in r_u: 
                r_u = r_u.replace(b', () => {', b'')
                units.append(r_u.strip())
            elif (b',  () => {') in r_u: 
                r_u = r_u.replace(b',  () => {', b'')
                units.append(r_u.strip())
            elif (b', () =>') in r_u: 
                r_u = r_u.replace(b', () =>', b'')
                units.append(r_u.strip())
            elif (b', fakeAsync(() => {') in r_u: 
                r_u = r_u.replace(b', fakeAsync(() => {', b'')
                units.append(r_u.strip())
            elif (b', doneFn => {') in r_u: 
                r_u = r_u.replace(b', doneFn => {', b'')
                units.append(r_u.strip())
            elif (b', done => {') in r_u: 
                r_u = r_u.replace(b', done => {', b'')
                units.append(r_u.strip())
            elif (b', async doneFn => {') in r_u: 
                r_u = r_u.replace(b', async doneFn => {', b'')
                units.append(r_u.strip())
            elif (b', async done => {') in r_u: 
                r_u = r_u.replace(b', async done => {', b'')
                units.append(r_u.strip())
            elif (b', async(() => {') in r_u: 
                r_u = r_u.replace(b', async(() => {', b'')
                units.append(r_u.strip())
            elif (b', {') in r_u: 
                r_u = r_u.replace(b', {', b'')
                units.append(r_u.strip())
            elif (b", '')") in r_u: 
                r_u = r_u.replace(b", '')", b'')
                units.append(r_u.strip())
            elif (b'Rendered);') in r_u: 
                r_u = r_u.replace(b'Rendered);', b'')
                units.append(r_u.strip())
            elif (b'Significant);') in r_u: 
                r_u = r_u.replace(b',Significant);', b'')
                units.append(r_u.strip())
            elif (b'Zero);') in r_u: 
                r_u = r_u.replace(b'Zero);', b'')
                units.append(r_u.strip())
            elif (b', () => expect(isFovExtendable(mockFovFilter)).toBeFalsy());') in r_u: 
                r_u = r_u.replace(b', () => expect(isFovExtendable(mockFovFilter)).toBeFalsy());', b'')
                units.append(r_u.strip())
            else:
                units.append(r_u.strip())
                
    return units, len(units)

def units_glamourer(units):
    glamourered_units = []
    for u in units:
        u = u.replace(b'it(', b'')
        u = u.replace(b'@Test(', b'')
        glamourered_units.append(u)
    return glamourered_units, len(glamourered_units)

if __name__ == "__main__":
    raw_units, raw_units_total = units_fetcher()
    units, units_total = units_cleaner(raw_units)
    glamourered_units, glamourered_units_total = units_glamourer(units)

    f = open("units.log", "a")
    
    for g_u in glamourered_units:
        f.write(g_u.decode("utf-8"))
        f.write("\n")

    print("raw_units_total", raw_units_total)
    print("units_total", units_total)
    print("glamourered_units_total", glamourered_units_total)

    f.close()