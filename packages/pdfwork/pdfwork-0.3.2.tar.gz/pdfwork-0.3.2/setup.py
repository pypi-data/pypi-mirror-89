# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdfwork']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.3.0,<9.0.0', 'pikepdf>=2.0.0,<3.0.0', 'tqdm>=4.52.0,<5.0.0']

entry_points = \
{'console_scripts': ['pdfwork = pdfwork.cli:cli_main']}

setup_kwargs = {
    'name': 'pdfwork',
    'version': '0.3.2',
    'description': '基于 pikepdf 封装的命令行工具，处理 PDF 文件用',
    'long_description': '#######\nPDFWork\n#######\n\n基于 [pikepdf](https://github.com/pikepdf/pikepdf) 封装的一个便于使用的 pdf 处理命令行工具。\n提供以下功能：\n\n-   书签（也叫目录）\n    -   导入、导入、抹除PDF文件中的书签\n-   合并 PDF\n-   分割 PDF\n\n安装方法\n========\n\n可以通过 pip 或 pipx 安装：\n\n.. code:: sh\n\n    # pip\n    pip install pdfwork\n    # pipx\n    pipx install pdfwork\n\n使用\n====\n\n合并 PDF 文件\n-------------\n\n假设你有一堆 PDF 文件，那么你可以使用 ``pdfwork merge`` 子命令来将它们合并。使用 ``-o`` 选项指定合并后的文件保存路径。\n\n要输入需要合并的文件，有三种方法：\n\n1. 直接在命令行中输入： ``-i alpha.pdf beta.pdf gamma.pdf``\n2. 在以 ``@`` 开头的文本文件（例如 ``@pdf.list.txt``）中以 **每行一个** 的形式编写 PDF 片段的路径，然后用 ``-i @pdf.list.txt`` 的形式指定列表文件。程序会在指定文件中读取 PDF 片段的路径。\n3. 或者留空，这样会从 stdin 读取文件路径，同样是每行一个。\n\n.. code:: sh\n\n    $ pdfwork merge -o merged.pdf -i a.pdf b.pdf c.pdf\n\n    $ pdfwork merge -o merged.pdf -i @abc.list.txt\n\n    $ pdfwork merge -o\n    a.pdf\n    b.pdf\n    c.pdf\n\n``@abc.list.txt`` 的内容如下::\n\n    a.pdf\n    b.pdf\n    c.pdf\n\n拆分 PDF 文件\n-------------\n\npdfwork 可以将一个完整的 PDF 文件按页拆分成单页 PDF。使用 ``-i origin.pdf`` 输入源文件路径。然后通过 ``-o prefix.%03d.pdf`` 设置输出文件名模板。\n\n可以在模板中使用 Python format 风格的占位符（详见 <https://docs.python.org/zh-cn/3/library/string.html#formatspec>），例如 ``{:d}`` 或 ``{:04d}`` 之类，像十六进制的 ``{:x}``、八进制的 ``{:o}`` 和二进制的 ``{:b}`` 也是可以使用的。\n\n当 ``-o`` 参数未指定时，程序会使用类似于 ``{:0d}.pdf`` 这样的模板，但自动推导宽度，以确保生成 001.pdf ~ 999.pdf 样式的文件。\n\n.. code:: sh\n\n    $ pdfwork split -i origin.pdf -o "origin.{:04d}.pdf"\n\n导入导出 PDF 文件的书签\n-----------------------\n\npdfwork 提供一种字面形式的书签描述语言，可以描述书签的标题、页码和嵌套关系。导入时，将描述语言转换成 PDF 的书签结构写入 PDF；导出时，从 PDF 中读取书签结构，编码成描述语言。\n\n描述语言以一行作为一条书签，通过 ``@`` 将一行分为 标题和页码两个部分::\n\n    标题 @ 页码\n\n并且用缩进来表示嵌套层级::\n\n    根书签 @ 页码\n        子书签 1 @ 页码\n        子书签 2\n\n这里可以观察到， “子书签 2” 没有输入页码。这是因为如果相邻的书签具有相同的页码，那么除了第一条之外的书签页码都可以省略不写，由程序自动推导。\n\n.. code:: sh\n\n    $ pdfwork outline --pdf origin.pdf import -i bookmarks.txt -o origin.bookmarked.pdf --offset 20\n\n    $ pdfwork outline --pdf origin.pdf export -o bookmarks.exported.txt\n\n在导入时，通常需要输入一个参数 ``--offset``，这个参数表示正文页码和物理页码的偏差。例如，大多数书籍都有封面、扉页、前言、目录等结构，这些结构并没有算在目录的页码里。因此，当从书籍的目录中将页码转抄过来，就会存在一个值为 offset 的偏差。假设正文第 1 页在 PDF 中的实际页码是 21，那么 offset = 21 - 1 = 20。如果所操作的书籍没有此类问题，那么可以省略此参数，令程序使用默认值 offset = 0 。另外，程序会自动生成序号。\n\n在导出时，各目录的页码已经计算成了物理页码，偏差归零。\n\n在 ``docs/example.bookmark.txt`` 有一份示例的描述语言文本。\n\n抹除书签\n--------\n\n保存去除了书签信息的 PDF 版本。\n\n.. code:: sh\n\n    $ pdfwork outline --pdf origin.pdf erase -o erased.pdf',
    'author': 'zombie110year',
    'author_email': 'zombie110year@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zombie110year/pdfwork',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
