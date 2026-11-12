"""Genomic parsing utilities for the GeneWeaver project."""

__version__ = "0.1.0"

from .fasta_reader import read_fasta, read_fasta_records
from .sequence_validator import validate_dna_sequence, is_valid_dna_sequence
from .sequence_cleaner import clean_dna_sequence
from .numpy_converter import encode_dna_sequence, decode_dna_array
from .chunk_processor import chunk_sequence, chunk_genome

__all__ = [
    "read_fasta", "read_fasta_records",
    "validate_dna_sequence", "is_valid_dna_sequence",
    "clean_dna_sequence",
    "encode_dna_sequence", "decode_dna_array",
    "chunk_sequence", "chunk_genome",
]
