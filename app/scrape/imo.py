# -*- coding: utf-8 -*-
"""
/app/imo.py
Functions for generating imo numbers.
"""

import numpy as np
from numpy import ndarray

def checksum(six_digits: ndarray) -> str:
    """
    Computes the checksum digit for the IMO.

    Args:
        six_digits (ndarray): Six leading digits of IMO

    Returns:
        (str): A string containing 7-digit IMO with leading 6 digits of IMO
            followed by one checksum digit.
    """

    total = 0
    imo = ""
    for i, digit in enumerate(six_digits):
        total += (7-i) * digit
        imo += str(digit)
    return imo + str(total)[-1]

def random() -> str:
    """
    Generates a random IMO from pool of possible values.
    IMO started from leading digit of 5, and after hitting the end of 9's, the
    sequence has wrapped around to using 1 as leading digit.

    Args:
        None

    Returns:
        (str): A string containing 7-digit IMO with leading 6 digits of IMO
            followed by one checksum digit.
    """

    digits = np.zeros(6)
    digits[0] = np.random.randint(1,high=6)
    if digits[0] != 1:
         digits[0] += 5
    digits[1:] = np.random.randint(0,high=9,size=5)
    
    return checksum(digits)

def cache_imo(imo: str):
    """
    Caches successful imo values to file.

    Args:
        imo (str): A string containing 7-digit IMO with leading 6 digits of IMO
            followed by one checksum digit.
    """
    with open("imo.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([imo])

def load_cached_imo() -> list:
    """
    Retrieves list of successful imo values.
    
    Returns:
        list[str]: List of imo values as str objects.
    """
    with open("imo.csv", "r", newline="") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

if __name__ == "__main__":
    six_digits = np.random.randint(0,high=9,size=6).astype(int)
    print(six_digits)
    print(checksum(six_digits))
    six_digits = np.array([1,0,0,9,6,6])
    print(six_digits)
    print(checksum(six_digits))
