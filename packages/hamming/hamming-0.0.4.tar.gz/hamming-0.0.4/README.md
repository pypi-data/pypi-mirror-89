# HAMMING
>

#### The HAMMING Module is a python library which lets you generate hamming code and detect error in it.

## Understanding the Concept

[Hamming code] is a block code that is capable of detecting up to two simultaneous bit errors and correcting single-bit errors. It was developed by R.W. Hamming for error correction.

## Installation

pip install hamming

## Examples
```
from hamming import hammingcode

hammingcode.generate_hamming_code("01010101")
hammingcode.detect_error_in_hamming_code("01010101")
```

## Requirements

The HAMMING offically supports Python 3.9.

[Hamming code]: <https://en.wikipedia.org/wiki/Hamming_code>
