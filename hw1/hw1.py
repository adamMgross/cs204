"""CS2204 Homework#1: CDC Mortality Statistics

Functions for processing a sanitized CDC Mortality Database

Name: Adam Gross
VUnetID: grossam2
Email: adam.gross@vannderbilt.edu

Honor Statement: I have neither given nor received unauthorized aid on this assignment.
"""
from cdc import db, code_names


def deaths_by_code(code):
    """Return number of deaths by ICD-10 code.

    Parameters:
        code (string), e.g.: 'D35.2'

    Returns an integer, the number of deaths in a
    single ICD-10 category, e.g.: 50.
    If the category is not found, returns None.
    """
    for entry in db:
        if entry[0] == code:
            return entry[1]
    return None


def most_deaths():
    """Return the ICD-10 code and number of deaths for the deadliest category.

    Returns a two element list of [code, number_of_deaths], e.g. ['D35.2', 50]
    """
    db.sort(key=lambda x: x[1])
    return db[-1]

def codes_above(threshold):
    """Return a list of ICD-10 codes which have deaths above threshold.

    The list contains all the ICD-10 codes where the number of deaths are
    higher than the specified threshold.

    Parameters:
        threshold: (int) minimum threshold for number of deaths

    Returns a list of codes, e.g. ['D35.2', 'I46.1', 'Y17']
    """
    index = 0
    db.sort(key=lambda x: x[1])
    if threshold > db[-1][1]:
        index = len(db)
    else:
        while db[index][1] < threshold:
            index += 1
    return [entry[0] for entry in db[index:]]


def codes_below(threshold):
    """Return a list of ICD-10 codes with number of deaths below threshold.

    The list contains all the ICD-10 codes where the number of deaths are lower
    than the specified threshold.

    Parameters:
        threshold: (int) maximum threshold for number of deaths

    Returns a list of codes, e.g. ['D35.2', 'I46.1', 'Y17']
    """
    return([entry[0] for entry in db if entry[1] < threshold])


def sum_deaths_by_codes(codes):
    """Return the aggregated number of deaths by multiple ICD-10 codes.

    Parameters:
        codes (list of strings), e.g.: ['D35.2', 'I46.1', 'Y17']

    Returns an integer, the aggregated (sum) number of deaths across the
    specified list of ICD-10 categories, e.g.: 1713
    """
    return sum([code[1] if code[0] in codes else 0 for code in db])


def sum_deaths_by_query(query):
    """Return the aggregated number of deaths by a query string.

    Parameters:
        query: (string) search string to match against ICD-10 category names

    Returns an integer, the aggregated (sum) number of deaths across all ICD-10
    categories matching the search string.
    NOTE: The search string (query) matches the category if and only if it is a
    case insensitive substring of the name of the ICD-10 category name (NOT
    THE CATEGORY CODE!).

    E.g.: sum_deaths_by_query('heart')
    """
    codes = []
    for codename in code_names:
        if query.lower() in code_names[codename].lower():
            codes.append(codename)
    return sum_deaths_by_codes(codes)


