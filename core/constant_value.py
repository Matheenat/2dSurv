import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")
def clamp(value: int, max_value: int, min_value: int) -> int:
    """
    Clamp a numeric value within a closed interval.
    Author
    ------
    mikhail akhsakov

    Description
    -----------
    Constrains `value` to the inclusive interval [min_value, max_value].
    If `value` exceeds the upper bound, `max_value` is returned.
    If `value` falls below the lower bound, `min_value` is returned.
    Otherwise, `value` is returned unchanged.
    Mathematical Formulation
    ------------------------
        clamp(v, M, m) = max(min(v, M), m)
    where:
        v ∈ ℤ
        m ≤ M
        result ∈ [m, M]
    Parameters
    ----------
    value : int
        The integer to be constrained.
    max_value : int
        Inclusive upper bound.
    min_value : int
        Inclusive lower bound.
        
    Returns
    -------
    int
        A value guaranteed to satisfy:
            min_value ≤ result ≤ max_value
    Raises
    ------
    ValueError
        If min_value > max_value.
    Complexity
    ----------
    Time: O(1)
    Space: O(1)
    Examples
    --------
    >>> clamp(10, 5, 0)
    5
    >>> clamp(-2, 5, 0)
    0
    >>> clamp(3, 5, 0)
    3
    """
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    return max(min(value, max_value), min_value)