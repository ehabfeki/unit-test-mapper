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

anomalies = [b"$emit", b"submit(", b"commit(", b"split(", b"@Test(\n", b"[C", b", 'C"]
snippets = [b'it(', b'@Test(', b', async () => {', b', assert', b', () => {', b',  () => {', b', () =>', b', fakeAsync(() => {', b', doneFn => {', b', done => {', b', async doneFn => {', b', async done => {', b', async(() => {', b', {', b", '')", b'Rendered);', b'Significant);', b'Zero);', b' expect(isFovExtendable(mockFovFilter)).toBeFalsy());', b', function () {});', b'EmptyContentIs', b'LoaderIs', b'ErrorBoundaryIs', b'FiltersBarMainIs', b'FiltersBarDrilldownIs', b'FiltersBarPageIs', b'ComponentIs', b'ComponentIsNot', b'LineChartIs', b", '' skip: true })", b'// ', b"t close menu'"]

def units_fetcher(path):
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

def anomalies_remover(raw_units):
    units = []
    for a in anomalies:
        raw_units = [r_u for r_u in raw_units if a not in r_u ]
    units = raw_units
    return units, len(units)

def snippets_remover(units):
    for idx in range(len(units)):
        for s in snippets:
            if s in units[idx]:
                units[idx] = units[idx].replace(s, b'')
        units[idx] = units[idx].strip()
    return units

if __name__ == "__main__":
    args = Args(convert_numbers=False)

    # Example: "/home/cerebral/cs/app-frontends/apps/"
    path = args.flag_str('p','path')

    raw_units, raw_units_total = units_fetcher(path)
    units, units_total = anomalies_remover(raw_units)
    units = snippets_remover(units)

    print("raw_units_total", raw_units_total)
    print("units_total", units_total)

    f = open("units.log", "a")
    
    for u in units:
        f.write(u.decode("utf-8"))
        f.write("\n")

    f.close()