from parsing import get_ingredients, find_matching_ingredients


def print_results(base, matching_ingredients, min_matches):
    if matching_ingredients is None:
        print("INGREDIENT NOT FOUND!")
        return False

    print("\nDisplaying ingredients with minimally {0} matching effects for base: {1}   {2}".format(min_matches, base, matching_ingredients[4][base][1]))
    del(matching_ingredients[4][base])  # remove the base ingredient itself from matching results

    for match_count in reversed(sorted(matching_ingredients.keys())):  # output from the highest match (most interesting) to the lowest
        if match_count >= min_matches:  # desired minimal number of matching effects
            if match_count == 4 and len(matching_ingredients[4].keys()) == 0:
                continue  # do not print empty 4-matches if the ingredient itself is the only 4-match

            print("##### {0} matches #####".format(match_count))
            for ingredient, effects in matching_ingredients[match_count].items():
                print("{0}{1}:  {2}{3} {4}".format(ingredient, (25 - len(ingredient)) * ' ', effects[0], (85 - len(str(effects[0]))) * ' ', effects[1]))


ingredients = get_ingredients()
base = ''
min_matches = 2

while base.upper() != 'EXIT':
    print('')
    input_ = input().replace('\'', '').upper()

    if input_.lower() == "help":
        help = """
        Alchemy Helper 1.2 - input name of an ingredient (without ' symbol) and find out matching ingredients with similar effects. Default minimal number of matching effects is 2.\n
        help - prints help and continues program
        set_max N - sets minimal matching number of effects, min. 0 - max. 4, default is N=2, eg. set_max 3
        set_matches N - same as set_max N
        find_all - iterate through all ingredients and print minimal matches (see 'set_max N' param) for every single ingredient
        ingredient - name of base ingredient, ATTENTION: should NOT contain symbol ' so modify names like this: Hagraven's claw -> Hagravens claw
        """
        print(help)
        continue

    if input_.lower().startswith("set_matches") or input_.lower().startswith("set_max"):
        min_matches = int(input_[-1])
        print("New minimal number of matching effects set to {0}\n".format(str(min_matches)))
        continue

    if input_.lower() == "find_all":
        for ingredient in ingredients.keys():
            matching_ingredients = find_matching_ingredients(ingredient, ingredients)  # dict in format   number_of_matched_effects: {ingredient: [[matching_effects], (effects)]}
            print_results(ingredient, matching_ingredients, min_matches)
        continue

    base = input_

    matching_ingredients = find_matching_ingredients(base, ingredients)  # dict in format   number_of_matched_effects: {ingredient: [[matching_effects], (effects)]}

    print_results(base, matching_ingredients, min_matches)
