import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    # assert 1 == 2

def test_is_instance():
    assert isinstance("hello", str)
    assert not isinstance(123, str)
    # assert isinstance(123, str)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type(123) is int
    assert type("hello") is str
    assert not type(123) is str

    # assert type(123) is str   

def test_greater_than():
    assert 5 > 3
    assert not (2 > 5)
    # assert 2 > 5

def test_less_than():
    assert 3 < 5
    assert not (5 < 3)
    # assert 5 < 3

def test_lists():
    my_list = [1, 2, 3]
    any_list  = [False, False]
    assert len(my_list) == 3
    assert 2 in my_list
    assert not (4 in my_list)
    assert all(my_list)  # This will fail if my_list is empty

    assert not any(any_list)  # This will fail if my_list is not empty
    # assert 4 in my_list

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def student():
    return Student("John", "Doe", "Computer Science", 3)

@pytest.fixture
def test_person_initialization(student):
    # student = Student("John", "Doe", "Computer Science", 3)
    assert student.first_name == "John"
    assert student.last_name == "Doe"
    assert student.major == "Computer Science"
    assert student.years == 3

    # assert student.first_name == "Jane"