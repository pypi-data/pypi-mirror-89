..
  (c) 2010-2012,2017,2020 by flonatel GmbH & Co. KG / Andreas Florath
  
  SPDX-License-Identifier: GPL-3.0-or-later

  This file is part of rmtoo.
  
  rmtoo is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  rmtoo is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with rmtoo.  If not, see <https://www.gnu.org/licenses/>.


slToo
+++++

Open Source Software development Life cycle Tool

.. image:: https://img.shields.io/github/release/kown7/sltoo.svg
    :target: https://github.com/kown7/sltoo/releases
.. image:: https://github.com/kown7/rmtoo/workflows/build/badge.svg?branch=master
    :target: https://github.com/kown7/rmtoo/actions?query=workflow%3Abuild
.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/gpl-3.0
.. image:: https://img.shields.io/codecov/c/github/codecov/example-python.svg
    :target: https://codecov.io/gh/kown7/rmtoo
.. image:: https://img.shields.io/pypi/v/sltoo.svg
    :target: https://pypi.python.org/pypi/sltoo

.. COMMENT pypi stats are not working
.. COMMENT .. image:: https://img.shields.io/pypi/dm/sltoo.svg
.. COMMENT    :target: https://pypi.python.org/pypi/sltoo

Introduction
============

This is a fork of ``rmtoo``. This fork is supposed to offer
software development life-cycle management SDLC_ options as well, e.g.,
traceability.

At the moment the only difference is the Excel import and export.

.. _SDLC: https://en.wikipedia.org/wiki/Software_development_process

Content
=======

This file contains the following chapters:

.. contents:: Table of Contents


Overview
========

rmtoo is a free and open source requirements management tool.

rmtoo uses a different approach than most other requirements
management tools: it comes as a command line tool which is optimized
for handling requirements. The power of rmtoo lies in the fact that
the development environment can handle the input and output files -
there is no need for a special tool set environment.

Example: if you need to handle baselines (and there often is), rmtoo
can be configured using a revision control system (e.g. git). The
revision control system can handle different revisions, baselining,
tagging, branching and many other things extremely well - there is no
reason to reinvent the wheel and making it less efficient.

Let one thing do one thing.


Unique Feature Set
------------------

rmtoo fits perfectly in a development environment using text editors
and command line tools such as emacs, vi, eclipse, make, maven.

* Use simple text files as input - use your favorite editor
* Many different output formats and artifacts are supported:
    * PDF - with links to dependent requirements
    * HTML - also with links to dependent requirements
    * Requirements dependency graph
    * Requirement count history graph
    * Lists of unfinished requirements including priority and effort
      estimation, e.g., for use in agile project development
* Fully integrated revision control system: git. Usages: history,
  statistics and baseline handling.
* A topic based output handling provides a common set of files for
  different types of output (PDF, HTML, ...)
* Complete support for automatic checking of constraints.
* Analytics modules: Heuristics help to evaluate the quality of
  requirements
* Modules to support commercial biddings based on a given set of
  requirements
* Emacs mode files for editing requirements and topics included
* Experimental output in XML
* Fully integrated with Makefile handling of all artifacts
* Fully modular design: additional output requires minimal effort
* During parsing most common problems are detected: all syntax errors
  and also many semantic errors.
* Fully automated test environment - tests about 95% of the code and
  is shipped with rmtoo packages to check for possible problems in
  different environments.


Installation
============

Dependencies
------------

To use ``sltoo``, other software packages must be installed.

``sltoo`` is written in python.  At least version 3.6 and 3.8 are supported,
but other versions should work just fine.

When you want to create LaTeX or PDF documentation, LaTeX is needed.

For the requirements dependency graph, graphviz is used.

For statistics plot gnuplot is used.  For the estimation module the
python-scipy package is needed.

Typically the packages from your distribution will work. For Ubuntu the
following packages are needed:

.. code::

    sudo apt-get install texlive-font-utils texlive-latex-base \
    texlive-font-utils graphviz gnuplot
    sudo apt-get -y install texlive-latex-recommended \
    texlive-pictures texlive-latex-extra
    pip3 install unflatten

For Fedora these packets:

.. code::

    sudo dnf install gnuplot texlive-latex texlive-tocloft \
    texlive-fancyhdr texlive-epstodpf texlive-metafont texlive-mfware


virtualenv / pip
----------------

This is the preferred installation method — it takes care of installing the
python dependencies correctly.

To install ``sltoo`` in a virtualenv, execute the following steps:

.. code::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install sltoo

This has to be done once.


First Project
=============

Setup
-----

Change to a directory where you want to create the new project. We assume the
``virtualenv`` is available is the same directory (this is not necessary).

.. code::

   git clone git@github.com:kown7/rmtoo.git
   cp -r rmtoo/contrib/template_project MyNewProject


Usage
-----

To create all the artifacts for the template project, execute

.. code::

   cd MyNewProject
   make
   ls artifacts

All the generated files are in the ``artifacts`` directory.

A typical workflow is to change or add requirements, topics or the
configuration in the ``MyNewProject`` directory, run ``make`` again
and check the artifacts.

The generated Excel file ``artifacts/specification.xlsx`` can be used to
change the *Topics* and *Requirements*. If the changes are to be incorporated
into the document simply put the Excel-file into the ``imports`` folder and
run ``make clean && make``. Do not forget to ``git add`` and commit any
changes made! To avoid problems with lock-files, copy the
``artifacts/specification.xlsx`` somwhere else to edit.


Release History
===============

To avoid conflicts with the original ``rmtoo`` releases, the major-numbers
will follow the upstream numbers (for now).

For licensing details see COPYING
See `doc/release_notes` folder for details.
