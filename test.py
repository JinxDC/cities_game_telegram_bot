import geonamescache

gc = geonamescache.GeonamesCache()
all_cities = gc.get_cities()
main_letter = ("ъ")


def get_cyrillic_cities_ending_with(letter):
    global main_letter

    letter = letter.lower()
    matching_cities = []

    for city_data in all_cities.values():
        alternatenames = city_data.get("alternatenames", [])
        for name in alternatenames:
            if name and all('А' <= ch <= 'я' or ch in 'ёЁ -' for ch in name):  # проверка на кириллицу
                if name.lower().endswith(letter):
                    matching_cities.append(name)

    return list(set(matching_cities))  # убираем дубликаты

cities = get_cyrillic_cities_ending_with(main_letter)
print(f"Найдено {len(cities)} городов:")
print(cities)

def get_cyrillic_cities_starting_with(letter):
    global main_letter

    letter = letter.lower()
    matching_cities = []

    for city_data in all_cities.values():
        alternatenames = city_data.get("alternatenames", [])
        for name in alternatenames:
            if name and all('А' <= ch <= 'я' or ch in 'ёЁ -' for ch in name):  # проверка на кириллицу
                if name.lower().startswith(letter):
                    matching_cities.append(name)

    return list(set(matching_cities))  # убираем дубликаты

cities = get_cyrillic_cities_starting_with(main_letter)
print(f"Найдено {len(cities)} городов:")
print(cities)
