# auditwheel changelog

## HEAD

## 3.3.1

Released Dec. 24, 2020

### User-facing changes
- [FEATURE] Vendor `wheel` to improve user experience ([#275](https://github.com/pypa/auditwheel/pull/275))

### Housekeeping
- Fix twine check warning
- Modernize Python syntax using `pyupgrade --py36-plus` ([#278](https://github.com/pypa/auditwheel/pull/278))
- Remove usage of `wheel` imported helpers for python 2/3 compatibility ([#276](https://github.com/pypa/auditwheel/pull/276))
- Bump `wheel` to 0.36.2 ([#273](https://github.com/pypa/auditwheel/pull/273))

## 3.3.0

Released Dec. 6, 2020

### User-facing changes
- [FEATURE] Add `--strip` option to repair ([#255](https://github.com/pypa/auditwheel/pull/255))
- [FEATURE] Add manylinux_2_24 policy ([#264](https://github.com/pypa/auditwheel/pull/264))
- [FEATURE] Add python 3.9 support ([#265](https://github.com/pypa/auditwheel/pull/265))
- [FEATURE] Drop python 3.5 support ([#261](https://github.com/pypa/auditwheel/pull/261))

### Housekeeping
- The PyPA has adopted the PSF code of conduct ([#256](https://github.com/pypa/auditwheel/pull/256))
- Remove unused `find_package_dirs` function ([#267](https://github.com/pypa/auditwheel/pull/267))
- Bump `wheel` to 0.36.1 ([#269](https://github.com/pypa/auditwheel/pull/269))

## 3.2.0

Released Jul. 1, 2020

### User-facing changes
- [FEATURE] Ensure that system-copied libraries are writable before running patchelf 
  ([https://github.com/pypa/auditwheel/pull/237](#237))
- [FEATURE] Preserve RPATH in extension modules ([https://github.com/pypa/auditwheel/pull/245](#245))

## 3.1.1

Released Apr. 25, 2020

### User-facing changes
- [BUGFIX] Always exclude ELF dynamic linker/loader from analysis ([#213](https://github.com/pypa/auditwheel/pull/213))
  - Fixes "auditwheel repair marked internal so files as shared library dependencies ([#212](https://github.com/pypa/auditwheel/issues/212))"
- [BUGFIX] Correctly detect non-platform wheels ([#224](https://github.com/pypa/auditwheel/pull/224))
  - Fixes "Auditwheel addtag returns stack trace when given a none-any wheel ([#218](https://github.com/pypa/auditwheel/issues/218))"
- [BUGFIX] Fix obsolete wheel usage in addtag ([#226](https://github.com/pypa/auditwheel/pull/226))

### Housekeeping
- Upgrade `wheel` to 0.34.2 ([#235](https://github.com/pypa/auditwheel/pull/235))

## 3.1.0

Released Jan. 29, 2020

### User-facing changes
- [FEATURE] Put libraries in `$WHEELNAME.libs` to avoid vendoring multiple copies 
  of the same library ([#90](https://github.com/pypa/auditwheel/pull/90))

### Housekeeping
- Upgrade `wheel` to 0.34  ([#223](https://github.com/pypa/auditwheel/pull/223))

## 3.0.0

Released Jan. 11, 2020

- No user facing changes since 3.0.0.0rc1.

## 3.0.0.0rc1

Released Nov. 7, 2019

### User-facing changes
- [FEATURE] manylinux2014 policy ([#192](https://github.com/pypa/auditwheel/pull/192), [#202](https://github.com/pypa/auditwheel/pull/202))
- [FEATURE] Update machine detection ([#201](https://github.com/pypa/auditwheel/pull/201))
- [FEATURE] Advertise python 3.8 support and run python 3.8 in CI ([#203](https://github.com/pypa/auditwheel/pull/203))

### Housekeeping
- Run manylinux tests using current python version ([#199](https://github.com/pypa/auditwheel/pull/199))

## 2.1.1

Released Oct. 08, 2019

### User-facing changes

- [BUGFIX] Add missing symbols for manylinux2010_i686 policy ([#141](https://github.com/pypa/auditwheel/pull/141), [#194](https://github.com/pypa/auditwheel/pull/194))
- [BUGFIX] Fix --version for python 3.10 ([#189](https://github.com/pypa/auditwheel/pull/189))

### Housekeeping

- Simplify policy unit test ([#188](https://github.com/pypa/auditwheel/pull/188))

## 2.1

Released Jul. 28, 2019

- Instead of outputting only the first shared library found in `purelib`,
  include a list of all offending files ([#143](https://github.com/pypa/auditwheel/pull/143))
- Better policy detection ([#150](https://github.com/pypa/auditwheel/pull/150))
- Use `AUDITWHEEL_PLAT` environment variable as a default option to --plat
  ([#151](https://github.com/pypa/auditwheel/pull/150))
- Workaround for `patchelf` bug not setting `DT_RUNPATH` correctly
  ([#173](https://github.com/pypa/auditwheel/pull/173))
- Remove `libcrypt.so.1` from library whitelist
  ([#182](https://github.com/pypa/auditwheel/pull/182))

## 2.0

Released Jan. 23, 2019

- After approximately 2 months of testing, no new regressions were detected in
  the 2.0 release candidate.
- Note that this release contains the implementation of [PEP
  571](https://www.python.org/dev/peps/pep-0571/), e.g. manylinux2010 support.

## 2.0rc1

Released Nov. 18, 2018

### User-facing changes

- [FEATURE] manylinux2010 policy support
  ([#92](https://github.com/pypa/auditwheel/pull/92),
  [#130](https://github.com/pypa/auditwheel/pull/130))
    - Closes the auditwheel portion of "manylinux2010 rollout" ([pypa/manylinux#179](https://github.com/pypa/manylinux/issues/179))
- [FEATURE] Drop Python 3.4 support and add Python 3.7 support
  ([#127](https://github.com/pypa/auditwheel/pull/127))

### Housekeeping

- Replace print statements with logger.
  ([#113](https://github.com/pypa/auditwheel/pull/113))
    - Closes [#109](https://github.com/pypa/auditwheel/issues/109)
- Many small code cleanup PRs:
    - Update Python versions in README and setup.cfg ([#123](https://github.com/pypa/auditwheel/pull/123))
    - Remove unneeded parentheses ([#122](https://github.com/pypa/auditwheel/pull/122))
    - Use a Pythonic context manager ([#118](https://github.com/pypa/auditwheel/pull/118))
    - Remove unused variables and imports ([#121](https://github.com/pypa/auditwheel/pull/121), [#117](https://github.com/pypa/auditwheel/pull/117))
    - Use Python 3 class syntax ([#119](https://github.com/pypa/auditwheel/pull/119))
    - Fix log.warn deprecation warning ([#120](https://github.com/pypa/auditwheel/pull/120))
- Fix Travis flakiness by disabling caches and remove broken auto-deployments
  ([#128](https://github.com/pypa/auditwheel/pull/128))

## 1.10

Released Nov. 17, 2018

- After three weeks of testing, no bugs were reported in 1.10rc1.

## 1.10rc1

Released Oct. 27, 2018

### User-facing changes

- [BUGFIX] Pin wheel to 0.31.1 to avoid the API break in the 0.32.0 release
  ([#106](https://github.com/pypa/auditwheel/pull/106))
   - Temporary fix for "auditwheel does not work with wheel>=0.32.0" ([#102](https://github.com/pypa/auditwheel/issues/102))
- [BUGFIX] Properly support non-extension wheels that contain binary dependencies ([#110](https://github.com/pypa/auditwheel/pull/110))
   - Fixes "Regression in tests from merging [#95](https://github.com/pypa/auditwheel/pull/95)" ("show" after "repair" no longer identifies the platform correctly) ([#107](https://github.com/pypa/auditwheel/issues/107))
   - Closes "Audit for binary files inside pure wheels" ([#32](https://github.com/pypa/auditwheel/issues/32))
   - Closes "Ensure that pure wheels are supported by 'repair'" ([#47](https://github.com/pypa/auditwheel/issues/47))
- [FEATURE] Support more platforms and Python implementations
  ([#98](https://github.com/pypa/auditwheel/pull/98))

### Housekeeping

- Add PyPI badge to the README
  ([#97](https://github.com/pypa/auditwheel/pull/97))
- Fix CD, hopefully ([#99](https://github.com/pypa/auditwheel/pull/99))
- Ensure Travis fails when the tests fail
  ([#106](https://github.com/pypa/auditwheel/pull/106))
- Remove the dot from `py.test` -> `pytest`
  ([#112](https://github.com/pypa/auditwheel/pull/112))

## 1.9

Released Jul. 3, 2018

### User-facing changes

- [BUGFIX] Skip pure wheels that don't need a platform added
  ([#71](https://github.com/pypa/auditwheel/pull/71))
    - Fixes "auditwheel repair should not fail on pure Python wheels" ([#47](https://github.com/pypa/auditwheel/issues/47))
- [FEATURE] Process non-Python binary executables (#95)
- [FEATURE] Add support for compiled cffi pypy extensions
  ([#94](https://github.com/pypa/auditwheel/pull/94))
    - Fixes "Undefined name 'src_name' in auditwheel/repair.py" ([#91](https://github.com/pypa/auditwheel/issues/91))
    - Closes "Support repairing cffi PyPy extensions" ([#93](https://github.com/pypa/auditwheel/issues/93))

### Housekeeping

- Remove unused `-f`/`--force` option for `main_repair.py`
  ([#96](https://github.com/pypa/auditwheel/pull/96))

## 1.8

Released Dec. 28, 2017

### User-facing changes

- [BUGFIX] Fix recursive `get_req_external`
  ([#84](https://github.com/pypa/auditwheel/pull/84))
- [BUGFIX] Add libresolv to the whitelisted libraries
  ([#81](https://github.com/pypa/auditwheel/pull/81))
    - Fixes "Whitelist libresolv" ([#80](https://github.com/pypa/auditwheel/issues/80))

### Housekeeping

- Typo fix in `auditwheel show`
  ([#83](https://github.com/pypa/auditwheel/pull/83))
- Make failing Travis wheelhouse test optional
  ([#87](https://github.com/pypa/auditwheel/pull/87))

## 1.7

Released May 26, 2017

### User-facing changes

- [BUGFIX] Fix symbol version checks for symbols that do not follow the format
  "NAME_X.X.X" ([#73](https://github.com/pypa/auditwheel/pull/73))
    - Fixes "ValueError in versioned symbols" ([#72](https://github.com/pypa/auditwheel/issues/72))

### Housekeeping

- Code simplication ([#74](https://github.com/pypa/auditwheel/pull/74))

## 1.6.1

Released May 2, 2017

## 1.6

Released May 24, 2017

- Bad release. Accidentally a duplicate of 1.4. See [#68
  (comment)](https://github.com/pypa/auditwheel/issues/68#issuecomment-298735698)

## 1.5

Released Oct. 23, 2016

## 1.4

Released May 25, 2016

## 1.3

Released Apr. 3, 2016

## 1.2

Released Mar. 23, 2016

## 1.1

Released Jan. 30, 2016

## 1.0

Released Jan. 20, 2016
