import argparse

def read_cli_args():
    """Handle the CLI arguments and options."""
    parser = argparse.ArgumentParser(
        prog="SiteChecker", description="Check the availability of websites.")
    
    parser.add_argument(
        '-u',
        '--urls',
        metavar="URLs",                             # sets a name for the argument in usage or help messages.
        nargs="+",                                  # accept a list of CL args after the -u or --urls switch
        type=str,                                   # data type of the CLI args  
        default=[],                                 # default CLI args, empty list.
        help="Enter one or more website URLs"       # help message to print out
    )
    # to read in the URLs from a file provided file name as input.
    # does not take `nargs`, allowing only a single file name to be provided.
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file"
    )
    # parse the async arguments
    parser.add_argument(
        "-a",
        "--asynchronous",
        action="store_true",
        help="run the connectivity check asynchornously."
    )
    return parser.parse_args()

def display_check_result(result, url, error=""):
    """Display the result of a connectivity check."""
    print('The status of "{url}" is: '.format(url=url), end=' ')
    if result:
        print('Online! 👍')
    else:
        print('Offline? 👎 \n Error: {error}'.format(error=error))