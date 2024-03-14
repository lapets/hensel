"""
Pure-Python implementation of `Hensel lifting \
<https://en.wikipedia.org/wiki/Hensel%27s_lemma>`__ for square roots modulo
a prime power.
"""
from __future__ import annotations
import doctest
from egcd import egcd

def hensel(root: int, prime: int, exponent: int = 1) -> int:
    """
    Lift a square root of a value modulo ``prime ** exponent`` to the square
    root of that same value modulo ``prime ** (exponent + 1)``.

    More specifically, let ``square`` be a nonnegative integer that is the
    least nonnegative residue of the congruence class ``root ** 2`` modulo
    ``prime ** exponent``. Use
    `Hensel lifting <https://en.wikipedia.org/wiki/Hensel%27s_lemma>`__ to
    return an integer that represents the square root modulo
    ``prime ** (exponent + 1)`` of the congruence class represented by the
    integer ``square`` modulo ``prime ** (exponent + 1)``.

    >>> hensel(4, 7)
    39
    >>> hensel(2, 7, 2)
    2

    Any attempt to invoke this function with arguments that do not have the
    expected types (or do not fall within the supported ranges) raises an
    exception. **If** ``prime`` **is not a prime number, the behavior of this
    function is not specified.**

    >>> hensel('abc', 7)
    Traceback (most recent call last):
      ...
    TypeError: 'str' object cannot be interpreted as an integer
    >>> hensel(2, {})
    Traceback (most recent call last):
      ...
    TypeError: 'dict' object cannot be interpreted as an integer
    >>> hensel(2, 7, [])
    Traceback (most recent call last):
      ...
    TypeError: 'list' object cannot be interpreted as an integer
    >>> hensel(2, -1)
    Traceback (most recent call last):
      ...
    ValueError: prime must be a positive integer
    >>> hensel(2, 7, -1)
    Traceback (most recent call last):
      ...
    ValueError: exponent must be a nonnegative integer

    The example below verifies the correct behavior of the function on a range
    of different inputs.

    >>> all(
    ...     pow(r, 2, p ** k) == pow(hensel(r, p, k), 2, p ** (k + 1))
    ...     for k in range(0, 5)
    ...     for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    ...     for r in range(1, p ** k) if r % p != 0
    ... )
    True
    """
    if not isinstance(root, int):
        raise TypeError(
            "'" + type(root).__name__ + "'" +
            ' object cannot be interpreted as an integer'
        )

    if not isinstance(prime, int):
        raise TypeError(
            "'" + type(prime).__name__ + "'" +
            ' object cannot be interpreted as an integer'
        )

    if not isinstance(exponent, int):
        raise TypeError(
            "'" + type(exponent).__name__ + "'" +
            ' object cannot be interpreted as an integer'
        )

    if prime < 0:
        raise ValueError('prime must be a positive integer')

    if exponent < 0:
        raise ValueError('exponent must be a nonnegative integer')

    root_inv = egcd(root, prime)[1]
    two_inv = egcd(2, prime)[1]
    prime_to_exponent = prime ** exponent
    c = (
        ((root_inv * two_inv) % prime)
        *
        (
            (
                (pow(root, 2, prime_to_exponent) - pow(root, 2))
                //
                prime_to_exponent
            )
            %
            prime
        )
    ) % prime

    return (root + c * prime_to_exponent) % (prime * prime_to_exponent)

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
