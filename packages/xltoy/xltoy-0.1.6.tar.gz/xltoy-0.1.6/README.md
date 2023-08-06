![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xltoy)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/glaucouri/xltoy)
![Travis (.com)](https://img.shields.io/travis/com/glaucouri/xltoy)


## XLtoy: 

The ultimate toolkit for Microsoft Excel modelers and mod-operations. 

#### The name

*XLtoy* it's a word pun that starts from **exel to py** concept, but the *p* seem superfluous here and *xlto(p)y* became 
XLtoy, more funny.

### Description

After many year in this field, i found that is too difficult, and often useless, to analyze an entire workbook, 
this approach force to write unpredictable an inefficient algorithms and doesn't work because often we are interested only in a subset 
of all cells. So main idea, is to identify a subset of areas of interest, defined as *working areas*
and focus XLtoy only on these, so with minimum changes to an existent sheet, the parser can handle it and produce 
useful information. If you can apply some **simple 
[rules](https://raw.githubusercontent.com/glaucouri/xltoy/main/rules.md)**
you are ready to go!

**So ?**

XLtoy framework can read, parse, diff, validate, manage changes and run out of the box complicated models written 
using Microsoft Excel. Not all features are ready up to now, but the development plan is show below.

This tool is useful for users that write, share, maintain and deploy models written in Excel. Many kind of model are 
well handled by XLtoy:
- validation models
- rule based models
- financial models
- forecasting models

In a collaborative environment, for example, a change management tools, can save a lot of time and money, comparing two version 
is useful know what's changed in the data or formulas. No less, dev-ops (od mod-ops) than need an instrument to identify 
uniquely model, data, and changes on each delivery. Model differ can identify precisely which and where are the differences 
using syntactic or semantic algorithm.

### Installation
It's strongly suggested to use virtualenv:
```
>pip3 install virtualenv
>python3 -m venv XLtoy_pyenv
>source XLtoy_pyenv/bin/activate
```

```
>pip install xltoy

# Or from source:

>git clone https://github.com/glaucouri/XLtoy.git
>cd XLtoy/
>python setup.py install
```

All features now are accessible via *xltoy* cli command.

```
> xltoy --help

Usage: xltoy [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  collect
  diff

```
### Documentation
 

* [working rules](https://raw.githubusercontent.com/glaucouri/xltoy/main/rules.md)
* [Tutorial](https://raw.githubusercontent.com/glaucouri/xltoy/main/tutorial.md)



#### Framework descriptions

The XLtoy Framework is composed of many subpackages, all of them are reachable via cli sub command.

* **xltoy.collector** : It read an excel workbook and extract all needed information, following rules described here. 
This means equations, named or anonymous exogenous data and parameters. 
Result can be represented as hierarchical yaml or json. This functionality solve problem related 
to *change management*, *versioning*, *model governance* and *diff* operation.

* **xltoy.parser** : It can parse all collected equation in order to understand for each all the dependencies, 
and transliterate each in a readable and working python code.
All relations between formulas are stored in a dependency graph in a key:value structure 
using the mnemonic name for each equation. This data structure allow us to do a topological analysis of entire
system of equations

## Time line
The framework will be finished in some steps, i want to share the release plane because 
with the release of first version i will need feedback, use cases and tester.  

#### Version 0.1: first working version:
* it define [working rules](https://raw.githubusercontent.com/glaucouri/xltoy/main/rules.md)
* fully testes with py3.6 to py3.8
* collector can read data,formulas and can show an entire workbook as yaml or json.
* **diff** works with data and formulas too, it can compare 2 workbook or a representation of it yaml 
or json.
* with fingerprint option model can be marked (like a md5 for a file)

#### Version 0.2: parser feature:
* parser can understand excel formula (probably not all syntax)
* in memory graph representation with all relation between equations.
* can find all predecessors and successors of a given equation.
* models can be exported as graph or python code.
* execution of python version can be done in a notebook or a stand alone env.

#### Version 0.3: executor feature:
* data can be stored as pandas DataFrame
* models can be binded to external data. Binding feature. and can be run on huge data set.

#### Version 0.4: big data feature:
* model can be distributed on a spark cluster and executed in order to work on big data
