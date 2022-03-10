## AIP folders description

This folder structure follows the convention of the [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science/). It is described as follows:

├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.

Data is also inmutable, and thus no need to track it. Thus, data folder is in .gitignore file.
