def reverse_print(list_arg, is_begin=True):
    '''
    list_arg should have such representation
    list_arg: {
        'value': 1,
            'next': {
                'value': 2,
                'next': {
                    'value': 3,
                    'next': {
                        'value': 4,
                        'next': None,
                },
            },
        },
    }
    i: correspond to first call
    '''
    if not list_arg:
        print()
        return

    if not list_arg['next'] is None:
        reverse_print(list_arg['next'], is_begin=False)

    if not is_begin:
        print(list_arg['value'], end=', ')
    else:
        print(list_arg['value'])


if __name__ == '__main__':
    some_list = {
        'value': 1,
        'next': {
            'value': 2,
            'next': {
                'value': 3,
                'next': {
                    'value': 4,
                    'next': None,
                },
            },
        },
    }
    another_list = dict()
    reverse_print(another_list)
