class Word:
    def __init__(self, word):
        self.word = word


class WordInfo(Word):
    def __init__(self, word):
        import pymorphy2
        super().__init__(word)
        self.morph = pymorphy2.MorphAnalyzer()

    def cascade(self, word):
        """Скланяет word по падежам -> str[]

        word -- введённое слово
        """
        cased_list = []
        p = self.morph.parse(word)[0]
        if 'NOUN' in p.tag:
            cased_list.append('Единственное число:')
            if 'Pltm' in p.tag:
                cased_list.append('всегда в мн.ч')
            else:
                cased_list.append(p.inflect({'nomn'})[0])
                cased_list.append(p.inflect({'gent'})[0])
                cased_list.append(p.inflect({'datv'})[0])
                cased_list.append(p.inflect({'accs'})[0])
                cased_list.append(p.inflect({'ablt'})[0])
                cased_list.append(p.inflect({'loct'})[0])
            cased_list.append('Множественное число:')
            if 'Sgtm' in p.tag:
                cased_list.append('всегда в ед.ч')
            else:
                cased_list.append(p.inflect({'nomn', 'plur'})[0])
                cased_list.append(p.inflect({'gent', 'plur'})[0])
                cased_list.append(p.inflect({'datv', 'plur'})[0])
                cased_list.append(p.inflect({'accs', 'plur'})[0])
                cased_list.append(p.inflect({'ablt', 'plur'})[0])
                cased_list.append(p.inflect({'loct', 'plur'})[0])
            return cased_list
        else:
            return ['У меня не получается просклонять']

    def part_of_speech(self, word):
        """Возвращает часть речи word -> str

        word -- введённое слово
        """
        pos = self.morph.parse(word)[0]
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
                   'NPRO': 'местоимение',
                   'PRED': 'предикатив',
                   'PREP': 'предлог',
                   'CONJ': 'союз',
                   'PRCL': 'частица',
                   'INTJ': 'междометие',
                   None: 'нет части речи'}
        return pos_dic[pos.tag.POS]

    def case(self, word):
        """Возвращает падеж word -> str

        word -- введённое слово
        """
        selected_word_case = self.morph.parse(word)[0].tag.case
        case_dic = {'nomn': 'именительный падеж',
                    'gent': 'родительный падеж',
                    'datv': 'дательный падеж',
                    'accs': 'винительный падеж',
                    'ablt': 'творительный падеж',
                    'loct': 'предложный падеж',
                    None: 'Нет падежа'}
        return case_dic[selected_word_case]

    def number(self, word):
        """Возвращает число word -> str

        word -- введённое слово
        """
        num = self.morph.parse(word)[0].tag.number
        num_dic = {'sing': 'ед.ч',
                   'plur': 'мн.ч',
                   None: 'Нет числа'}
        return num_dic[num]

    def gender(self, word):
        """Возвращает род word -> str

        word -- введённое слово
        """
        gen = self.morph.parse(word)[0].tag.gender
        gen_dic = {'masc': 'мужской род',
                   'femn': 'женский род',
                   'neut': 'средний род',
                   None: 'Нет рода'}
        return gen_dic[gen]

    def aspect(self, word):
        """Возвращает совершенность word -> str

        word -- введённое слово
        """
        asp = self.morph.parse(word)[0].tag.aspect
        asp_dic = {'perf': 'совершенный',
                   'impf': 'несовершенный',
                   None: 'нет вида'}
        return asp_dic[asp]

    def transitivity(self, word):
        """Возвращает переходность word -> str

        word -- введённое слово
        """
        tran = self.morph.parse(word)[0].tag.transitivity
        tran_dic = {'intr': 'непереходный',
                    'tran': 'переходный',
                    None: 'нет переходности'}
        return tran_dic[tran]

    def mood(self, word):
        """Возвращает наклонение word -> str

        word -- введённое слово
        """
        moo = self.morph.parse(word)[0].tag.mood
        mood_dic = {'indc': 'изъявительное',
                    'impr': 'повелительное',
                    None: 'либо условное, либо его нет'}
        return mood_dic[moo]

    def tense(self, word):
        """Возвращает время word -> str

        word -- введённое слово
        """
        time = self.morph.parse(word)[0].tag.tense
        ten_did = {'past': 'прошедшее',
                   'pres': 'настоящее',
                   'futr': 'будущее',
                   None: 'нет времени'}
        return ten_did[time]

    def person(self, word):
        """Возвращает лицо word -> str

        word -- введённое слово
        """
        per = self.morph.parse(word)[0].tag.person
        per_dic = {'1per': '1 лицо',
                   '2per': '2 лицо',
                   '3per': '3 лицо',
                   None: 'нет лица'}
        return per_dic[per]

    def voice(self, word):
        """Возвращает залог word -> str

        word -- введённое слово
        """
        vc = self.morph.parse(word)[0].tag.voice
        vc_dic = {'actv': 'действительный',
                  'pssv': 'страдательный',
                  None: 'нет залога'}
        return vc_dic[vc]


