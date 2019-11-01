import os
import shutil
from pathlib import Path
from subprocess import Popen, PIPE

# from dask.distributed import Client

def viable_vmdrc(file):
    with open(file, "r") as f:
        rawdata = f.read()
        if "after idle {" in rawdata:
            return True
        else:
            return False


def find_vmdrc(cwd=Path(".")):
    here = list(cwd.glob("*vmdrc*"))
    home = list(Path(os.environ["HOME"]).glob("*vmdrc*"))

    if len(here) == 1:
        print("found a file called vmdrc here. Using this.")
        if viable_vmdrc(here[0]):
            return here[0]
        else:
            print("File {} is not recognized as a viable VMDRC file, continuing".format(here[0]))

    elif len(here) >= 1:
        print("Found more than one file called 'vmdrc' file, not sure which one to take.")
        for file in here:
            if viable_vmdrc(file):
                return file
            else:
                print(f"File {file} is not recognized as a viable VMDRC file, continuing")
                continue

    # Checking the home directory for a file called ".vmdrc"
    print("Nothing viable was found in the cwd, trying the $HOME directory")

    if (len(home) == 1) and viable_vmdrc(home[0]):
        return home[0]

    elif len(home) >= 1:
        print("Found more than one file called 'vmdrc' file, not sure which one to take.")
        for file in home:
            if viable_vmdrc(file) and "bak" not in file.name:
                return file
            else:
                print(f"File {file} is rejected as VMDRC file, continuing.")
                continue

    # Base case
    print("No viable vmdrc file was found, sorry.")
    return None


def provide_vmd_startup(file, cwd=Path(".")):
    """
    File takes a vmdrc file and prepares it for use as a startup script,
    basically removing the "after idle" tag and the corresponding brackets
    """

    with open(file, "r") as rf:
        while True:
            # Consume lines until the "after idle" tag
            line = rf.readline()
            if "after idle {" in line:
                break

        raw_str = rf.readlines()[:-3]

    writefile = cwd / "vmd_startup.vmd"

    with open(writefile, "w") as wf:
        wf.write("".join(raw_str))

    return writefile


def call_vmd(file_info, vmd_basecmd="vmd", vmd_template=Path("data/VMD.tcl"), cwd=Path(".")):
    """
    Modify the jinja2-templated VMD template file, get a viable vmd startup file and extract
    the viewpoint from the visualisation state file
    """
    # TODO

    vmd_scriptfile = Path("data/VMD.tcl")


    vmd_cmd = ["vmd", ]

    return


def call_mwfn(inp_fn, stdin, cwd=None):
    """
    Function strongly based on eljost's pysisyphus.wrapper.mwfn.make_cdd
    https://github.com/eljost/pysisyphus/blob/dev/pysisyphus/wrapper/mwfn.py

    """

    if cwd is None:
        cwd = Path(".")
    mwfn_cmd = ["Multiwfn", inp_fn]
    proc = Popen(
        mwfn_cmd, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd
    )
    stdout, stderr = proc.communicate(stdin)
    proc.terminate()
    return stdout, stderr


def make_cdd(inp_fn, log, state, cwd=".", inc=None, keep=True, quality=2):
    """
    Function strongly based on eljost's pysisyphus.wrapper.mwfn.make_cdd
    https://github.com/eljost/pysisyphus/blob/dev/pysisyphus/wrapper/mwfn.py

    Create CDD cube in cwd.
    Parameters
    ----------
    inp_fn : str
        Filename of a .molden/.fchk file.
    log : str
        Filename of the .log file.
    state : int
        CDD cubes will be generated up to this state.
    cwd : str or Path
        If a different cwd should be used.
    inc : int
        Increment value, default is no increment
    keep : bool
        Wether to keep electron.cub and hole.cub, default is False.
    quality : int
        Quality of the cube. (1=low, 2=medium, 3=high).
    """

    assert quality in (1, 2, 3)

    stdin = f"""18
    1
    {log}
    {state}
    1
    {quality}
    10
    1
    11
    1
    15
    """

    stdout, stderr = call_mwfn(inp_fn, stdin, cwd=cwd)

    cwd = Path(cwd)

    cube_fns = ("electron.cub", "hole.cub", "CDD.cub")
    if not keep:
        # always keep CDD.cub
        for fn in cube_fns[:2]:
            full_path = cwd / fn
            os.remove(full_path)

    # Rename cubes according to the current state
    new_paths = list()

    for fn in cube_fns:
        old_path = cwd / fn
        root, ext = os.path.splitext(fn)
        if not inc:
            new_path = cwd / f"S_{state:03d}_{inc}_{root}{ext}"
        else:
            new_path = cwd / f"S_{state:03d}_{root}{ext}"

        try:
            shutil.copy(old_path, new_path)
            os.remove(old_path)
            new_paths.append(new_path)
        except FileNotFoundError:
            pass

    return new_paths
