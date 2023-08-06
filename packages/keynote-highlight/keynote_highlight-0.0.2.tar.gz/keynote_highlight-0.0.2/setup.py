# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keynote_highlight']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.3,<3.0.0',
 'black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'pyperclip>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['keyhi = keynote_highlight.main:main']}

setup_kwargs = {
    'name': 'keynote-highlight',
    'version': '0.0.2',
    'description': 'Code highlighter with preset, but customizable settings',
    'long_description': '# Keynote highlighter\n\n*Code highlighter with preset, but customizable settings*\n\n## Install\n\nRequires python 3.9\n\n`pip install keynote-highlight`\n\n## Motivation\n\nHave you ever wanted to highlight your code for presentation with just one command from cli? Then this tool is for you!\n\nLet\'s say, you want to make a presentation on Riemann sum and you want to add this code to your slides.\n\n```python\nfrom typing import Callable, Iterator\n\n\ndef linspace(a: float, b: float, n=100) -> Iterator[tuple[float, float]]:\n    """Linspace in pure python"""\n    delta = abs((b - a) / n)\n    x_i_min_1 = a\n    x_i = a + delta\n    yield x_i_min_1, x_i\n    for _ in range(n):\n        x_i_min_1 = x_i\n        x_i += delta\n        yield x_i_min_1, x_i\n    yield x_i, b\n\n\ndef riemann_sum(f: Callable[[float], float], range_: tuple[float, float]) -> float:\n    """\n    Calculate Riemann sum\n    \n    :param f: function of a single argument\n    :param range_: range of values this function is defined on\n    :return: Riemann sum\n    """\n    res = 0\n    for x_i_min_1, x_i in linspace(*range_):\n        res += f((x_i+x_i_min_1)/2) * (x_i - x_i_min_1)\n    return res\n\nif __name__ == "__main__":\n    print(riemann_sum(lambda x: x, (-4, 3)))\n```\n\nThis is how it\'s going to look:\n\n[![keyhi_demo.png](images/keyhi_demo.png)](https://yadi.sk/i/Cy2s4W1BV5kVsA)\n\n## Features\n- Select any language and styles to highlight code available in pygments;\n- Change font size of your code;\n- Load and save code straight to clipboard;\n    - You can also your default cli code editor as a source of code instead of clipboard.\n- For python you can change width of your code and apply black code formatter.\n\n```\n➜ keyhi --help \nUsage: keyhi [OPTIONS]\n\n  Highlight code for keynote.app from clipboard and save result to\n  clipboard.\n\n  STYLE Style for code\n\n  FONTSIZE Font size to use\n\n  LANGUAGE Programming language of source code\n\n  INP What is the source of code\n\n  LINE-WIDTH python only. Format code to fit width\n\nOptions:\n  -l, --language [abap|apl|abnf|as3|as|ada|adl|agda|aheui|alloy|at|ampl|html+ng2|ng2|antlr-as|antlr-csharp|antlr-cpp|antlr-java|antlr|antlr-objc|antlr-perl|antlr-python|antlr-ruby|apacheconf|applescript|arduino|arrow|aspectj|asy|augeas|autoit|ahk|awk|bbcbasic|bbcode|bc|bst|bare|basemake|bash|console|bat|befunge|bib|blitzbasic|blitzmax|bnf|boa|boo|boogie|brainfuck|bugs|camkes|c|cmake|c-objdump|cpsa|aspx-cs|csharp|ca65|cadl|capdl|capnp|cbmbas|ceylon|cfengine3|chai|chapel|charmci|html+cheetah|js+cheetah|cheetah|xml+cheetah|cirru|clay|clean|clojure|clojurescript|cobolfree|cobol|coffee-script|cfc|cfm|cfs|common-lisp|componentpascal|coq|cpp|cpp-objdump|crmsh|croc|cryptol|cr|csound-document|csound|csound-score|css+django|css+erb|css+genshitext|css|css+php|css+smarty|cuda|cypher|cython|d|d-objdump|dpatch|dart|dasm16|control|delphi|devicetree|dg|diff|django|docker|dtd|duel|dylan-console|dylan|dylan-lid|ecl|ec|earl-grey|easytrieve|ebnf|eiffel|iex|elixir|elm|emacs|email|erb|erlang|erl|html+evoque|evoque|xml+evoque|execline|ezhil|fsharp|fstar|factor|fancy|fan|felix|fennel|fish|flatline|floscript|forth|fortranfixed|fortran|foxpro|freefem|gap|gdscript|glsl|gas|genshi|genshitext|pot|cucumber|gnuplot|go|golo|gooddata-cl|gosu|gst|groff|groovy|hlsl|haml|html+handlebars|handlebars|haskell|hx|hexdump|hsail|hspec|html+django|html+genshi|html|html+php|html+smarty|http|haxeml|hylang|hybris|idl|icon|idris|igor|inform6|i6t|inform7|ini|io|ioke|irc|isabelle|j|jags|jasmin|java|js+django|js+erb|js+genshitext|js|js+php|js+smarty|jcl|jsgf|jsonld|json|jsp|jlcon|julia|juttle|kal|kconfig|kmsg|koka|kotlin|lsl|css+lasso|html+lasso|js+lasso|lasso|xml+lasso|lean|less|lighty|limbo|liquid|lagda|lcry|lhs|lidr|live-script|llvm|llvm-mir-body|llvm-mir|logos|logtalk|lua|mime|moocode|doscon|make|css+mako|html+mako|js+mako|mako|xml+mako|maql|md|mask|mason|mathematica|matlab|matlabsession|minid|ms|modelica|modula2|trac-wiki|monkey|monte|moon|mosel|css+mozpreproc|mozhashpreproc|javascript+mozpreproc|mozpercentpreproc|xul+mozpreproc|mql|mscgen|mupad|mxml|mysql|css+myghty|html+myghty|js+myghty|myghty|xml+myghty|ncl|nsis|nasm|objdump-nasm|nemerle|nesc|newlisp|newspeak|nginx|nim|nit|nixos|notmuch|nusmv|numpy|objdump|objective-c|objective-c++|objective-j|ocaml|octave|odin|ooc|opa|openedge|pacmanconf|pan|parasail|pawn|peg|perl6|perl|php|pig|pike|pkgconfig|plpgsql|pointless|pony|postscript|psql|postgresql|pov|powershell|ps1con|praat|prolog|promql|properties|protobuf|psysh|pug|puppet|pypylog|python2|py2tb|pycon|python|pytb|qbasic|qvto|qml|rconsole|rnc|spec|racket|ragel-c|ragel-cpp|ragel-d|ragel-em|ragel-java|ragel|ragel-objc|ragel-ruby|raw|rd|reason|rebol|red|redcode|registry|resource|rexx|rhtml|ride|roboconf-graph|roboconf-instances|robotframework|rql|rsl|rst|rts|rbcon|rb|rust|sas|splus|sml|sarl|sass|scala|scaml|scdoc|scheme|scilab|scss|shexc|shen|sieve|silver|singularity|slash|slim|slurm|smali|smalltalk|sgf|smarty|snobol|snowball|solidity|sp|sourceslist|sparql|sql|sqlite3|squidconf|ssp|stan|stata|sc|swift|swig|systemverilog|tap|tnt|toml|tads3|tasm|tcl|tcsh|tcshcon|tea|ttl|termcap|terminfo|terraform|tex|text|thrift|tid|todotxt|tsql|treetop|turtle|html+twig|twig|ts|typoscriptcssdata|typoscripthtmldata|typoscript|ucode|unicon|urbiscript|usd|vbscript|vcl|vclsnippets|vctreestatus|vgl|vala|aspx-vb|vb.net|html+velocity|velocity|xml+velocity|verilog|vhdl|vim|wdiff|webidl|whiley|x10|xquery|xml+django|xml+erb|xml|xml+php|xml+smarty|xorg.conf|xslt|xtend|extempore|yaml+jinja|yaml|yang|zeek|zephir|zig|auto]\n                                  Programming language to highlight\n  -f, --fontsize INTEGER          Fontsize of resulting text\n  -s, --style [default|emacs|friendly|colorful|autumn|murphy|manni|monokai|perldoc|pastie|borland|trac|native|fruity|bw|vim|vs|tango|rrt|xcode|igor|paraiso-light|paraiso-dark|lovelace|algol|algol_nu|arduino|rainbow_dash|abap|solarized-dark|solarized-light|sas|stata|stata-light|stata-dark|inkpot]\n                                  Theme of resulting text\n  -i, --inp [clipboard|editor]    What is the source of code\n  -w, --line-width INTEGER        python only. Format code to fit width\n  --help                          Show this message and exit.\n```\n',
    'author': 'Nikita Churikov',
    'author_email': 'nikita@chur.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/churnikov/keynote-highlight',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
