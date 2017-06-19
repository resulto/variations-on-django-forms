Django variations on forms
==========================

Project showing variations on Django form usage. Some usage scenarios:

1. Field that is required depending on the value of another field.
2. Adding a default empty choice to a required ModelChoiceField.
3. Customizing the choices of a ModelChoiceField by replacing it with a
   TypedChoiceField.
4. Validating a choice in ModelChoiceField and ModelMultipleChoiceField
   depending on the value of another field.
5. Skipping validation of \*ChoiceField by delegating the check to coerce
   or clean.

Local install
-------------

This project requires Python 3.6+ because it uses type annotations.

::

    pip install -r requirements.txt
    python manage.py migrate
