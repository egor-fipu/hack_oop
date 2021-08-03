import random
import colorama
from colorama import init, Fore, Back, Style

colorama.init(autoreset=True)


class Thing:
    def __init__(self, name, protection, attack, health):
        self.name = name
        self.protection = protection
        self.attack = attack
        self.health = health

    def __str__(self):
        return (f'{self.name}| защита: {format(self.protection, ".2f")}, '
               f'атака: {self.attack}, здоровье: {self.health}')


class Person:
    def __init__(self, name, base_protection, base_attack, base_health, things=None):
        self.name = name
        self.base_protection = base_protection
        self.base_attack = base_attack
        self.base_health = base_health
        self.things = things

    def get_things(self, set_things):
        """Функция принимает список из вещей и в цикле прибавляет параметры
         каждой вещи к соответствующим параметрам бойца. В конце присваивает
         список переменной self.things бойца (чтобы потом посмотреть,
         чем экипирован боец)"""
        for thing in set_things:
            self.base_protection += thing.protection
            self.base_attack += thing.attack
            self.base_health += thing.health
        self.things = set_things

    def subtract_health(self, enemy_attack):
        """Функция принмиает значение атаки нападающего бойца, и по формуле
        отнимает здоровье. Возвращет значение нанесенного урона (чтобы
        потом выводить в сообщении на арене."""
        attack_damage = enemy_attack - enemy_attack * self.base_protection
        self.base_health -= attack_damage
        return format(attack_damage, '.2f')

    def __str__(self):
        """Делаем проверку if чтобы можно было выводить информацию о бойце
        без экипировки и с ней."""
        if self.things is None:
            return (f'{self.name}| защита: {format(self.base_protection, ".2f")}, '
                    f'атака: {self.base_attack}, здоровье: {self.base_health}')
        if self.things is not None:
            return (f'{self.name}| защита: {format(self.base_protection, ".2f")}, '
                    f'атака: {self.base_attack}, здоровье: {self.base_health} '
                    f'(снаряжение: {", ".join(f.name for f in self.things)})')


class Paladin(Person):
    def __init__(self, name, base_protection, base_attack, base_health):
        Person.__init__(self, name, base_protection, base_attack, base_health)
        self.base_protection *= 2
        self.base_health *= 2


class Warrior(Person):
    def __init__(self, name, base_protection, base_attack, base_health):
        Person.__init__(self, name, base_protection, base_attack, base_health)
        self.base_attack *= 2


def start_thing_list():
    """Функция формирует список вещей (объектов класса Thing).
    Значения для защиты, атаки, здоровья берем рандомные из диапазона,
    имена придумываем сами в списке (сделал список из 40 имен,
    т.к. в соответствии с ТЗ, теоретически каждому из 10 персонажей может быть
    роздано по 4 вещи). В цикле создаются объекты класса Thing и добавляются
    список вещей."""
    name_thing_list = ['sword', 'shield', 'ring', 'vest', 'hat', 'glove',
                       'amulet', 'beads', 'watch', 'belt', 'scarf', 'boots',
                       'pants', 'cap', 'bag', 'shovel', 'axe', 'hammer',
                       'helmet', 'lamp', 'holster', 'handkerchief',
                       'earrings', 'blaster', 'gun', 'sneakers', 'shoes',
                       'phone', 'book', 'glass', 'mace', 'kalashnikov', 'star',
                       'mask', 'notebook', 'huawei', 'xiaomi', 'oppo', 'lg', 'ski']

    thing_list = []
    for index in range(len(name_thing_list)):
        # globals()[<имя переменной>] - создаёт имя переменной из 'str'
        globals()[name_thing_list[index]] = Thing(name=name_thing_list[index],
                                                  protection=random.uniform(0.01, 0.1),
                                                  attack=random.randint(5, 15),
                                                  health=random.randint(5, 20))
        thing_list.append(globals()[name_thing_list[index]])

    # Сортируем по проценту защиты, по возрастанию
    thing_list = sorted(thing_list, key=lambda i: i.protection)

    return thing_list


