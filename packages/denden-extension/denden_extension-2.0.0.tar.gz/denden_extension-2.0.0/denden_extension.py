# -*- coding: utf-8 -*-
"""
DenDen Extension for Python-Markdown
=======================================

Adds DenDenMarkdown handling to Python-Markdown.

See <https://github.com/muranamihdk/denden_extension>
for documentation.

Copyright (c) 2015-2020 Hideaki Muranami

License: [MIT](http://opensource.org/licenses/MIT)

"""

import re
import time

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.postprocessors import Postprocessor
from markdown import util


"""
Placeholder for two bytes space
---------------------------------------------------------------"""

TWO_BYTES_SPACE = "klzzwxh:{}".format(time.time())  # 'klzzwxh:12288'


"""
The actual regular expressions for patterns
---------------------------------------------------------------"""

# 改ページ（ファイル分割）：===
DOC_BREAK_RE = r"^[ ]{0,3}(=+[ ]{0,2}){3,}[ ]*"

#エスケープ記号： \<
ESCAPE_RE = r"\\(.)"

# ページ番号：[%5] or [%%5]
PAGE_NUM_RE = r"^\s*?\[(%%?)(\d+?)\]\s*$"  # block
PAGE_NUM_INLINE_RE = r"\[(%%?)(\d+?)\]"  # inline

# ルビ：{電子書籍|でん|し|しょ|せき}
RUBY_RE = r"{([^\|]+?)((?:\|.+?)+?)}"

# ルビ文字：|でん|し|しょ|せき
RUBY_RTS_RE = r"\|([^\|]+)"

# 横中縦：^21^世紀
TATE_CHU_YOKO_RE = r"(\^)(.+?)\^"


"""
The classes for DenDenMarkdown syntax
---------------------------------------------------------------"""

class TwoBytesSpacePreprocessor(Preprocessor):
    """ Replace two bytes spaces with a placeholder. """

    def run(self, lines):
        new_lines = []
        for line in lines:
            new_lines.append(re.sub(r"　", TWO_BYTES_SPACE, line))
        return new_lines


class DocBreakProcessor(BlockProcessor):
    """ Process Doc Breaks. """

    SEARCH_RE = re.compile(DOC_BREAK_RE, re.MULTILINE)

    def test(self, parent, block):
        m = self.SEARCH_RE.search(block)
        if m and (m.end() == len(block) or block[m.end()] == "\n"):
            self.match = m
            return True
        return False

    def run(self, parent, blocks):
        block = blocks.pop(0)
        prelines = block[:self.match.start()].rstrip("\n")
        if prelines:
            self.parser.parseBlocks(parent, [prelines])
        el = util.etree.SubElement(parent, 'hr')
        el.set('class', 'docbreak')
        postlines = block[self.match.end():].lstrip("\n")
        if postlines:
            blocks.insert(0, postlines)


class PageNumProcessor(BlockProcessor):
    """ Process Page Numbers. """
    RE = re.compile(PAGE_NUM_RE)

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        percent_sign = m.group(1)
        page_num = m.group(2)
        el = util.etree.SubElement(parent, 'div')
        el.attrib = {
            'id': "pagenum_{}".format(page_num),
            'class': "pagenum",
            'title': page_num,
            'epub:type': "pagebreak"}
        if percent_sign == "%%":
            el.text = page_num.strip()


class DenDenEscapeInlineProcessor(InlineProcessor):
    """
    Add "|" into the characters which should be escaped and
    Return an escaped character.
    """
    def handleMatch(self, m, data):
        char = m.group(1)
        ESCAPED_CHARS = self.md.ESCAPED_CHARS
        ESCAPED_CHARS.append("|")
        if char in self.md.ESCAPED_CHARS:
            return "{}{}{}".format(util.STX, ord(char), util.ETX), m.start(0), m.end(0)
        else:
            return None, m.start(0), m.end(0)


