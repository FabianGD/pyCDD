import os
from pathlib import Path
import shutil

from pyCDD.subprocessing import call_mwfn, make_cdd
from pyCDD.argparsing import get_data_to_process

def main():
    args = get_data_to_process()
    make_cdd("/scratch/data/T123/pysisyphus/2_S5/image_000.000.gaussian16.fchk", "/scratch/data/T123/pysisyphus/2_S5/image_000.000.gaussian16.log", 5, inc=0)
    print(args)


if __name__ == "__main__":
    main()
