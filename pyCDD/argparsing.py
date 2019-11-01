import jinja2


def get_data_to_process():

    from pathlib import Path
    import argparse

    parser = argparse.ArgumentParser(
        description="Process batch QC data for CDDs. (calculation via Multiwfn, plotting with VMD)"
    )
    parser.add_argument(
        "--inputdir",
        "-i",
        metavar="INDIR",
        help="Directory of the input data, default '%(default)s'",
        type=str,
        default=".",
    )
    parser.add_argument(
        "--outputdir",
        "-o",
        metavar="OUTDIR",
        help="Directory of the output data, default '%(default)s'",
        type=str,
        default=".",
    )
    parser.add_argument(
        "states",
        metavar="N",
        type=int,
        nargs="+",
        help="Excited state that you want the CDD. Can also be a more than one state.",
    )
    parser.add_argument(
        "--fchktemplate",
        dest="fchk_tmp",
        help="String template stating variable parts of the \
              .fchk/.molden filename, default '%(default)s', rendered to '*.fchk'",
        type=str,
        default="YYY.fchk",
    )
    parser.add_argument(
        "--logtemplate",
        dest="log_tmp",
        help="String template stating variable parts of the .log \
              filename, default '%(default)s', rendered to '*.fchk'",
        type=str,
        default="YYY.log",
    )
    parser.add_argument(
        "--vmdtemplate",
        dest="log_jinja",
        help="VMD template file (incorporating 'viewpoint', 'orbs', 'cdddens' keywords) \
              filename, default '%(default)s'",
        type=str,
        default="./VMD.tcl",
    )
    parser.add_argument(
        "--multiwfn",
        "-w",
        dest="mwfn_cmd",
        help="Multiwfn executable, default '%(default)s'",
        default="Multiwfn",
        type=str,
    )
    parser.add_argument(
        "--vmd",
        "-v",
        dest="vmd_cmd",
        help="VMD executable, default '%(default)s'",
        default="vmd",
        type=str,
    )
    parser.add_argument(
        "--vmdstate",
        dest="vmd_statefile",
        help="VMD visualisation state file name, optional",
        type=str,
    )

    args = vars(parser.parse_args())
    cwd = Path.cwd()

    # Build proper paths from the args
    # Recognizes relative and absolute paths
    args["inputdir"] = cwd / Path(args["inputdir"])
    args["outputdir"] = cwd / Path(args["outputdir"])
    args["outputdir"] = cwd / Path(args["outputdir"])

    return args

def interpret_args(args):
    """
    Build a list of input objects used to convey information to the multiwfn and vmd facilities
    """
    idir = args["inputdir"]
    fchk = jinja2.Template(args["fchk_tmp"].replace("YYY", "{{ fname }}"))

    if idir.is_dir():
        fchkfiles = list(idir.glob(fchk.render({"fname": "*"})))
    else:
        raise OSError("Input directory given is not a directory or does not exist, exiting.")

    # TODO: Find corresponding log files based on the fchk names


class FileInformation:
    def __init__(self, fchk, log, nr, state):
        self.fchk_file = fchk
        self.log_file = log
        self.number = nr
        self.root = state

    def __lt__(self, other):
        return self.nr < other.nr

    def __gt__(self, other):
        return self.nr > other.nr

    def __eq__(self, other):
        return self.nr == other.nr



class JobInformation:
    def __init__(self, fileinfos, idir, odir, mwfn, vmd, vmdstate):
        self.files = fileinfos
        self.input_dir = idir
        self.output_dir = odir
        self.mwfn_cmd = mwfn
        self.vmd_cmd = vmd
        self.vmdstate = vmdstate