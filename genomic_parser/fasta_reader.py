
"""Read genomic FASTA files using Biopython."""

from pathlib import Path
from typing import Dict, List, Union

from Bio import SeqIO


def read_fasta(file_path: Union[str, Path]) -> List[Dict]:
    """Read a FASTA file and extract genomic sequence information.

    Args:
        file_path: Path to a FASTA file (.fasta or .fa).

    Returns:
        A list of dictionaries containing:
            id: FASTA record identifier.
            description: Complete FASTA header description.
            sequence: DNA sequence as an uppercase string.
            length: Number of bases in the sequence.

        Returns an empty list if the FASTA file contains no records.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IsADirectoryError: If the supplied path is a directory.
        ValueError: If the file extension is not supported.
    """
    path = Path(file_path)

    # Check whether the file exists.
    if not path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    # Ensure the supplied path is a file, not a directory.
    if path.is_dir():
        raise IsADirectoryError(
            f"Expected a FASTA file, got directory: {path}"
        )

    # Validate the file extension.
    if path.suffix.lower() not in {".fasta", ".fa"}:
        raise ValueError(
            f"Unsupported file extension: {path.suffix}. "
            "Expected .fasta or .fa"
        )

    records = []

    # Parse FASTA records using Biopython.
    with path.open("r", encoding="utf-8") as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(record.seq).upper()

            records.append({
                "id": record.id,
                "description": record.description,
                "sequence": sequence,
                "length": len(sequence),
            })

    return records


def read_fasta_records(file_path: Union[str, Path]) -> List[Dict]:
    """Read FASTA records using the compatible legacy function name.

    This wrapper delegates to read_fasta() so both function names
    return the same data structure and follow the same validation rules.
    """
    return read_fasta(file_path)