def start_person_list():
    """Функция формирует список из 10 бойцов. Записываем 20 имен в
    name_person_list. В цикле рандомно (через tmp_type) создаются
    объекты класса Paladin или Warrior и добавляются в список бойцов.
    Значения для защиты, атаки, здоровья берем рандомные из диапазона.
    """
    name_person_list = ['Sergey', 'Ivan', 'Olga', 'Atom', 'Asasin',
                        'Dog', 'Cat', 'Egor', 'Barak', 'Donald',
                        'Robot', 'Nataly', 'Victor', 'Vital', 'Iphone',
                        'Mac', 'Apple', 'Mouse', 'Liu', 'Kano']
    type_person = ['Paladin', 'Warrior']
    person_list = []
    for _ in range(10):
        name = random.choice(name_person_list)
        # чтобы бойцы не повторялись удаляем его из списка
        name_person_list.remove(name)
        tmp_type = random.choice(type_person)
        if tmp_type == 'Paladin':
            globals()[name] = Paladin(name=name + '_(Paladin)',
                                      base_protection=random.uniform(0.01, 0.2),
                                      base_attack=random.randint(10, 20),
                                      base_health=random.randint(50, 80))
        if tmp_type == 'Warrior':
            globals()[name] = Warrior(name=name + '_(Warrior)',
                                      base_protection=random.uniform(0.01, 0.2),
                                      base_attack=random.randint(10, 20),
                                      base_health=random.randint(50, 80))

        person_list.append(globals()[name])

    # Сортируем по здоровью, по возрастанию
    person_list = sorted(person_list, key=lambda i: i.base_health)

    return person_list


def equip(person_list, thing_list):
    """Функция экипирует бойцов и возвращает список экипирвоанных бойцов.
    Принимает 2 списка: неэкипирвоанных бойцов и ввещей. В соответствии с ТЗ
    в цикле каждому бойцу по очереди раздаем от 1 до 4 вещей."""
    for person in person_list:
        tmp_thing_list = []
        for _ in range(random.randint(1, 4)):
            tmp_thing = random.choice(thing_list)
            # чтобы вещи не повторялись удаляем ее из списка
            thing_list.remove(tmp_thing)
            tmp_thing_list.append(tmp_thing)
        # передаем сформированный список вещей бойцу
        person.get_things(tmp_thing_list)

    # Сортируем по здоровью, по возрастанию
    person_list = sorted(person_list, key=lambda i: i.base_health)

    return person_list


def arena(person_list):
    """Функция реализует схватки бойцов. В качестве аргумента принимает
     список экипированных бойцов. Дерутся рандомно все со всеми по два
    бойца. Цикл работает пока в списке не останется один боец"""
    while len(person_list) != 1:
        fighter_1 = random.choice(person_list)
        # удаляем этого бойца из списка, чтобы сам с собой не подрался
        person_list.remove(fighter_1)
        fighter_2 = random.choice(person_list)
        print(f'{fighter_2.name} наносит удар по {fighter_1.name} на '
              f'{fighter_1.subtract_health(fighter_2.base_attack)} урона. '
              f'У {fighter_1.name} осталось здоровья '
              f'{format(fighter_1.base_health, ".2f")}')
        # если боец остался жив - возвращаем его обратно в список
        if fighter_1.base_health > 0:
            person_list.append(fighter_1)
        # если умер - выводим об этом сообщение
        if fighter_1.base_health <= 0:
            print(Fore.RED + f'Боец {fighter_1.name} покидает поле. '
                             f'Его здоровье: {format(fighter_1.base_health, ".2f")}')

    print(Fore.YELLOW + f'Победителем стал {person_list[0]}')


def main():
    thing_list = start_thing_list()
    print(Fore.BLUE + f'Список доступных вещей (всего {len(thing_list)} предметов):')
    for thing in thing_list:
        print(thing)

    print()

    person_list = start_person_list()
    print(Fore.BLUE + 'Список бойцов:')
    for person in person_list:
        print(person)

    print()

    person_list = equip(person_list, thing_list)
    print(Fore.BLUE + 'Снаряжаем бойцов:')
    for person in person_list:
        print(person)

    print()

    print(Fore.BLUE + 'Бойцы выходят на арену:')
    arena(person_list)


main()
