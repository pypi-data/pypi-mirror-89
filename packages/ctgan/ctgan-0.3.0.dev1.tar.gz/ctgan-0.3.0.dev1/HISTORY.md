# History

## v0.2.2 - 2020-11-13

In this release we introduce several minor improvements to make CTGAN more versatile and
propertly support new types of data, such as categorical NaN values, as well as conditional
sampling and features to save and load models.

Additionally, the dependency ranges and python versions have been updated to support up
to date runtimes.

Many thanks @fealho @leix28 @csala @oregonpillow and @lurosenb for working on making this release possible!

### Improvements

* Drop Python 3.5 support - [Issue #79](https://github.com/sdv-dev/CTGAN/issues/79) by @fealho
* Support NaN values in categorical variables - [Issue #78](https://github.com/sdv-dev/CTGAN/issues/78) by @fealho
* Sample synthetic data conditioning on a discrete column - [Issue #69](https://github.com/sdv-dev/CTGAN/issues/69) by @leix28
* Support recent versions of pandas - [Issue #57](https://github.com/sdv-dev/CTGAN/issues/57) by @csala
* Easy solution for restoring original dtypes - [Issue #26](https://github.com/sdv-dev/CTGAN/issues/26) by @oregonpillow

### Bugs fixed

* Loss to nan - [Issue #73](https://github.com/sdv-dev/CTGAN/issues/73) by @fealho
* Swapped the sklearn utils testing import statement - [Issue #53](https://github.com/sdv-dev/CTGAN/issues/53) by @lurosenb

## v0.2.1 - 2020-01-27

Minor version including changes to ensure the logs are properly printed and
the option to disable the log transformation to the discrete column frequencies.

Special thanks to @kevinykuo for the contributions!

### Issues Resolved:

* Option to sample from true data frequency instead of logged frequency - [Issue #16](https://github.com/sdv-dev/CTGAN/issues/16) by @kevinykuo
* Flush stdout buffer for epoch updates - [Issue #14](https://github.com/sdv-dev/CTGAN/issues/14) by @kevinykuo

## v0.2.0 - 2019-12-18

Reorganization of the project structure with a new Python API, new Command Line Interface
and increased data format support.

### Issues Resolved:

* Reorganize the project structure - [Issue #10](https://github.com/sdv-dev/CTGAN/issues/10) by @csala
* Move epochs to the fit method - [Issue #5](https://github.com/sdv-dev/CTGAN/issues/5) by @csala

## v0.1.0 - 2019-11-07

First Release - NeurIPS 2019 Version.
