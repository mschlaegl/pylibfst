import os


def _test_example(example, directory):
    stream = os.popen(
        "python " + directory + "/" + example + ".py" " examples/counter.fst"
    )
    output = stream.read()
    with open("tests/refoutput/" + example + ".out", "r") as file:
        refoutput = file.read()  # .replace('\n', '')
    if output != refoutput:
        return 1
    return 0


def test_example_dumpfst_old():
    assert _test_example("dumpfst_old", "tests/examples_old") == 0


def test_example_IterBlocks_callback_old():
    assert _test_example("IterBlocks_callback_old", "tests/examples_old") == 0


def test_example_IterBlocks_wrapped_callback_old():
    assert _test_example("IterBlocks_wrapped_callback_old", "tests/examples_old") == 0


def test_example_dumpfst():
    assert _test_example("dumpfst", "examples") == 0


def test_example_IterBlocks_callback():
    assert _test_example("IterBlocks_callback", "examples") == 0


def test_example_IterBlocks_wrapped_callback():
    assert _test_example("IterBlocks_wrapped_callback", "examples") == 0
