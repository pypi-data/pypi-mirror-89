<!--- Local IspellDict: en -->
<!--- SPDX-FileCopyrightText: 2020 Jens Lechtenbörger -->
<!--- SPDX-License-Identifier: CC0-1.0 -->

[![](coverage.svg)](https://pypi.org/project/coverage/)
[![REUSE status](https://api.reuse.software/badge/gitlab.com/oer/functional_dependencies)](https://api.reuse.software/info/gitlab.com/oer/cs/functional-dependencies)

# Overview
This package provides an
[Open Educational Resource](https://en.wikipedia.org/wiki/Open_educational_resources)
(OER) to refresh prior knowledge about functional dependencies (FDs)
and normalization of relational database schemata.  Towards that goal,
the package implements algorithms for the manipulation of functional
dependencies; the package’s doc string explains the used vocabulary
and contains examples.

Selected algorithms:
- FD.rminimize(): Return a minimal cover of r-minimal FDs
- FDSet.closure(): Return closure of attributes under given FDs
- FDSet.lminimize(): Return minimum subset of lhs that determines rhs
- FDSet.key(): Return a key
- FDSet.basis(): Return non-redundant r- and l-minimal basis
- RelSchema.synthesize(): Normalize via synthesis into set of 3NF schemata

# Side goal
Besides, the package may serve as sample Python code that respects
usual coding conventions, which are checked with
[pre-commit hooks](https://pre-commit.com).
The configuration file [.pre-commit-config.yaml](https://gitlab.com/oer/cs/functional-dependencies/-/blob/master/.pre-commit-config.yaml)
specifies test tools used here.

# Origin of code
The code here is based on
[that file](https://gitlab.com/oer/cs/programming/-/blob/master/functional_dependencies.py),
which will not be maintained any longer.
