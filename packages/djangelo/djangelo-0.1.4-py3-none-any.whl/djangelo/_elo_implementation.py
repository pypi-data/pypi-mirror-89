import ctypes
from ctypes import c_float as cf


class ELOComparator:

    """Defines the behavior of an ELO rated object when is compared"""

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other


"""Avoiding floating overflow issues, we use C code calculating elo"""
cImport  = ctypes.CDLL('libdjangelo.so')
cImport.get_spected_growing.argtypes = [cf, cf]


class ELOAlgorithmImplementation:

    """Implements ELO as algorithm

        See: https://en.wikipedia.org/wiki/Elo_rating_system#Theory
    """
    @property
    def global_hints_mean(self):
        """The client class must be specify how to get the global hints

        Returns:
            int
        """
        return self.get_global_hints_mean()

    @property
    def spected_growing(self):
        return cImport.get_spected_growing(cf(self.hints),
                                           cf(self.global_hints_mean))

    @property
    def actual_growing(self):
        return self.hints - self.global_hints_mean

    def update_value(self, sensibility):
        newValue = sensibility *(
                      self.actual_growing - self.spected_growing
                   )
        self.value += round(newValue)
