import pytest
from tools.profanity_helper import AdvancedProfanityFilter


@pytest.fixture
def profanity_filter():
    return AdvancedProfanityFilter()


def test_load_blacklist(profanity_filter):
    # Arrange
    expected_blacklist = ["jancuk", "anjing", "babi"]

    # Act
    actual_blacklist = profanity_filter.load_blacklist("words_blacklist.txt")
    new_blacklist = []
    for word in expected_blacklist:
        if word in actual_blacklist:
            new_blacklist.append(word)

    # Assert
    assert new_blacklist == expected_blacklist


def test_load_whitelist(profanity_filter):
    # Arrange
    expected_whitelist = ["bangsa", "kontrol"]

    # Act
    actual_whitelist = profanity_filter.load_whitelist("words_whitelist.txt")
    new_whitelist = []
    for word in expected_whitelist:
        if word in actual_whitelist:
            new_whitelist.append(word)

    # Assert
    assert new_whitelist == expected_whitelist


def test_replace_profanity(profanity_filter):
    # Arrange
    text = "This is a b@d t3xt"

    # Act
    replaced_text = profanity_filter.replace_profanity(text)

    # Assert
    assert replaced_text == "this is a bad text"


def test_is_similar(profanity_filter):
    # Arrange
    word = "hello"
    profane_word = "h3ll0"

    # Act
    replaced_text = profanity_filter.replace_profanity(profane_word)
    is_similar = profanity_filter.is_similar(word, replaced_text)

    # Assert
    assert is_similar == True


def test_is_whitelisted(profanity_filter):
    # Arrange
    word = "bangsa"

    # Act
    is_whitelisted = profanity_filter.is_whitelisted(word)

    # Assert
    assert is_whitelisted == True


def test_is_profanity(profanity_filter):
    # Arrange
    word = "b4ng54t"

    # Act
    is_profanity = profanity_filter.is_profanity(word)

    # Assert
    assert is_profanity == True


def test_censor(profanity_filter):
    # Arrange
    text = "This is an b4ng5@t message"

    # Act
    censored_text = profanity_filter.censor(text)

    # Assert
    assert censored_text == "This is an ***** message"
