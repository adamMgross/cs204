"""CS2204 Homework#2: Type design for DNA strands

This file contains the definition and a test suite of the
DNA class. If executed, the test suite will run. If the
VERBOSE global variable is set to true, a detailed stack
trace will be printed for each error, otherwise only a brief
summary if presented.

Name: Adam Gross
VUnetID: grossam2
Email: adam.m.gross.1@vanderbilt.edu
I have neither given nor received unauthorized aid on this assignment.
"""

import sys
import string
import random
import traceback

VERBOSE = False


class DNA:
    """Class for working with DNA strands"""

    def __init__(self, data=''):
        """Initialize object from optional base string

        Parameters:
            data (string), e.g.: 'AcTG'

        The initializer is responsible for checking, if the base string
        (data parameter) contains valid DNA nucleotide characters only
        (i.e. 'A', 'C', 'T', 'G'). This - and all other methods - should
        accept both lower or upper case characters (i.e. 'A' or 'a') and
        should work case insensitive.

        The class can use an arbitrary internal data structure (list, string,
        etc.) to store the given sequence.

        If the data parameter contains invalid characters, a ValueError
        exception is raised.
        """
        for letter in data.lower():
            if letter not in 'actg':
                raise ValueError('invaliid characters')
        self.data_string = data.lower()

    def __str__(self):
        """Convert to string

        Returns the nucleotide sequence as string with all letter capitalized.
        Note: the string contains the nucleotide characters only, no delimiters
        or other formatting characters should be used.

        Eg.:
            >> dna = DNA('AACCTG')
            >> print(dna)
            'AACCTG'
        """
        return self.data_string.upper()

    def __len__(self):
        """Get length of the sequence and return it as an integer"""
        return len(self.data_string)

    def __eq__(self, other):
        """Equivalence test between DNA objects ('==' operator)

        Parameters:
            other (DNA or string): the object to compare with

        Returns True if the two objects represent the exact same DNA sequence,
        otherwise returns False.

        NOTE: the method should support string objects for comparison and
        should handle these case insensitive.
        """
        target = str(other).lower()
        return self.data_string == target

    def __ne__(self, other):
        """Inequivalence test between DNA objects ('!=' operator)

        Parameters:
            other (DNA or string): the object to compare with

        Returns False if the two objects represent the exact same DNA sequence,
        otherwise returns True.

        NOTE: the method should support string objects for comparison and
        should handle these case insensitive.
        """
        return not self.__eq__(other)

    def __getitem__(self, index):
        """Index-based access to single nucleotides in the sequence

        Parameters:
            index (integer): the 0-based index of the nucleotide

        Returns a single nucleotide character at the requested index. The
        letter is capitalized.
        """
        return self.data_string[index].upper()

    def __setitem__(self, index, value):
        """Index-based modification of a single nucleotide in the sequence

        Parameters:
            index (integer): the 0-based index of the nucleotide
            value (string): a single nucleotide character

        This method updates one of the existing nucleotides in the sequence
        at the given index. The method checks if the new value is valid,
        otherwise raises a ValueError exception (see: __init__). Both
        lower and upper case letters should be accepted.

        The method raises an IndexError exception if the index is outside
        of the valid range for the stored sequence.

        No return value is provided.
        """
        if value.lower() not in 'actg':
            raise ValueError('invalid character')
        self.data_string = self.data_string[:index] + value.lower() + self.data_string[index + 1:]

    def __delitem__(self, index):
        """Index-based deletion of a single nucleotide in the sequence

        Parameters:
            index (integer): the 0-based index of the nucleotide

        This method deletes one of the existing nucleotides in the sequence
        at the given index.

        The method raises an IndexError exception if the index is outside
        of the valid range for the stored sequence.

        No return value is provided.
        """
        if index >= len(self.data_string):
            raise IndexError('invalid index')
        temp = list(self.data_string)
        del temp[index]
        self.data_string = ''.join(temp)

    def __contains__(self, other):
        """Containment test between DNA objects ('in' operator)

        Parameters:
            other (DNA or string): the other sequence to find inside this seq

        Returns True if the other sequence is contained by this DNA object
        anywhere in its sequence, otherwise returns False.

        NOTE: the method should support string objects for the contained
        (other) sequence and should handle these case insensitive.
        """
        return str(other).lower() in self.data_string

    def __add__(self, other):
        """Concatenation of two DNA sequences ('+' operator)

        Parameters:
            other (DNA or string): the other sequence to concatenate with

        Returns a new DNA object, which represents the concatenated value of
        the two original sequences (first, this sequence, than the sequence
        of the other parameter). Neither of the original objects will be
        changed.

        NOTE: the method should support string objects for the 'other'
        sequence and should handle these case insensitive.
        """
        return DNA(self.data_string + str(other).lower())

    def __mul__(self, i):
        """Repetition of a DNA sequence ('*' operator)

        Parameters:
            i (integer): the number of repetitions

        Returns a new DNA object, which is created by fully repeating the
        current object's sequence by the given number. The original object
        will not be changed.
        """
        return DNA(''.join([self.data_string for j in range(i)]))

    def find(self, other):
        """Find the position of the first match of a DNA (sub) sequence

        Parameters:
            other (DNA or string): the other sequence to find inside this seq

        Returns the first index (integer) in this sequence where the other
        sequence is found. If the other sequence is not a sub-sequence of
        this object, returns -1.

        NOTE: the method should support string objects for the contained
        (other) sequence and should handle these case insensitive.
        """
        return self.data_string.find(str(other).lower())

    def count(self, other):
        """Count the number of non-overlapping occurences of a (sub) sequence.

        Parameters:
            other (DNA or string): the other sequence to count inside this seq

        Returns the number (integer) of non-overlapping occurrences of the
        other sequence in the current sequence.

        NOTE: the method should support string objects for the counted
        (other) sequence and should handle these case insensitive.

        The method raises a ValueError exception if an empty other sequence is
        provided to find.
        """
        target = str(other).lower()
        if not other:
            raise ValueError('empty target')
        i = 0
        count = 0
        while i < len(self.data_string):
            test = self.data_string[i:i+len(target)]
            if test == target:
                count += 1
                i += len(target)
            else:
                i += 1
        return count

    def reverse(self):
        """Build a reversed DNA sequence

        Returns a new DNA object, which is created by reversing the current
        object's sequence. The original object will not be changed.
        """
        return DNA(''.join([x for x in reversed(self.data_string)]))

    def complement(self):
        """Build a complementary DNA sequence

        Returns a new DNA object, which contains the complementary DNA
        sequence of the current object's sequence (i.e.: A <-> T, C <-> G)
        The original object will not be changed.
        """
        comp = {'a': 't',
                't': 'a',
                'c': 'g',
                'g': 'c'}
        return DNA(''.join([comp[letter] for letter in self.data_string]))

    def transcribe(self):
        """Build an RNA sequence

        Returns a python string, representing the RNA sequence which is
        synthesized from the current DNA sequence (i.e.: all Thymine ('T')
        nucleobase is replaced with Uracil ('U')). The RNA string contains
        capital letters.
        The original object will not be changed.
        """
        return ''.join(['U' if x == 't' else x.upper() for x in self.data_string])

    # EXTRA CREDIT: optional work
    def match(self, other):
        """Calculate a matching score between two DNA sequences

        Parameters:
            other (DNA or string): the other sequence to calculate the
                                   matching score with

        Returns the score (integer) of the matching. The score is calculated
        by finding the longest common sequence in the two DNA strands
        (i.e.: the longest sub sequence which is present in both strands).
        The score is the length of the common sequence.

        NOTE: the method should support string objects for the other sequence
        and should handle these case insensitive.
        """
        pass


