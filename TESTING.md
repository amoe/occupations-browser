# Testing guide

A test utility function `occubrow.test_utility.make_backend` is available to
allow test writers to avoid configuring an entire Backend, which may have
several parts that can be mocked but normally would not be.  You pass the
Repository to this function, which it's your choice whether it be a mocked
repository or a non-mocked repository.
