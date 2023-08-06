"""
This module contains information related to the reference genome.
"""

import logging

from collections import  Counter
from bgreference import refseq

from oncodrivefml import __logger_name__

logger = logging.getLogger(__logger_name__)

ref_build = 'hg38'
"""
Build of the Reference Genome
"""

__CB = {"A": "T", "T": "A", "G": "C", "C": "G"}


def change_build(build):
    """
    Modify the default build fo the reference genome

    Args:
        build (str): genome reference build

    """
    global ref_build
    ref_build = build
    logger.info('Using %s as reference genome', ref_build.upper())


def get_build():
    return ref_build


def get_ref(chromosome, start, size=1):
    """
    Gets a sequence from the reference genome

    Args:
        chromosome (str): chromosome
        start (int): start position where to look
        size (int): number of bases to retrieve

    Returns:
        str. Sequence from the reference genome

    """
    return refseq(ref_build, chromosome, start, size)


def get_ref_triplet(chromosome, start):
    """

    Args:
        chromosome (str): chromosome identifier
        start (int): starting position

    Returns:
        str: 3 bases from the reference genome

    """
    return get_ref(chromosome, start, size=3)


def reverse_complementary_sequence(seq):
    return "".join([__CB[base] if base in __CB else base for base in seq.upper()[::-1]])
