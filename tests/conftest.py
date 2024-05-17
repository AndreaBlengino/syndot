from hypothesis.strategies import composite, text, lists, characters
import os


TEST_DATA_PATH = 'test_data'
SETTINGS_DIR = os.path.join(TEST_DATA_PATH, 'Settings')


@composite
def paths(draw, absolute = False):
    folder_list = draw(lists(elements = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97,
                                                                                                max_codepoint = 122)),
                             min_size = 2,
                             max_size = 5))
    if absolute:
        folder_list.insert(0, os.path.join(os.getcwd(), TEST_DATA_PATH))
    else:
        folder_list.insert(0, os.path.join('.', TEST_DATA_PATH))

    return os.path.join(*folder_list)


@composite
def usernames(draw):
    return draw(text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)))

