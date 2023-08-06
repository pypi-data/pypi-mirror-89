from IPython.display import display

from dutil.transform import ht


def dht(arr, n: int = 2) -> None:
    """Display first and last (top and bottom) entries"""

    display(ht(arr, n))
