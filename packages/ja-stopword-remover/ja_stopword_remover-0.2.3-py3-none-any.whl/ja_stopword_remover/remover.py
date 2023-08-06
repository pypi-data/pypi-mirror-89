from .stop_words import Stopword
from sklearn.base import BaseEstimator, TransformerMixin

import copy


class StopwordRemover:
    """
    単語のリストからストップワードにあたる単語を除去して返します。
    """

    def remove(
        self,
        text_list,
        demonstrative=True,
        symbol=True,
        verb=True,
        one_character=True,
        postpositional_particle=True,
        slothlib=True,
        auxiliary_verb=True,
        adjective=True,
    ):
        """
        ストップワードを消去したい単語のリストを引数に指定してください。
        ストップワードを品詞ごとに選びたい場合は、下記の品詞を表す変数にFalseを指定。
        stopwordRemover.remove(text_list, demonstrative=False)
        demonstrative：指示語　pronoun：こそあど言葉　symbol:記号　verb：動詞　one_character：一字
        postpositional_particle：助詞　adjective：形容詞　auxiliary_verb：助動詞　slothlib：slothlib収録語
        """
        stopword_list = []
        stopword = Stopword()
        if demonstrative:
            stopword_list.extend(stopword.demonstrative)

        if symbol:
            stopword_list.extend(stopword.symbol)

        if verb:
            stopword_list.extend(stopword.verb)

        if one_character:
            stopword_list.extend(stopword.one_character)

        if postpositional_particle:
            stopword_list.extend(stopword.postpositional_particle)

        if slothlib:
            stopword_list.extend(stopword.slothlib)

        if auxiliary_verb:
            stopword_list.extend(stopword.auxiliary_verb)

        if adjective:
            stopword_list.extend(stopword.adjective)

        stopword_list = list(set(stopword_list))

        removed_text_list = []

        y = copy.deepcopy(text_list)

        for text in y:
            for stopword in stopword_list:
                while stopword in text:
                    text.remove(stopword)

            removed_text = []
            for word in text:
                removed_text.append(word)

            removed_text_list.append(removed_text)

        return removed_text_list


class SKStopwordRemover(BaseEstimator, TransformerMixin, StopwordRemover):
    """
    単語のリストからストップワードにあたる単語を除去して返します。
    sl-learnのpipeline用です。
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(
        self,
        text_list,
        demonstrative=True,
        symbol=True,
        verb=True,
        one_character=True,
        postpositional_particle=True,
        slothlib=True,
        auxiliary_verb=True,
        adjective=True,
    ):
        return self.remove(
            text_list,
            demonstrative=demonstrative,
            symbol=symbol,
            verb=verb,
            one_character=one_character,
            postpositional_particle=postpositional_particle,
            slothlib=slothlib,
            auxiliary_verb=auxiliary_verb,
            adjective=adjective,
        )