# EXTRA CREDIT: optional work
def sum_deaths_by_chapter(chapter):
    """Return the aggregated number of deaths in an ICD-10 chapter.

    Parameters:
        chapter: (int) the chapter number (see NOTE), e.g.: 9

    Returns an integer, the aggregated (sum) number of deaths across all ICD-10
    categories belonging to the specified chapter.
    See: https://en.wikipedia.org/wiki/ICD-10 for the chapter-code assignment.
    NOTE: ICD-10 uses roman numerals for chapters, but here we just use the
    integer value (e.g. IX - Diseases of the circulatory system is represented
    by 9)
    """
    if chapter < 1 or chapter > 22:
        return 0
    chapters = {1: ('A00', 'B99'),
                2: ('C00', 'D48'),
                3: ('D50', 'D89'),
                4: ('E00', 'E90'),
                5: ('F00', 'F99'),
                6: ('G00', 'G99'),
                7: ('H00', 'H59'),
                8: ('H60', 'H95'),
                9: ('I00', 'I99'),
                10: ('J00', 'J99'),
                11: ('K00', 'K93'),
                12: ('L00', 'L99'),
                13: ('M00', 'M99'),
                14: ('N00,' 'N99'),
                15: ('O00', 'O99'),
                16: ('P00', 'P96'),
                17: ('Q00', 'Q99'),
                18: ('R00', 'R99'),
                19: ('S00', 'T98'),
                20: ('V01', 'Y98'),
                21: ('Z00', 'Z99'),
                22: ('U00', 'U99')
                }

    def valid_icd(prefix):
        for codename in code_names:
            if prefix in codename:
                return True
        return False

    def generate_icd_list(chapter):
        begin, end = chapters[chapter]
        icd_list = []
        current = begin
        while current[0] <= end[0]:
            if int(current[1:]) > int(end[1:]):
                break
            if valid_icd(current):
                for i in range(10):
                    code = '{}.{}'.format(current, i)
                    if code in code_names:
                        icd_list.append(code)

            number = int(current[1:])
            next_num = (int(current[1:]) + 1) % 100
            letter = current[0]
            if next_num == 0:
                letter = chr(ord(letter) + 1)
                next_num = '00'
            if int(next_num) < 10:
                next_num = '0' + str(next_num)
            current = letter + str(next_num)
        return icd_list
    return sum_deaths_by_codes(generate_icd_list(chapter))

###############################################################################
# TEST functions : ignore everything from here

def test_deaths_by_code():
    """Test deaths_by_code() function"""
    assert deaths_by_code('') is None
    assert deaths_by_code('does not exist') is None
    assert deaths_by_code('I82.3') == 3
    assert deaths_by_code('W17') == 481


def test_most_deaths():
    """Test most_deaths() function"""
    assert list(most_deaths()) == ['I25.1', 161745]


def test_codes_above():
    """Test codes_above() function"""
    from random import randint
    assert len(codes_above(-1)) == len(db)
    assert len(codes_above(1e10)) == 0
    for i in range(10):
        thr = randint(0, 200000)
        codes = codes_above(thr)
        for code, deaths in db:
            assert ((code in codes) and (deaths > thr)) or (deaths <= thr)


def test_codes_below():
    """Test codes_below() function"""
    from random import randint
    assert len(codes_below(1e10)) == len(db)
    assert len(codes_below(0)) == 0
    for i in range(10):
        thr = randint(0, 200000)
        codes = codes_below(thr)
        for code, deaths in db:
            assert ((code in codes) and (deaths < thr)) or (deaths >= thr)


def test_sum_deaths_by_codes():
    """Test sum_deaths_by_codes() function"""
    from random import sample, randint
    assert sum_deaths_by_codes([]) == 0
    for i in range(10):
        codes, deaths = zip(*sample(db, randint(0, len(db)-1)))
        assert sum_deaths_by_codes(codes) == sum(deaths)


def test_sum_deaths_by_query():
    """Test sum_deaths_by_query() function"""
    assert sum_deaths_by_query('heart') == 302182
    assert sum_deaths_by_query('lung') == 161113
    assert sum_deaths_by_query('diabetes') == 76587
    assert sum_deaths_by_query('too much running') == 0
    assert sum_deaths_by_query('broccoli') == 0


def test_sum_deaths_by_chapter():
    """Test sum_deaths_by_chapter() function (optional, extra credit)"""
    assert sum_deaths_by_chapter(0) == 0
    assert sum_deaths_by_chapter(99) == 0
    assert sum_deaths_by_chapter(1) == 70413
    assert sum_deaths_by_chapter(7) == 34
    assert sum_deaths_by_chapter(13) == 13344


if __name__ == '__main__':
    import sys
    import traceback

    for test in (test_deaths_by_code,
                 test_most_deaths,
                 test_codes_above,
                 test_codes_below,
                 test_sum_deaths_by_codes,
                 test_sum_deaths_by_query,
                 test_sum_deaths_by_chapter):
        try:
            print(test.__doc__, '... ', end='', flush=True)
            test()
            print('PASSED')
        except:
            print('FAILED')
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
