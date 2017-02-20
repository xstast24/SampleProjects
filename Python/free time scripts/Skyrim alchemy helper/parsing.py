def get_ingredients():
    with open('ingredients', 'r') as f_ingredients:
        table = f_ingredients.read()
        table = table.replace('â€ˇ', '')
        table = table.replace('*', '')
        table = table.replace('â€', '')
        table = table.replace('\'', '')
        ingredients = {}
        for line in table.split('\n'):
            columns = line.split('\t')
            ingredients[columns[0].upper()] = (columns[1], columns[2], columns[3], columns[4])

    return ingredients


def find_matching_ingredients(base_ingredient, all_ingredients):
    try:
        base_effects = all_ingredients[base_ingredient]
    except KeyError:
        return None

    matching_ingredients = {}  # dict in format   number_of_matched_effects: {ingredient: [[matching_effects], (effects)]}
    # matching_ingredients_2 = {} TODO
    for ingredient, effects in all_ingredients.items():
        matches = 0
        matching_effects = []
        for effect in effects:
            if effect in base_effects:
                matches += 1
                matching_effects.append(effect)

        try:
            matching_ingredients[matches][ingredient] = [matching_effects, effects]
        except KeyError:
            matching_ingredients[matches] = {}
            matching_ingredients[matches][ingredient] = [matching_effects, effects]

    return matching_ingredients