###############################################################################
# Testing: ignore everything from here

def generate_base_str(canonical=True, valid=True, max_len=64, min_len=2):
    """Generate a valid base string with proper capitalization"""
    valid_bases = 'ACTG'
    invalid_bases = ''.join([ch for ch in string.ascii_uppercase
                            if ch not in valid_bases])
    bases = valid_bases if valid else invalid_bases
    bases = bases if canonical else bases + bases.lower()

    base_str = []
    for i in range(random.randint(min_len, max_len)):
        base_str.append(random.choice(bases))
    return ''.join(base_str)


def test_construction():
    """Test DNA object construction"""
    dna = DNA()
    for i in range(10):
        dna = DNA(generate_base_str())
    for i in range(10):
        dna = DNA(generate_base_str(canonical=False))
    for i in range(10):
        try:
            dna = DNA(generate_base_str(valid=False))
        except ValueError:
            pass
        else:
            assert False, "Invalid DNA string should generate ValueException"


def test_str():
    """Test string conversion (__str__)"""
    assert str(DNA()) == ''
    for i in range(10):
        dna_str = generate_base_str(canonical=False)
        assert (str(DNA(dna_str))) == dna_str.upper()


def test_len():
    """Test length (__len__)"""
    assert len(DNA()) == 0
    for i in range(10):
        dna_str = generate_base_str(canonical=False, max_len=1024)
        assert (len(DNA(dna_str))) == len(dna_str)


