#     list_arg should have such representation
#     list_arg: {
#         'value': 1,
#             'next': {
#                 'value': 2,
#                 'next': {
#                     'value': 3,
#                     'next': {
#                         'value': 4,
#                         'next': None,
#                 },
#             },
#         },
#     }


def reverse_print(list_arg):
    assert isinstance(list_arg, dict), "List is not instance of 'dict'"
    # если список пустой выводим пустую строку
    if not list_arg:
        print()
        return
    # хранит элементы списка в обратном порядке, для последующего вывода
    reverse_list = []

    class CheckValue:
        # данный класс необходим для проверки наличия атрибута 'value'
        # т.к. CheckValue определен внутри класса, он недоступен для внешнего вызова
        # что обеспечивает корректность работы проверки наличия атрибута - list_arg.get('value', CheckValue)
        pass

    def get_reverse_list(list_arg):
        next_node = list_arg.get('next', False)
        assert next_node is not False and isinstance(next_node, (dict, type(None))), "List node doesn't have 'next' attribute or it is not instance of dict or NoneType"
        curr_val = list_arg.get('value', CheckValue)
        assert curr_val is not CheckValue, "List node doesn't have 'value' attribute"
        reverse_list.insert(0, curr_val)
        if next_node is not None:
            get_reverse_list(next_node)

    get_reverse_list(list_arg)
    print(reverse_list)


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
    reverse_print(some_list)