class GSEHelper(Word):
    def __init__(self, word='', exam_type='русский язык'):
        self.types = {'Математика': ('https://math-oge.sdamgia.ru/', 650000),
                      'Информатика': ('https://inf-oge.sdamgia.ru/', 8400000),
                      'Русский язык': ('https://rus-oge.sdamgia.ru/', 4500000),
                      'Английский язык': ('https://en-oge.sdamgia.ru/', 650000),
                      'Немецкий язык': ('https://de-oge.sdamgia.ru/', 45000),
                      'Французский язык': ('https://fr-oge.sdamgia.ru/', 30000),
                      'Испанский язык': ('https://sp-oge.sdamgia.ru/', 25000),
                      'Физика': ('https://phys-oge.sdamgia.ru/', 1700000),
                      'Химия': ('https://chem-oge.sdamgia.ru/', 1200000),
                      'Биология': ('https://bio-oge.sdamgia.ru/', 1400000),
                      'География': ('https://geo-oge.sdamgia.ru/', 900000),
                      'Обществознание': ('https://soc-oge.sdamgia.ru/', 2200000),
                      'Литература': ('https://lit-oge.sdamgia.ru/', 100000),
                      'История': ('https://hist-oge.sdamgia.ru/', 400000)}
        self.exam_type = exam_type
        self.task_number = 1
        super().__init__(word)

    def get_task(self):
        """Возвращает случайное задание из ОГЭ по предмету exam_type -> str
        (текст с уже встроенными отступами)

        exam_type -- предмет ОГЭ (default русский язык)
        """
        from random import randint, choice
        from requests import get
        import re
        from bs4 import BeautifulSoup
        max_num = self.types[self.exam_type.lower().capitalize()][1]
        self.task_number = randint(max_num - 100, max_num)
        num = choice(range(2, max_num))
        url = self.types[self.exam_type.lower().capitalize()][0] + \
              f'test?id={str(num)}&nt=True&pub=False'
        html = get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        all_text = soup.get_text()
        lines = (line.strip() for line in all_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # весь текст варианта
        all_text = '\n'.join(chunk for chunk in chunks if chunk)

        chosen_task = all_text.find('Задани')
        remaining_text = all_text[chosen_task:]
        try:
            res = remaining_text.split('№')[1].strip()
            res = res[:res.find('(П')]
            task_text_array = res.split()
            task_text_array[0] = re.sub(r'\d+', '', task_text_array[0])
            task_text_array = ' '.join(x for x in task_text_array)
            task_text_array = re.split(r'(\(\d+\)|\d+\))', task_text_array)
            res = '\n'.join(x for x in task_text_array)
            if any(['Текст, на­чи­на­ю­щий­ся' in res or
                    'Прослушайте текст' in res or
                    'Текст, начинающийся словами' in res or
                    len(res) > 4096]):
                res = 'На этом месте могло бы быть изложение...'
        except IndexError or UnboundLocalError:
            # заново
            res = 'Что-то пошло не так...'
        return res

    def get_meaning(self):
        """Возращает лексическое(ие) значение(ия) self.word -> str

        self.word -- str (default '')
        """
        import bs4
        import requests
        import re
        url = f'https://ru.wiktionary.org/wiki/{self.word}'
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        all_text = soup.get_text()
        lines = (line.strip() for line in all_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        all_text = '\n'.join(chunk for chunk in chunks if chunk)
        # весь текст страницы

        res = re.sub(r'\d+ *Значение', '', all_text)
        res = re.sub(r'(\(.+\)|\[\d\])', '', res[res.find('Значение'):])
        lis = [x.replace('\xa0', ' ') for x in res.split('\n')][1:-1]
        lis = [x for x in lis if not re.match(r'^(\w\. \w\. )', x)]
        try:
            forbidden_index = lis.index('Синонимы') \
                if 'Синонимы' in lis \
                else lis.index('Синонимы[править]')
        except Exception:
            return 'такого слова нет\n'
        to_return = lis[:forbidden_index]
        num = 1
        for i in range(len(to_return)):
            if '◆' in to_return[i] and to_return[i].index('◆') > 5:
                to_return[i] = f'{num}) ' + to_return[i]
                num += 1
        to_return.append('')
        return '\n'.join(to_return)


class Rules(WordInfo):
    def __init__(self, word):
        super().__init__(word)

    def hyphen_rule(self):
        if any([x in self.word for x in ('то', 'либо', 'нибудь', 'кое')]) and \
                '-' not in self.word:
            return 'Пишется через дефис т.к' \
                   ' через дефис пишутся местоимения с ' \
                   'приставкой кое- и суффиксами -то, -либо,' \
                   ' - нибудь'
        if self.word[:len(self.word) // 2] == self.word[len(self.word) // 2 + 1:] \
                and len(self.word) > 1:
            return 'Повторяющиеся слова пишутся через дефис'
        if self.word[:2].lower() in ('по', 'па') and \
                any([x in self.word[len(self.word) - 5:] for x in
                     ('ки', 'ьи', 'ому', 'ему', 'иму', 'ии')]) \
                and '-' not in self.word:
            self.word = 'по' + self.word[3:]
            return 'С дефисом слова пишутся на -ки, -ьи, -ому,- ему с приставкой по'
        return ''