def test_neq():
    """Test equivalence (__eq__, __ne__)"""
    assert DNA() == DNA()
    assert DNA() == ''
    for i in range(10):
        dna_str = generate_base_str(canonical=False)
        assert DNA(dna_str) == DNA(dna_str)
        assert DNA(dna_str) == dna_str
        assert DNA(dna_str) != DNA(dna_str + 'A')
        assert DNA(dna_str) != dna_str + 'C'

def test_indexing():
    """Test indexing (__get/set/del_item__)"""
    for i in range(10):
        dna_str = generate_base_str()
        dna = DNA(dna_str)
        for i_ch, ch in enumerate(dna_str):
            assert dna[i_ch] == ch
        new_str = generate_base_str(max_len=len(dna_str))
        for i_ch, ch in enumerate(new_str):
            dna[i_ch] = random.choice((ch.lower(), ch.upper()))
        while len(new_str) < len(dna):
            del dna[-1]
        assert dna == new_str
        try:
            dna = DNA(dna_str)
            dna[random.randrange(0, len(dna))] = 'F'
        except ValueError:
            pass
        else:
            assert False, 'Invalid DNA letter should generate ValueException'


def test_contains():
    """Test containment (__contains__)"""
    for i in range(10):
        dna_str = generate_base_str(canonical=False)
        begin = random.randrange(len(dna_str))
        end = random.randrange(begin, len(dna_str))
        sub_str = dna_str[begin:end]
        dna = DNA(dna_str)
        sub = DNA(sub_str)
        assert sub in dna
        assert sub_str in dna
        assert dna not in sub
        assert dna_str not in sub


def test_add():
    """Test concatenation (__add__)"""
    assert (DNA() + DNA() == DNA())
    assert (DNA() + DNA('A') == DNA('A'))
    assert (DNA() + 'A' == DNA('A'))

    for i in range(10):
        dna_str1 = generate_base_str(canonical=False)
        dna_str2 = generate_base_str(canonical=False)
        dna1 = DNA(dna_str1)
        dna2 = DNA(dna_str2)
        assert (dna1 + dna2) == dna_str1.upper() + dna_str2.upper()
        assert (dna1 + dna_str2) == dna_str1.upper() + dna_str2.upper()
        assert dna1 == DNA(dna_str1)    # check for side effects
        assert dna2 == DNA(dna_str2)


def test_mul():
    """Test repeating (__mul__)"""
    assert (DNA() * 7) == DNA()
    assert (DNA('A') * 0) == DNA()

    for i in range(10):
        dna_str = generate_base_str()
        dna = DNA(dna_str)
        m = random.randint(0, 10)
        assert str(dna * m) == dna_str * m
        assert dna == DNA(dna_str)    # check for side effects


