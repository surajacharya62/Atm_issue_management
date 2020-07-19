import prac

print('second module-{}'.format(__name__))


def main():
    print('first module-{}'.format(__name__))


if __name__ == '__main__':
    main()

else:
    print('run from import.')
