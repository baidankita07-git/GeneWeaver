# GeneWeaver — Genomic Parser

Member 3 component: genomic FASTA ingestion, sequence validation/cleaning,
NumPy encoding and chunk preparation. This package is a parser foundation;
CRISPR guide/PAM scoring is planned as a separate module in the next phase.

## Scope

- Read multi-record FASTA files using Biopython.
- Extract record IDs, descriptions, sequences and lengths.
- Validate canonical DNA bases and optional IUPAC ambiguity symbols.
- Normalize sequence case and whitespace.
- Encode canonical A/C/G/T bases as NumPy integer values.
- Split sequences into chunks while retaining zero-based, half-open coordinates.

## Project structure

```text
genomic_parser/
  __init__.py
  fasta_reader.py
  sequence_validator.py
  sequence_cleaner.py
  numpy_converter.py
  chunk_processor.py
tests/
data/
docs/
requirements.txt
```

## Setup

Use Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Quick example

```python
from genomic_parser import read_fasta, clean_dna_sequence
from genomic_parser import encode_dna_sequence, chunk_sequence

records = read_fasta("data/sample.fasta")
sequence = clean_dna_sequence(records[0]["sequence"])
encoded = encode_dna_sequence(sequence)
chunks = chunk_sequence(sequence, chunk_size=1000, overlap=50)

print(records[0]["id"], len(encoded), len(chunks))
```

Only canonical A/C/G/T bases can be NumPy-encoded with the current two-bit
mapping. The validator and cleaner can accept IUPAC ambiguity symbols by
default; decide how ambiguous bases should be handled before encoding.

## Tests

```bash
python -m pytest -q
```

## Coordinate convention

Chunk coordinates are zero-based and half-open: `start` is included and
`end` is excluded. For a chunk of length `n`, `end - start == n`.

## Development status

This package implements Member 3's parser foundation. CRISPR guide handling,
PAM detection, mismatch scoring and off-target ranking belong to the planned
`crispr_scoring/` module and are not implemented in this parser package yet.
