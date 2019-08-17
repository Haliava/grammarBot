import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def part_of_speech(word):
    pos = morph.parse(word)[0]
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
    return pos_dic[pos.tag.POS]


def case(word):
    case = morph.parse(word)[0].tag.case
    case_dic = {'nomn': 'именительный падеж',
                'gent': 'родительный падеж',
                'datv': 'дательный падеж',
                'accs': 'винительный падеж',
                'ablt': 'творительный падеж',
                'loct': 'предложный падеж',
                None: 'Нет падежа'}
    return case_dic[case]


def number(word):
    num = morph.parse(word)[0].tag.number
    num_dic = {'sing': 'ед.ч',
               'plur': 'мн.ч',
               None: 'Нет числа'}
    return num_dic[num]


def gender(word):
    gen = morph.parse(word)[0].tag.gender
    gen_dic = {'masc': 'мужской род',
               'femn': 'женский род',
               'neut': 'средний род',
               None: 'Нет рода'}
    return gen_dic[gen]


def aspect(word):
    asp = morph.parse(word)[0].tag.aspect
    asp_dic = {'perf': 'совершенный',
               'impf': 'несовершенный',
               None: 'нет вида'}
    return asp_dic[asp]


def transitivity(word):
    tran = morph.parse(word)[0].tag.transitivity
    tran_dic = {'intr': 'непереходный',
                'tran': 'переходный',
                None: 'нет переходности'}
    return tran_dic[tran]


def mood(word):
    moo = morph.parse(word)[0].tag.mood
    mood_dic = {'indc': 'изъявительное',
                'impr': 'повелительное',
                None: 'либо условное, либо его нет'}
    return mood_dic[moo]


def tense(word):
    time = morph.parse(word)[0].tag.tense
    ten_did = {'past': 'прошедшее',
               'pres': 'настоящее',
               'futr': 'будущее',
               None: 'нет времени'}
    return ten_did[time]


def person(word):
    per = morph.parse(word)[0].tag.person
    per_dic = {'1per': '1 лицо',
               '2per': '2 лицо',
               '3per': '3 лицо',
               None: 'нет лица'}
    return per_dic[per]


def voice(word):
    vc = morph.parse(word)[0].tag.voice
    vc_dic = {'actv': 'действительный',
              'pssv': 'страдательный',
              None: 'нет залога'}
    return vc_dic[vc]