def test_find():
    """Test find() method"""
    for i in range(100):
        dna_str = generate_base_str(canonical=False, max_len=1024)
        fnd_str = generate_base_str(canonical=False, max_len=5)
        dna = DNA(dna_str)
        assert dna.find(fnd_str) == dna_str.upper().find(fnd_str.upper())
        assert dna.find(DNA(fnd_str)) == dna_str.upper().find(fnd_str.upper())


def test_count():
    """Test count() method"""
    try:
        DNA(generate_base_str()).count('')
    except ValueError:
        pass
    else:
        assert False, 'Empty target should raise ValueError'

    assert DNA('ACTG').count('C') == 1
    assert DNA('AAAG').count('AA') == 1
    assert DNA('AAAG').count('AG') == 1
    assert DNA('AAAGA').count('A') == 4
    assert DNA('AAAGA').count('a') == 4
    assert DNA('AAAGA').count(DNA('A')) == 4


def test_reverse():
    """Test reverse() method"""
    assert DNA().reverse() == DNA()
    for i in range(10):
        dna_str = generate_base_str(canonical=False)
        dna = DNA(dna_str)
        rev_dna = DNA(dna_str).reverse()
        assert isinstance(rev_dna, DNA)
        assert str(rev_dna) == dna_str[::-1].upper()
        assert dna == DNA(dna_str)    # check for side effects


def test_complement():
    """Test complement() method"""
    assert DNA().complement() == DNA()
    assert isinstance(DNA('atcg').complement(), DNA)

    assert DNA('AT').complement() == 'TA'
    assert DNA('GACG').complement() == 'CTGC'
    assert DNA('TTAAAAGAT').complement() == 'AATTTTCTA'
    assert DNA('TTTT').complement() == 'AAAA'
    assert DNA('GTTCGTGCT').complement() == 'CAAGCACGA'
    assert DNA('TGC').complement() == 'ACG'
    assert DNA('TCGATCG').complement() == 'AGCTAGC'
    assert DNA('CTGATC').complement() == 'GACTAG'
    assert DNA('GTAGTCAA').complement() == 'CATCAGTT'

    dna_str = generate_base_str(canonical=False)
    dna = DNA(dna_str)
    dna.complement()
    assert dna == DNA(dna_str)    # check for side effects


def test_transcribe():
    """Test transcribe() method"""
    assert DNA().transcribe() == ''
    assert isinstance(DNA('atcg').transcribe(), str)

    assert DNA('t').transcribe() == 'U'
    assert DNA('cgCtCGc').transcribe() == 'CGCUCGC'
    assert DNA('TGTaTgcGC').transcribe() == 'UGUAUGCGC'
    assert DNA('atCcCCGGaA').transcribe() == 'AUCCCCGGAA'
    assert DNA('tGCcC').transcribe() == 'UGCCC'
    assert DNA('cAtCgCTctTT').transcribe() == 'CAUCGCUCUUU'
    assert DNA('aAtAa').transcribe() == 'AAUAA'
    assert DNA('gGCgAc').transcribe() == 'GGCGAC'
    assert DNA('CGga').transcribe() == 'CGGA'
    assert DNA('TgatTG').transcribe() == 'UGAUUG'

    dna_str = generate_base_str(canonical=False)
    dna = DNA(dna_str)
    dna.transcribe()
    assert dna == DNA(dna_str)    # check for side effects


