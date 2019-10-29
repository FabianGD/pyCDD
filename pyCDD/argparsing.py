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
        dest="fchk_jinja",
        help="Jinja string template stating variable parts of the \
              .fchk/.molden filename, default '%(default)s'",
        type=str,
        default="{{ fname }}.fchk",
    )
    parser.add_argument(
        "--logtemplate",
        dest="log_jinja",
        help="Jinja string template stating variable parts of the .log \
              filename, default '%(default)s'",
        type=str,
        default="{{ fname }}.log",
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
        "--vmdstate",
        dest="vmd_statefile",
        help="VMD visualisation state file name, optional",
        type=str,
    )

    args = vars(parser.parse_args())
    cwd = Path(".")

    args["inputdir"] = cwd / Path(args["inputdir"])
    args["outputdir"] = cwd / Path(args["outputdir"])

    return args

