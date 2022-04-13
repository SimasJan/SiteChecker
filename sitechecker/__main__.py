import sys
import pathlib
import asyncio
from sitechecker.check import is_site_online, is_site_online_async
from sitechecker.cli import display_check_result, read_cli_args

def _read_urls_from_file(file):
    """Read the URLs from a file provided."""
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            # strip of leading/trailing whitespace from a file
            urls = [url.strip() for url in urls_file]
            if urls:
                return urls
            print("Error: empty input file `{}`".format(file), file=sys.stderr)
    else:
        print("Error: input file not found.", file=sys.stderr)
    return []

def _get_urls_to_check(parsed_args):
    """Get URLs to check from the parsed CLI arguments."""
    urls = parsed_args.urls
    if parsed_args.input_file:
        urls += _read_urls_from_file(parsed_args.input_file)
    return urls

def _synchronous_check(urls):
    """Check URLs in a synchronous way."""
    error = ""
    for url in urls:
        try:
            result = is_site_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

async def _asynchronous_check(urls):
    """Check URLs in an asynchronous way."""
    async def _check(url):
        error = ""
        try:
            result = await is_site_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)
    # alls and awaits the gather() function from the asyncio module. 
    # This function runs a list of awaitable objects concurrently and returns an 
    # aggregated list of resulting values if all the awaitable objects complete successfully. 
    await asyncio.gather(*(_check(url) for url in urls))

def main():
    """Run Site Checker."""
    cli_args = read_cli_args()
    urls = _get_urls_to_check(cli_args)
    if not urls:
        print("Error: no URLs to check", file=sys.stderr)
        sys.exit(1)

    # check if asynchronous in cli args and run with that, other do sync
    if cli_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)

if __name__ == "__main__":
    main()
