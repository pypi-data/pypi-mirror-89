# denden_extension

Denden_extension is a [Python-Markdown](https://github.com/waylan/Python-Markdown) extension enables [DenDenMarkdown](https://github.com/denshoch/DenDenMarkdown) syntax in Python-Markdown.


## Requirement

Python-Markdown >= 3.0.0, < 3.1


## Install

```
pip install denden_extension
```


## Usage

Designate denden_extension as extension with other extensions when you use the Python-Markdown.

```
>>> import markdown
>>> from denden_extension import DenDenExtension
>>> markdown_text = '{電子出版|でんししゅっぱん}を手軽に'
>>> html_text = markdown.markdown(markdown_text, extensions=['markdown.extensions.extra', 'markdown.extensions.nl2br', 'markdown.extensions.sane_lists', DenDenExtension()])
>>> html_text
'<p><ruby>電子出版<rt>でんししゅっぱん</rt></ruby>を手軽に</p>'
```

or

```
>>> import markdown
>>> from denden_extension import DenDenExtension
>>> markdown.markdownFromFile(
...             input='markdown_text.md',
...             output='html_text.html',
...             encoding='utf-8',
...             extensions=['markdown.extensions.extra', 'markdown.extensions.nl2br', 'markdown.extensions.sane_lists', DenDenExtension()],
...             )
```

or

```
python -m markdown -x markdown.extensions.extra -x markdown.extensions.nl2br -x markdown.extensions.sane_lists -x denden_extension markdown_text.md > html_text.html
```

For more details of usage of Python-Markdown, see [Python-Markdown documentation](https://pythonhosted.org/Markdown/).

### Options

You can disable some features of denden_extension.

Disable Chunk file syntax:

```
>>> html_text = markdown.markdown(markdown_text, extensions=['markdown.extensions.extra', 'markdown.extensions.nl2br', 'markdown.extensions.sane_lists', DenDenExtension(docbreak=False)])
```

Disable Footnotes with epub:type attribute:

```
>>> html_text = markdown.markdown(markdown_text, extensions=['markdown.extensions.extra', 'markdown.extensions.nl2br', 'markdown.extensions.sane_lists', DenDenExtension(footnote=False)])
```

If you run the Python-Markdown from command line with an extension with options, you need to prepare the configuration file. For more details, see [Python-Markdown documentation](https://pythonhosted.org/Markdown/cli.html#using-extensions).


## Description

DenDenMarkdown is an extended Markdown syntax fitted for Japanese and EPUB publishing.  
Denden_extension enables the following DenDenMarkdown syntax in Python-Markdown.

- [Japanese Ruby Annotation](http://conv.denshochan.com/markdown#ruby)
- [Tate-Chu-Yoko](http://conv.denshochan.com/markdown#tcy)
- [Footnotes with epub:type attribute](http://conv.denshochan.com/markdown#footnotes) *1
- [EPUB pagebreak syntax](http://conv.denshochan.com/markdown#pagebreak)
- [Chunk file syntax](http://conv.denshochan.com/markdown#docbreak) *2

*1 Denden_extension depends on the Python-Markdown's footnotes extension for implementing this feature. So you also need the [markdown.extensions.footnotes](https://pythonhosted.org/Markdown/extensions/footnotes.html) or [markdown.extensions.extra](https://pythonhosted.org/Markdown/extensions/extra.html) which includes the footnotes extension.  
*2 Three or more equal signs ('=') on a line by themselves is replaced by a horizontal rule tag with docbreak class attribute (\<hr class="docbreak" /\>).

DenDenMarkdown inherits its syntax from [PHP Markdown Extra](https://michelf.ca/projects/php-markdown/extra/). In Python-Markdown, PHP Markdown Extra syntax is enabled by [markdown.extensions.extra](https://pythonhosted.org/Markdown/extensions/extra.html) and [markdown.extensions.sane_lists](https://pythonhosted.org/Markdown/extensions/sane_lists.html), which are included in the Python-Markdown Library.  
Also, DenDenMarkdown adopts GFM style line break. This can be enabled by [markdown.extensions.nl2br](https://pythonhosted.org/Markdown/extensions/nl2br.html), which is included with the Python-Markdown too.

If you only want to use DenDenMarkdown's original syntax, you just need to designate only markdown.extensions.footnotes and denden_extension.  
If you don't use footnotes, only denden_extension is necessary.

The following syntax of DenDenMarkdown is not implemented in denden_extension.

- Twitter account autolink syntax

For more details of DenDenMarkdown syntax, see http://conv.denshochan.com/markdown (Japanese).


## Change log

- 2.0 (2020-12-21) -- suport only Python-Markdown >= 3.0.0, < 3.1 and Python3
- 1.0 (2016-04-29) -- formal release
- 0.1 (2015-08-23) -- first experimental release


## Contact

[Contact form](https://docs.google.com/forms/d/1MAbCiYzr4w_q0XbQgX56voC0dq7N7WrhN95LzhgERp8/viewform)