class PageNumTagProcessor(InlineProcessor):
    """
    Return a 'pagenum' class element containing the matching text.
    """
    def handleMatch(self, m, data):
        matched_part = m.group(0)
        percent_sign = m.group(1)
        page_num = m.group(2)
        if m.start(0) == 0 or data[m.start(0) -1] == "\n":  # if line(data) starts with matched_part or matched_part is preceded by a new line
            el = util.etree.Element('div')
        else:  # There is a string before the matched part
            el = util.etree.Element('span')
        el.attrib = {
            'id': "pagenum_{}".format(page_num),
            'class': "pagenum",
            'title': page_num,
            'epub:type': "pagebreak"}
        if percent_sign == "%%":
            el.text = page_num
        return el, m.start(0), m.end(0)


class RubyTagProcessor(SimpleTagInlineProcessor):
    """Return a ruby element."""
    def handleMatch(self, m, data):
        ruby_tag, rt_tag = self.tag.split(",")
        ruby_texts = re.findall(RUBY_RTS_RE, m.group(2))
        body_text = m.group(1)
        if len(body_text) == len(ruby_texts):
            ruby_element = util.etree.Element(ruby_tag)
            ruby_element.text = body_text[0]
            for idx, ruby_text in enumerate(ruby_texts):
                rt_element = util.etree.SubElement(ruby_element, rt_tag)
                rt_element.text = ruby_text
                if idx +1 < len(body_text):
                    rt_element.tail = body_text[idx+1]
        else:
            ruby_element = util.etree.Element(ruby_tag)
            ruby_element.text = body_text
            rt_element = util.etree.SubElement(ruby_element, rt_tag)
            rt_element.text = re.sub(r'\|', '', m.group(2))
        return ruby_element, m.start(0), m.end(0)


class TateChuYokoTagProcessor(SimpleTagInlineProcessor):
    """
    Return a 'tcy' class element containing the matching text.
    """
    def handleMatch(self, m, data):
        el = util.etree.Element(self.tag)
        el.text = m.group(2)
        el.set('class', 'tcy')
        return el, m.start(0), m.end(0)


class PageNumPostprocessor(Postprocessor):
    """ Reorder attributes of page number elements. """

    DIV_RE = re.compile(r'<div class="pagenum" epub:type="pagebreak" id="pagenum_(\d+)" title="\d+">')
    SPAN_RE = re.compile(r'<span class="pagenum" epub:type="pagebreak" id="pagenum_(\d+)" title="\d+">')

    def sub_div(self, m):
        text = '<div id="pagenum_{}" class="pagenum" title="{}" epub:type="pagebreak">'.format(m.group(1), m.group(1))
        return text

    def sub_span(self, m):
        text = '<span id="pagenum_{}" class="pagenum" title="{}" epub:type="pagebreak">'.format(m.group(1), m.group(1))
        return text

    def run(self, text):
        text = self.DIV_RE.sub(self.sub_div, text)
        text = self.SPAN_RE.sub(self.sub_span, text)
        return text


class FootnoteSubPostprocessor(Postprocessor):
    """ Substitute Footnotes for XHTML and Epub Format. """

    FOOT_NOTE_ANCHOR_RE = re.compile(r'<sup id="fnref:(\d+)"><a class="footnote-ref" href="#fn:\d+" rel="footnote">(.*?)</a></sup>')
    FOOT_NOTE_TARGET_RE = re.compile(r'<li id="fn:(\d+)">\n(.*?)<a class="footnote-backref" href="#fnref:\d+" rev="footnote" title="Jump back to footnote \d+ in the text">&#8617;</a></p>\n</li>', re.DOTALL)

    def sub_anc(self, m):
        text = '<a id="fnref_{}" href="#fn_{}" rel="footnote" class="noteref" epub:type="noteref">{}</a>'.format(m.group(1), m.group(1), m.group(2))
        #text = '<a class="noteref" epub:type="noteref" href="#fn_{}" id="fnref_{}" rel="footnote" >{}</a>'.format(m.group(1), m.group(1), m.group(2))
        return text

    def sub_tgt(self, m):
        text = '<li>\n<div id="fn_{}" class="footnote" epub:type="footnote">\n{}<a href="#fnref_{}">&#9166;</a></p>\n</div>\n</li>'.format(m.group(1), m.group(2), m.group(1))
        #text = '<li>\n<div class="footnote" epub:type="footnote" id="fn_{}">\n{}<a href="#fnref_{}">&#9166;</a></p>\n</div>\n</li>'.format(m.group(1), m.group(2), m.group(1))
        return text

    def run(self, text):
        text = text.replace('<div class="footnote">', '<div class="footnotes" epub:type="footnotes">')
        text = self.FOOT_NOTE_ANCHOR_RE.sub(self.sub_anc, text)
        text = self.FOOT_NOTE_TARGET_RE.sub(self.sub_tgt, text)
        return text


