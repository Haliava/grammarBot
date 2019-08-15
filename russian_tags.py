import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def part_of_speech(word):
    pos = morph.parse(word)[0].tag.POS if len(morph.parse(word)) > 1 else morph.parse(word).tag.POS
    pos_dic = {'NOUN': 'существительное',
               'VERB': 'глагол',
               'INFN': 'инфинитив',
               'ADJF': 'полное прилагательное',
               'ADJS': 'краткое прилагательное',
               'COMP': 'компаратив',
               'PRTF': 'полное причастие',
               'PRTS': 'краткое причастие',
               'GRND': 'деепричастие',
               'NUMR': 'числительное',
               'ADVB': 'наречие',
               'NPRO': 'местоимение-существительное',
               'PRED': 'предикатив',
               'PREP': 'предлог',
               'CONJ': 'союз',
               'PRCL': 'частица',
               'INTJ': 'междометие'}
    return pos_dic[pos]


def case(word):
    try:
        case = morph.parse(word)[0].tag.case if len(morph.parse(word)) > 1 else morph.parse(word).tag.case
    except Exception:
        return 'Нет падежа'
    case_dic = {'nomn': 'именительный падеж',
                'gent': 'родительный падеж',
                'datv': 'дательный падеж',
                'accs': 'винительный падеж',
                'ablt': 'творительный падеж',
                'loct': 'предложный падеж',
                None: 'Нет падежа'}
    return case_dic[case]


def number(word):
    try:
        num = morph.parse(word)[0].tag.number if len(morph.parse(word)) > 1 else morph.parse(word).tag.number
    except Exception:
        return 'Нет числа'
    num_dic = {'sing': 'ед.ч',
               'plur': 'мн.ч',
               None: 'Нет числа'}
    return num_dic[num]


def gender(word):
    try:
        gen = morph.parse(word)[0].tag.gender if len(morph.parse(word)) > 1 else morph.parse(word).tag.gender
    except Exception:
        return 'Нет рода'
    gen_dic = {'masc': 'мужской род',
               'femn': 'женский род',
               'neut': 'средний род',
               None: 'Нет рода'}
    return gen_dic[gen]


def aspect(word):
    asp = morph.parse(word).tag.aspect
    asp_dic = {'perf': 'совершенный',
               }
