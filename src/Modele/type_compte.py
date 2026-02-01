"""
enum class
"""
from enum import IntEnum


class TypeCompte(IntEnum):
    """
    Enum for different possible account type
    """

    COURANT = 0
    LIVRET_A = 1
    PEL = 2
