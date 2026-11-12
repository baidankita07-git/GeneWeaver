import numpy as np
import pytest
from genomic_parser.numpy_converter import encode_dna_sequence, decode_dna_array


def test_encode_decode_round_trip():
    encoded = encode_dna_sequence("ACGT")
    assert encoded.tolist() == [0, 1, 2, 3]
    assert decode_dna_array(encoded) == "ACGT"


def test_encoding_rejects_ambiguous_symbols():
    with pytest.raises(ValueError):
        encode_dna_sequence("ACNT")
