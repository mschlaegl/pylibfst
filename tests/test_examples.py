import os

def _test_example(example):
    stream = os.popen("python examples/" + example + ".py" " examples/counter.fst")
    output = stream.read()
    with open("tests/refoutput/" + example + ".out", "r") as file:
        refoutput = file.read()#.replace('\n', '')
    if output != refoutput:
        return 1
    return 0

def test_example_dumpfst():
    assert _test_example("dumpfst") == 0

def test_example_IterBlocks_callback():
    assert _test_example("IterBlocks_callback") == 0

def test_example_IterBlocks_wrapped_callback():
    assert _test_example("IterBlocks_wrapped_callback") == 0
