from itertools import product


class Course(object):

    def __init__(self, info_dict):
        self.code = str(info_dict['code'])
        self.title = ''.join(str(c) for c in info_dict['title'] if ord(c) < 128)
        self.credits = info_dict['credits']
        self.lec = {str(key): val for key, val in info_dict['lec'].iteritems()}
        self.tut = {str(key): val for key, val in info_dict['tut'].iteritems()}
        self.lab = {str(key): val for key, val in info_dict['lab'].iteritems()}
        self.matching = info_dict['matching']
        self.time = self.generate_time()
        self.options = self.generate_options()

    def generate_time(self):
        time = {}
        for k, v in self.lec.iteritems():
            key = 'L' + k
            time[key] = v
        for k, v in self.tut.iteritems():
            key = 'T' + k
            time[key] = v
        for k, v in self.lab.iteritems():
            key = 'LA' + k
            time[key] = v
        return time

    def generate_options(self):
        options = {}
        lec = self.lec.keys()
        tut = self.tut.keys()
        lab = self.lab.keys()
        self.lec['e'], self.tut['e'], self.lab['e'] = [], [], []
        # dummy entry for list concatenation
        if not lec:
            lec = 'e'
        if not tut:
            tut = 'e'
        if not lab:
            lab = 'e'
        if self.matching:
            group = len(self.lec.keys()) - 1
            for _lec, _tut, _lab in product(lec, tut, lab):
                for number in map(str, range(1, 1 + group)):
                    temp = _lec + _tut + _lab
                    if temp.count(number) + temp.count('e') == 3:
                    # secret formula validating match
                        val = self.lec[_lec] + self.tut[_tut] + self.lab[_lab]
                        key = ''
                        if _lec != 'e':
                            key += 'L' + _lec + ' '
                        if _tut != 'e':
                            key += 'T' + _tut + ' '
                        if _lab != 'e':
                            key += 'LA' + _lab + ' '
                        options[key[:-1]] = val
        else:
            for _lec, _tut, _lab in product(lec, tut, lab):
                val = self.lec[_lec] + self.tut[_tut] + self.lab[_lab]
                key = ''
                if _lec != 'e':
                    key += 'L' + _lec + ' '
                if _tut != 'e':
                    key += 'T' + _tut + ' '
                if _lab != 'e':
                    key += 'LA' + _lab + ' '
                options[key[:-1]] = val
        if options.keys() == ['']:
            return {}
        else:
            return options
