import pymorphy2


def do_a_thing(word):
    cased_list = []
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    if 'NOUN' in p.tag:
        cased_list.append('Единственное число:')
        cased_list.append(p.inflect({'nomn'})[0])
        cased_list.append(p.inflect({'gent'})[0])
        cased_list.append(p.inflect({'datv'})[0])
        cased_list.append(p.inflect({'accs'})[0])
        cased_list.append(p.inflect({'ablt'})[0])
        cased_list.append(p.inflect({'loct'})[0])
        cased_list.append('Множественное число:')
        cased_list.append(p.inflect({'nomn', 'plur'})[0])
        cased_list.append(p.inflect({'gent', 'plur'})[0])
        cased_list.append(p.inflect({'datv', 'plur'})[0])
        cased_list.append(p.inflect({'accs', 'plur'})[0])
        cased_list.append(p.inflect({'ablt', 'plur'})[0])
        cased_list.append(p.inflect({'loct', 'plur'})[0])
        return cased_list
    else:
        return ['У меня не получается просклонять']
