def format_shopping_cart(ingredients):
    data = []
    for i, ingredient in enumerate(ingredients):
        data.append(
            f'{i+1}) {ingredient["ingredient__name"]} - '
            f'{ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
        )
    return 'Список проектов:\n\n' + '\n'.join(data)
