from eldar import Query


def test_validate_query():
    """
    Tests that we detect valid queries as valid and non-valid as non-valid
    :return:
    """

    query = Query('Hello AND World')
    validity_check = query.validate_query()
    assert validity_check.get("is_valid") is True
    assert validity_check.get("query_issues") == []

    query = Query('(Hello) AND (World')
    validity_check = query.validate_query()
    assert validity_check.get("is_valid") is False
    assert validity_check.get("query_issues") == ["Number of opening and closing parentheses do not match"]

    query = Query('("Hello") AND ("World)')
    validity_check = query.validate_query()
    assert validity_check.get("is_valid") is False
    assert validity_check.get("query_issues") == ["Number of opening and closing quotation marks do not match"]

    query = Query('("Hello") AND "World)')
    validity_check = query.validate_query()
    assert validity_check.get("is_valid") is False
    assert set(validity_check.get("query_issues")) == {
        "Number of opening and closing quotation marks do not match",
        "Number of opening and closing parentheses do not match"
    }

    query = Query(' ')
    validity_check = query.validate_query()
    assert validity_check.get("is_valid") is False
    assert validity_check.get("query_issues") == ["No query provided"]


def test_query_results():
    """
    Test that the results of a query search are as espected
    :return:
    """

    query = Query('Hello AND World')
    sample_text = "Hello how are you today world?"
    result = query(sample_text)
    assert result is True

    query = Query('Hello AND World')
    sample_text = "Hello how are you today?"
    result = query(sample_text)
    assert result is False

    query = Query('Hello OR World')
    sample_text = "Hello how are you today?"
    result = query(sample_text)
    assert result is True

    query = Query('(Hello AND World) AND NOT (Bad)')
    sample_text = "Hello how are you today world?"
    result = query(sample_text)
    assert result is True

    query = Query('(Hello AND World) AND NOT (Bad)')
    sample_text = "Hello how are you today world? I'm bad"
    result = query(sample_text)
    assert result is False

    query = Query('(Hello OR World) AND NOT (Bad)')
    sample_text = "Hello how are you today? I'm bad"
    result = query(sample_text)
    assert result is False

    query = Query('((Hello OR World) AND NOT (Bad)) AND (Good)')
    sample_text = "Hello how are you today? I'm bad"
    result = query(sample_text)
    assert result is False

    query = Query('((Hello OR World) AND NOT (Bad)) AND (Good)')
    sample_text = "Hello how are you today? I'm OK"
    result = query(sample_text)
    assert result is False

    query = Query('((Hello OR World) AND NOT (Bad)) AND (Good)')
    sample_text = "Hello how are you today? I'm Good"
    result = query(sample_text)
    assert result is True

    query = Query('((Hello AND World) AND NOT (Bad)) AND (Good)')
    # This has a special character which should be decoded
    sample_text = "Hello world how are you today? I'm göod"
    result = query(sample_text)
    assert result is True

    query = Query('(Hello AND World) AND NOT (Bad OR Good)')
    sample_text = "Hello world how are you today? I'm good"
    result = query(sample_text)
    assert result is False

    sample_text = "Hello world how are you today?"
    result = query(sample_text)
    assert result is True

    query = Query('(Hello AND World) AND NOT (Bad AND Good)')
    sample_text = "Hello world how are you today? I'm good"
    result = query(sample_text)
    assert result is True

    sample_text = "Hello world how are you today? I'm good but can be bad"
    result = query(sample_text)
    assert result is False

    query = Query('(("hello" OR "hi") AND ("world" OR "earth"))')

    sample_text = "Hi there, I am from Earth"
    result = query(sample_text)
    assert result is True

    # Test chained AND NOT
    query = Query("Hello AND NOT world AND NOT how")
    sample_text = "Hello world, how are you?"
    result = query(sample_text)
    assert result is False

    sample_text = "Hello, how are you?"
    result = query(sample_text)
    assert result is False

    sample_text = "Hello world!"
    result = query(sample_text)
    assert result is False

    sample_text = "Hello what's up?"
    result = query(sample_text)
    assert result is True

def test_query_case_sensitive_matching():

    query = Query('Hello AND World')
    sample_text = "Hello how are you today world?"
    result = query(sample_text)
    assert result is True

    query = Query('Hello AND World', ignore_case=False)
    sample_text = "Hello how are you today world?"
    result = query(sample_text)
    assert result is False

def test_query_search_with_quotes():
    """
    Tests that we don't match a substring in a word and that we do match query types correctly
    :return:
    """

    # This should match
    query = Query("and")

    sample_text = "I want to go ahead and cancel the booking"
    result = query(sample_text)
    assert result is True

    # This should match
    query = Query('and AND not an')

    sample_text = "I want to go ahead and cancel the booking"
    result = query(sample_text)
    assert result is True

    # This shouldn't match
    query = Query("an")

    sample_text = "I want to go ahead and cancel the booking"
    result = query(sample_text)
    assert result is False
