# -*- coding: utf-8 -*-
import sys
from typing import Union

from ar_corrector.corrector import Corrector

crr = Corrector()


class CompoundSplitter:
    """Compound splitter class."""

    @staticmethod
    def words_concat(word_1: str, word_2: str) -> Union[str, list]:
        """
        Words concat method.

        Args:
            word_1: first compound word
            word_2: second compound word.

        Returns:
            List of words.
        """
        if isinstance(word_1, str) or isinstance(word_1, unicode):
            word_1 = [word_1]
        if isinstance(word_2, str) or isinstance(word_2, unicode):
            word_2 = [word_2]
        return word_1 + word_2

    @staticmethod
    def spliter(word: str) -> Union[str, list]:
        """
        Spliter method.

        Args:
            word: word want to split.
        Returns:
            list of words.

        """
        right_compound1_upper = None
        right_compound2_upper = None
        max_index = len(word)
        for index, char in enumerate(word):
            left_compound = word[0:max_index - index]
            right_compound_1 = word[max_index - index:max_index]
            right_compound_2 = word[max_index - index + 1:max_index]
            if right_compound_1:
                right_compound1_upper = right_compound_1[0].isspace()
            if right_compound_2:
                right_compound2_upper = right_compound_2[0].isspace()
            if index > 0 and len(left_compound) > 1 and not crr.is_known(left_compound):
                left_compound = left_compound
            is_left_compound_valid_word = len(left_compound) > 1 and crr.is_known(left_compound)
            if is_left_compound_valid_word and \
                    ((not CompoundSplitter().spliter(right_compound_1) == '' and not right_compound1_upper)
                     or right_compound_1 == ''):
                return [compound for compound in
                        CompoundSplitter().words_concat(left_compound, CompoundSplitter().spliter(right_compound_1))
                        if not compound == '']
            elif is_left_compound_valid_word and word[max_index - index:max_index - index + 1] == 's' and \
                    ((not CompoundSplitter().spliter(right_compound_2) == '' and not right_compound2_upper)
                     or right_compound_2 == ''):
                return [compound for compound in
                        CompoundSplitter().words_concat(left_compound, CompoundSplitter().spliter(right_compound_2))
                        if not compound == '']
        if not word == '' and crr.is_known(word):
            return [word]
        elif not word == '' and crr.is_known(word):
            return [word]
        else:
            return ''

    @staticmethod
    def processing(word: str) -> list:
        """
        Processing method.
        Args:
            word: target word

        Returns:
            list of words after splitting.
        """
        if crr.is_known(word) or word.isdigit():
            return [word]
        compound = CompoundSplitter().spliter(word) if CompoundSplitter().spliter(word) == list else list(
            CompoundSplitter().spliter(word))
        return compound


if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_word = sys.argv[1]
    else:
        print("[Using]\n compound_word_splitter_ar.py  [target word]")
        sys.exit(0)
    if sys.version_info[0] > 2:
        unicode = str
    print(CompoundSplitter().processing(target_word))
