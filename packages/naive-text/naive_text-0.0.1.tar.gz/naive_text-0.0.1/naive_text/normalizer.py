import abc

from opencc import OpenCC


def char_half_to_full_width(uchar):
    """Convert half width chars to full width chars."""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:
        return uchar
    if inside_code == 0x0020:
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def str_half_to_full_width(ustring):
    return ''.join(char_half_to_full_width(x) for x in ustring)


def char_full_to_half_width(uchar):
    """"Convert half width chars to full width chars."""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return uchar
    return chr(inside_code)


def str_full_to_half_width(ustring):
    return ''.join(char_full_to_half_width(x) for x in ustring)


class AbstractTextNormalizer(abc.ABC):

    @abc.abstractmethod
    def normalize(self, text, **kwargs):
        raise NotImplementedError()


class TextNormalizer(AbstractTextNormalizer):

    def __init__(self, **kwargs):
        self.chinese_t2s = None
        self.chinese_s2t = None

    def to_half_width(self, text, **kwargs):
        if not text:
            return ""
        to_half_chars = set(kwargs.get('to_half_width_chars', []))
        res = []
        for c in text:
            if c in to_half_chars:
                res.append(char_full_to_half_width(c))
            else:
                res.append(c)
        return ''.join(res)

    def to_full_width(self, text, **kwargs):
        if not text:
            return ""
        to_full_chars = set(kwargs.get('to_full_width_chars', []))
        res = []
        for c in text:
            if c in to_full_chars:
                res.append(char_half_to_full_width(c))
            else:
                res.append(c)
        return ''.join(res)

    def to_lower(self, text, **kwargs):
        if not text:
            return ""
        return text.lower()

    def to_upper(self, text, **kwargs):
        if not text:
            return ""
        return text.uppper()

    def to_simplified(self, text, **kwargs):
        if not text:
            return ""
        if not self.chinese_t2s:
            self.chinese_t2s = OpenCC('t2s')
        return self.chinese_t2s.convert(text)

    def to_traditional(self, text, **kwargs):
        if not text:
            return ""
        if not self.chinese_s2t:
            self.chinese_s2t = OpenCC('s2t')
        return self.chinese_s2t.convert(text)

    def normalize(self, text, **kwargs):
        if not text:
            return ""
        if kwargs.get('to_half_width', False):
            text = self.to_half_width(text, **kwargs)
        if kwargs.get('to_full_width', False):
            text = self.to_full_width(text, **kwargs)
        if kwargs.get('to_simplified', False):
            text = self.to_simplified(text, **kwargs)
        if kwargs.get('to_traditional', False):
            text = self.to_traditional(text, **kwargs)
        if kwargs.get('to_lower', False):
            text = self.to_lower(text, **kwargs)
        if kwargs.get('to_upper', False):
            text = self.to_upper(text, **kwargs)
        return text
