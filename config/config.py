# - IMPORTS ---
import argparse


# - FUNCTIONS ---
def arg_parser():
    parser = argparse.ArgumentParser(
        description="WIP for sending GPU loads to GPAC"
    )

    # add arguments
    parser.add_argument(
        "-s", "--sleep", type=int, default=5, help="Check every -s seconds"
    )
    parser.add_argument(
        "-r",
        "--run",
        type=int,
        default=600,
        help="For how many hours to run before break",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        default=None,
        help="Password to connect to the servers",
    )
    parser.add_argument(
        "-a",
        "--anonymize",
        action='store_true',
        help="Anonymize the results",
    )

    # Parse the arguments
    return parser.parse_args()
