import pytest
import graph_operations

def test_roots_are_correctly_generated():
    expected_roots = {'ironmonger', 'hold', 'keep'}
    actual_roots = graph_operations.get_roots()
    assert actual_roots == expected_roots