class TwoBytesSpacePostprocessor(Postprocessor):
    """ Restore two bytes spaces. """

    def run(self, text):
        return text.replace(TWO_BYTES_SPACE, "　")


"""
The DenDenMarkdown Extension Class
---------------------------------------------------------------"""

class DenDenExtension(Extension):
    """ DenDen Extension for Python-Markdown. """

    def __init__(self, **kwargs):
        self.config = {
            'docbreak' : [True, 'Insert Documentation Breaks.'],
            'pagenum' : [True, 'Insert Page Numbers.'],
            'footnote' : [True, 'Substitute Footnotes for XHTML and Epub Format.']}
        super(DenDenExtension, self).__init__(**kwargs)

    #def extendMarkdown(self, md, md_globals):
    def extendMarkdown(self, md):
        '''
        All items are automatically sorted by the value of the “priority” parameter such that the item with the highest value will be processed first.
        https://python-markdown.github.io/extensions/api/#registries
        If an item is registered with a "name" which already exists, the
        existing item is replaced with the new item.
        markdown/util.py
        '''

        # Add preprocessors.
        #md.preprocessors.add('two_bytes_space', TwoBytesSpacePreprocessor(), '_begin')
        md.preprocessors.register(TwoBytesSpacePreprocessor(md), 'two_bytes_space', 40)  # top

        # Add blockprocessors.
        if self.getConfig('docbreak'):
            md.parser.blockprocessors.register(DocBreakProcessor(md.parser), 'doc_break', 45)  # after 'hr'
        if self.getConfig('pagenum'):
            md.parser.blockprocessors.register(PageNumProcessor(md.parser), 'page_num', 15)  # before 'paragraph'

        # Add inline patterns.
        md.inlinePatterns.register(DenDenEscapeInlineProcessor(ESCAPE_RE, md), 'escape', 180)  # overwrite
        if self.getConfig('pagenum'):
            try:
                md.inlinePatterns.register(PageNumTagProcessor(PAGE_NUM_INLINE_RE, md), 'page_num', 15)  # after 'strong2'
            except ValueError:
                md.inlinePatterns.register(PageNumTagProcessor(PAGE_NUM_INLINE_RE, md), 'page_num', 5)  # after 'emphasis2'
        try:
            md.inlinePatterns.register(RubyTagProcessor(RUBY_RE, 'ruby,rt'), 'denden_ruby', 4)  # after 'page_num'
        except ValueError:
            md.inlinePatterns.register(RubyTagProcessor(RUBY_RE, 'ruby,rt'), 'denden_ruby', 3)  # end
        md.inlinePatterns.register(TateChuYokoTagProcessor(TATE_CHU_YOKO_RE, 'span'), 'denden_tate_chu_yoko', 2)  # after 'denden_ruby'

        # Add postprocessors.
        if self.getConfig('pagenum'):
            md.postprocessors.register(PageNumPostprocessor(md), 'page_num', 8)  # end
        if self.getConfig('footnote'):
            """
            try:
                md.postprocessors.add('footnote_sub', FootnoteSubPostprocessor(), '>footnote')  # after the 'footnote' key item
            except ValueError:
                #md.postprocessors.add('footnote_sub', FootnoteSubPostprocessor(), '_end')
                md.postprocessors.register(FootnoteSubPostprocessor(md), 'footnote_sub', 6)
            """
            md.postprocessors.register(FootnoteSubPostprocessor(md), 'footnote_sub', 6)  # end
        md.postprocessors.register(TwoBytesSpacePostprocessor(md), 'two_bytes_space', 4)  # end


def makeExtension(**kwargs):
    """ Return an instance of the DenDenExtension class """
    return DenDenExtension(**kwargs)
