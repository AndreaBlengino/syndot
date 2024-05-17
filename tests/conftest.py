from hypothesis.strategies import composite, text, lists, characters
import os


TEST_DATA_PATH = 'test_data'


@composite
def paths(draw):
    folder_list = draw(lists(elements = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97,
                                                                                                max_codepoint = 122)),
                             min_size = 2,
                             max_size = 5))
    folder_list.insert(0, os.path.join('.', TEST_DATA_PATH))

    return os.path.join(*folder_list)
