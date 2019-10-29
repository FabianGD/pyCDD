import os
from pathlib import Path
import shutil

from pyCDD.subprocessing import call_mwfn, make_cdd
from pyCDD.argparsing import get_data_to_process

def main():
    args = get_data_to_process()
    print(args)


if __name__ == "__main__":
    main()
