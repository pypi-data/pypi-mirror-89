import click
from .utils import submission_scraper


@click.group()
def main():
    """
    \b
      _________  _____
     / ___/ __ \/ ___/
    / /__/ /_/ / /__  
    \___/ .___/\___/  
       /_/            

    CPC is a command-line utility
    aimed towards competitive programmers.
    """
    pass


@main.command("scrape")
def scrape():
    """
    Start interactive solution scraper
    """
    submission_scraper.Scraper().start()


if __name__ == "__main__":
    main()