def test_match():
    """Test match() method (optional, extra credit)"""
    assert DNA('tCcgaCTATGTAgCGttaaCcagcAtActaaACcAaCGtCcTttctaACt').match(
        'tgacACGcCaTAACTgccTTgtaACTCagCTaACAgCttTgTtaaAaa') == 5
    assert DNA('gTGgTtgGtGGATCTggaCAtTgCaccTTAGTGctcCAaCtgAACgcaa').match(
        'aaGTCTgAaTgGgTagaCGaAaCttacatCagTtgagtcAcCaCcACTAAC') == 5
    assert DNA('AataATaTGcgAcATtTgcCGCgtcaaTATGTacaATGCataAatCCGA').match(
        'agCtgttaTCtGCtctGaGcgGtcGcAtttTaCGCTatCtTagtaTgAaGtg') == 5
    assert DNA('tAaAcgCgggtcacTtcAcActgtGGCCtACcGtTCTTtTCTGaGtaGa').match(
        'tGgCATAgGcGgcaCGacggtGCgatcCcCaaGAgGGGgACTCGCgCtaG') == 4
    assert DNA('cACGGgACCgctTttCAGGCcCAaTcCcAGagCCAgtccgGTgCTtGaTC').match(
        'gtcAagtgctCcCGcACTAttcttaTCTAAaCacagtGgGGAAtGGaAGCG') == 5
    assert DNA('aCtttcAgATcgaacaAAtGtGAaCttgtCAgCGtaTTAgTTGcaGatCtcg').match(
        'tgACGAtATTgCgActctGATgAATccTCGagCCtcAGTgCAaGcGCCcATg') == 4
    assert DNA('AaggcGcctTtaCGaTgGCTgAgCTtCaGCgCCCcGGccatTGTtCacGT').match(
        'AaCttGgAGGaGAgGCaaGGTaaGttgGagaTAgagCaaaaTtCgtCttGa') == 4
    assert DNA('TCGGGTGTCGGcGAtaTCgGGcttcATGCGtCGCGcTtagCGGGtTGaCcaT').match(
        'aatgtGTCtAGGggGacCgGcaGGcGCattCgTTgacGgAgCGtaGgCgag') == 6
    assert DNA('AtAcCatcgGTAgATTCTcCtcgGaaGGCtcgatTTaCgaTAaaATCa').match(
        'CgtacAcaaACaCTtaAtAcgcCGTcCCCtGaGtCgCGccCCAcgtagtTga') == 4
    assert DNA('TCacGGttCTcctAcattGAtccGgGcGGTctaCcTAATAGctacCcGCG').match(
        'ggagTGgGAGtcAaGtGcgAgCCTGTTTgcaATGACTgCcCGcTTAgTgt') == 5
    assert DNA('AAgAAaAgCACaTGGccctTacctcgcctgCTTgcGTaAgcGAGCgAcT').match(
        'CatctaTaCTcAtGtaAcaGcTaAactCCaAtAGCccCcCaTCAACtAtG') == 4
    assert DNA('CTtCccaGTtAccAaggtGCtCTcGAGTGTaACaccAaCGgcCATCcacAag').match(
        'AGgCCggACAcATcctTCTggAgGtcgaAaTAgaGcgGtcatCAaCgc') == 5
    assert DNA('GgAAgtTGATTtggGCCAttTtACtaTATAtcttTACGGgGATAACGTTG').match(
        'AgTGtAGCcGgGtCGTtgGcgTGgctTTTGTCTACAAaGcAcCgtGTtGC') == 5
    assert DNA('AGaATtgtagatAgCtgctATGCAACgCGAcGtCGcgGcGCgAGCATgcAg').match(
        'gaTAgTGTTTtAaTGGtTAttTTaagcccCtACTaaTCtCcGaTCgTc') == 5
    assert DNA('CtGTGgtgcaataCGcaCGCgTcTaGccatGGGTTtctcgtGtGcaGGAG').match(
        'CCGTTgataATTtTTtttACcCACCcAGgCaAcTTgcTTacAGGtATTctg') == 4

    for i in range(10):
        dna1 = DNA(generate_base_str(max_len=128, min_len=64))
        dna2 = DNA(generate_base_str(max_len=128, min_len=64))
        assert dna2.match(dna1) == dna1.match(dna2)


if __name__ == '__main__':
    for test in (test_construction,
                 test_str,
                 test_len,
                 test_neq,
                 test_indexing,
                 test_contains,
                 test_add,
                 test_mul,
                 test_find,
                 test_count,
                 test_reverse,
                 test_complement,
                 test_transcribe,
                 test_match):
        try:
            print(test.__doc__, '... ', end='', flush=True)
            test()
            print('PASSED')
        except:
            print('FAILED')
            exc_info = sys.exc_info()
            if VERBOSE:
                traceback.print_exception(*exc_info)
