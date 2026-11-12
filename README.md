
# GeneWeaver
## GPU-Accelerated CRISPR Alignment Engine

### Member 3 — Genomic Parser & CRISPR Scoring

This component handles genomic FASTA ingestion, sequence validation and
cleaning, NumPy encoding, genome chunk preparation, and the planned
CRISPR guide/PAM scoring functionality.

The genomic parser provides the foundation for processing DNA sequences
before downstream alignment and scoring operations.

## 1. Scope

### Genomic Parser
- Read multi-record FASTA files using Biopython.
- Extract record IDs, descriptions, sequences, and lengths.
- Validate canonical DNA bases and optional IUPAC ambiguity symbols.
- Normalize sequence case and whitespace.
- Encode canonical A/C/G/T bases as NumPy integer values.
- Split long sequences into indexed chunks.
- Preserve sequence IDs and zero-based, half-open coordinates.

### CRISPR Scoring — Planned
- CRISPR guide sequence handling.
- PAM sequence detection.
- Guide and target sequence matching.
- Nucleotide mismatch detection.
- Position-based mismatch scoring.
- PAM-aware scoring matrix.
- Potential off-target site ranking.

## 2. Project Structure

```text
GeneWeaver/
├── genomic_parser/
│   ├── __init__.py
│   ├── fasta_reader.py
│   ├── sequence_validator.py
│   ├── sequence_cleaner.py
│   ├── numpy_converter.py
│   └── chunk_processor.py
├── tests/
│   └── __init__.py
├── data/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

## 3. Technologies

- Python 3.10+
- Biopython — FASTA parsing and biological sequence handling
- NumPy — Numerical DNA sequence representation
- Pytest — Unit testing

## 4. Setup

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 5. Quick Example

```python
from genomic_parser import read_fasta, clean_dna_sequence
from genomic_parser import encode_dna_sequence, chunk_sequence

records = read_fasta("data/sample.fasta")

sequence = clean_dna_sequence(records[0]["sequence"])

encoded = encode_dna_sequence(sequence)

chunks = chunk_sequence(
    sequence,
    chunk_size=1000,
    overlap=50
)

print(records[0]["id"], len(encoded), len(chunks))
```

Only canonical A/C/G/T bases can currently be NumPy-encoded using the
two-bit mapping. The validator and cleaner can accept IUPAC ambiguity
symbols; ambiguous bases must be handled before encoding.

## 6. Testing

Run the test suite from the project root:

```bash
python -m pytest -q
```

## 7. Coordinate Convention

Genome chunk coordinates use zero-based, half-open indexing:

- `start` — inclusive starting position.
- `end` — exclusive ending position.
- `length` — number of bases in the chunk.

The coordinate relationship is:

```text
length = end - start
```

Adjacent chunks may overlap according to the configured overlap value.

## 8. Development Status

### Genomic Parser
- FASTA ingestion foundation.
- Sequence validation and cleaning.
- NumPy sequence encoding.
- Configurable genome chunking.
- Chunk metadata preservation.
- Unit testing.

### CRISPR Scoring
Planned for the next development phase. Guide handling, PAM detection,
mismatch scoring, and off-target ranking will be implemented separately.

## 9. Contribution Scope

This component is maintained as Member 3's responsibility within
GeneWeaver.

Development is limited to genomic parsing and CRISPR scoring logic.
GPU alignment, distributed processing, and other team components remain
the responsibility of their respective team members.
