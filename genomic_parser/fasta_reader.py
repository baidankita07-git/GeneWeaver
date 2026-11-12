"""Read FASTA files with Biopython and return structured records."""

from pathlib import Path
from typing import Union

from Bio import SeqIO


def read_fasta_records(file_path: Union[str, Path]):
    """Return Biopython SeqRecord objects from a FASTA file.

    Raises FileNotFoundError if the path does not exist and ValueError if the
    file contains no FASTA records.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    records = list(SeqIO.parse(str(path), "fasta"))
    if not records:
        raise ValueError(f"No FASTA records found in: {path}")
    return records


def read_fasta(file_path: Union[str, Path]):
    """Return FASTA records as dictionaries containing id, description and sequence."""
    records = read_fasta_records(file_path)
    return [
        {
            "id": record.id,
            "description": record.description,
            "sequence": str(record.seq),
            "length": len(record.seq),
        }
        for record in records
    ]
