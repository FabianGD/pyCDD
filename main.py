import os
from pathlib import Path
import shutil

from pyCDD.subprocessing import call_mwfn, make_cdd
from pyCDD.argparsing import get_data_to_process, interpret_args

def main():
    args = get_data_to_process()

    print(args)

    interpret_args(args)

if __name__ == "__main__":
    main()
