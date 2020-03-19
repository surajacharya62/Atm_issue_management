from django.core.exceptions import ValidationError
import re
from django import forms


def validate_switch_ip(value):
    # pattern = re.compile(r"test")
    # print(value)
    # print(re.match("rest", value))
    # if re.match("rest", value):
    #     print('Please provide Correct IP address')
    #     #raise forms.ValidationError("Please provide valid IP such as 10.0.24.17")
    # return value

    if not "test" in value:
        raise forms.ValidationError('Error')
        print('error')
    return value


