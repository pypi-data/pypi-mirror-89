import abc
import re


class AbstractSentenceSegmenter(abc.ABC):

    @abc.abstractmethod
    def cut(self, paragraph, **kwargs):
        raise NotImplementedError()


class SentenceSegmenter(AbstractSentenceSegmenter):

    def __init__(self, regex='([﹒﹔﹖﹗．；。！？;]["’”」』]{0,2}|：(?=["‘“「『]{1,2}|$))', **kwargs):
        self.pattern = re.compile(regex)

    def cut(self, paragraph, **kwargs):
        sentences = []
        for sent in self.pattern.split(paragraph):
            if self.pattern.match(sent) and sentences:
                sentences[-1] += sent
            else:
                sentences.append(sent)
        return sentences
