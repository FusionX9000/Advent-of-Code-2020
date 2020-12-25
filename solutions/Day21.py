from io import TextIOWrapper
from typing import NamedTuple
from functools import reduce
import operator
import re

Food = NamedTuple(
    'Food', [('ingredients', list[str]), ('allergens', list[str])])


def ingredients_with_allergen(foods: list[Food]) -> dict[str, set[str]]:
    allergen_map: dict[str, set[str]] = dict()
    for food in foods:
        for allergen in food.allergens:
            if allergen not in allergen_map:
                allergen_map[allergen] = set(food.ingredients)
            else:
                allergen_map[allergen] = allergen_map[allergen].intersection(
                    set(food.ingredients))
    return allergen_map


def part1(foods: list[Food]) -> int:
    allergen_map = ingredients_with_allergen(foods)
    ingr_with_algn = reduce(lambda a, x: a.union(
        x), allergen_map.values(), set())

    return reduce(lambda a, x: a+len([ingredient for ingredient in x.ingredients if ingredient not in ingr_with_algn]), foods, 0)

    # cleaner but less readable generator expression
    # return sum(ingredient not in ingr_with_algn for food in foods for ingredient in food.ingredients)


def part2(foods: list[Food]) -> int:
    """An indexed priority queue will reduce time complexity from O(N^2) to O(NlogN)"""
    poss_allergen_map = ingredients_with_allergen(foods)
    allergen_map: dict[str, str] = dict()

    unsafe: set[str] = set()

    while len(allergen_map) < len(poss_allergen_map):
        for allergen, ingredients in poss_allergen_map.items():
            ingredients.difference_update(unsafe)
            if len(ingredients) == 1:
                ingredient = next(iter(ingredients))
                unsafe.add(ingredient)
                allergen_map[allergen] = ingredient
        # can remove non-ambiguous allergens in poss_allergen_map here, but worst case time complexity remains.

    return ",".join([ingredient for allergen, ingredient in sorted(allergen_map.items(), key=operator.itemgetter(1))])


def process_input(file: TextIOWrapper) -> list[Food]:
    foods = list()
    for line in file.read().splitlines():
        match = re.search(
            r'(?P<ingredients>.+) \(contains (?P<allergens>.+)\)', line)
        food = Food(match["ingredients"].split(),
                    match["allergens"].split(", "))
        foods.append(food)
    return foods


if __name__ == "__main__":
    with open('../inputs/Day21.txt', 'r') as f:
        foods = process_input(f)
    print("Part 1:", part1(foods))
    print("Part 2:", part2(foods))
