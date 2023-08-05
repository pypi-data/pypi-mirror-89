from django.test import TestCase
from django.core.exceptions import FieldDoesNotExist

class FormTestCase(TestCase):
    '''
    Base class for FormTests.
    Parameters:
    - form : Form to test
    '''
    form = None

    def assertField(self, field_name, field_class, must_have={}, must_not_have={}):
        '''
        Tests if a field exists under the given name and
        if the field is of the right type.
        Also checks if the field has the given must_have attributes
        and does not have any of the must_not_have attributes. If you
        dont care about the value of the attribute you can just set it to 
        something that fullfills value == False (i.e. '' or 0)
        '''
        try:
            field = self.form.base_fields[field_name]
        except FieldDoesNotExist:
            self.fail(
                'Expecting %s to have a field named \'%s\'' % (
                    self.form.__name__,
                    field_name
                )
            )
        self.assertEqual(
            type(field), field_class,
            msg='Expecting type of %s to be %s' % (
                str(field),
                field_class.__name__
            )
        )

        for key, value in must_have.items():
            if value:
                self.assertEqual(
                    getattr(field, key), value,
                    msg='Expeting the value of %s %s to be \'%s\'' % (
                        str(field),
                        key,
                        value
                    )
                )
            else:
                self.assertTrue(
                    hasattr(field, key),
                    msg='Expeting %s to have \'%s\'' % (
                        str(field),
                        key
                    )
                )

        for key, value in must_not_have.items():
            if value:
                self.assertTrue(
                    getattr(field, key) != value,
                    msg='Expeting the value of %s %s to not be \'%s\'' % (
                        str(field),
                        key,
                        value
                    )
                )
            else:
                self.assertFalse(
                    hasattr(field, value),
                    msg='Expeting %s to not have \'%s\'' % (
                        str(field),
                        key
                    )
                )

        return field