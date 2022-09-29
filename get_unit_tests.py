"""Unit tests retriever
    - [x] list all spec files under /app-frontends/apps
    - [] fetch all it(), test() with no test id in dir
"""
folder_path = "/home/cerebral/cs/app-frontends/apps/"

import glob
import mmap

specs = glob.glob(folder_path+'**/*.spec.ts', recursive=True)

for spec in specs:
    print("::::DEBUG::::SPEC_FILE::::", spec)
    # with open(spec, 'rb', 0) as file:
    with open(spec, 'rb') as file:
        f = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        # print(f.read())
        if f.read().find('it('):
            print("::::DEBUG::::TESTCASE::::", f.readline())
