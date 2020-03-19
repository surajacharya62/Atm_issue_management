import  re

pattern = re.compile('[0-9][0-9][.][0-9][.][0-9][0-9]')

str = '10.0.10'

if pattern.match(str):
    print(re.match(pattern, str))
    print('found')
else:
    print('not found')