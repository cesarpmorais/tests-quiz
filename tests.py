import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title='q1')
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)


def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100


def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_create_choice_with_invalid_text():
    with pytest.raises(Exception, match='Text cannot be empty'):
        Choice(id=1, text='')
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        Choice(id=1, text='a' * 101)


def test_create_question_with_invalid_points():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=101)


def test_add_multiple_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    assert len(question.choices) == 2
    assert question.choices[0] == choice1
    assert question.choices[1] == choice2


def test_remove_choice():
    question = Question(title='q1')
    choice = question.add_choice('a', False)
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0


def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Invalid choice id 999'):
        question.remove_choice_by_id(999)


def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.remove_all_choices()
    assert len(question.choices) == 0


def test_select_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    selected = question.select_choices([choice1.id])
    assert selected == [choice1.id]


def test_select_more_than_max_selections():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.select_choices([choice1.id, choice2.id])


def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    question.set_correct_choices([choice1.id])
    assert choice1.is_correct is True
    assert choice2.is_correct is False


def test_generate_choice_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    assert choice1.id == 1
    assert choice2.id == 2


@pytest.fixture
def sample_question():
    question = Question(title='Sample Question', max_selections=2)
    choice1 = question.add_choice('Option A', True)
    choice2 = question.add_choice('Option B', False)
    choice3 = question.add_choice('Option C', True)
    return question


def test_select_correct_choices_with_fixture(sample_question):
    selected = sample_question.select_choices(
        [sample_question.choices[0].id, sample_question.choices[2].id])
    assert selected == [sample_question.choices[0].id,
                        sample_question.choices[2].id]


def test_remove_all_choices_with_fixture(sample_question):
    sample_question.remove_all_choices()
    assert len(sample_question.choices) == 0
