from genomic_parser.fasta_reader import read_fasta, read_fasta_records


def test_read_fasta(tmp_path):
    fasta = tmp_path / "sample.fasta"
    fasta.write_text(">seq1 sample sequence\nACGTAC\n>seq2\nTTAA\n")
    records = read_fasta(fasta)
    assert len(records) == 2
    assert records[0] == {
        "id": "seq1", "description": "seq1 sample sequence",
        "sequence": "ACGTAC", "length": 6
    }
    assert len(read_fasta_records(fasta)) == 2
