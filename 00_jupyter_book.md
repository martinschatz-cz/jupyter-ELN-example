# Jupyter Book Workflow: From Initialization to Build

This guide assumes you have your `environment.yml` file ready and your existing notebooks in a folder.

---

## Environment setup

Create and activate the dedicated conda environment from `environment.yml`.

```bash
# Create the environment from your yaml file
conda env create -f environment.yml

# Activate it
conda activate jp_eln_env
```

## Project initialization (Cookiecutter)

Use the official cookiecutter template to scaffold a Jupyter Book project, or create the book directory manually.

```bash
# Install cookiecutter if needed
pip install cookiecutter

# Run the Jupyter Book cookiecutter template
cookiecutter https://github.com/executablebooks/cookiecutter-jupyter-book
```

During the cookiecutter run you will be prompted for a book title and repository name. After the template is created, move your existing notebooks (for example the files under `Jupyter Notebook/`) into the new book folder (typically `book/` or `my-book/`).

## Configuration & table of contents

Jupyter Book uses two main YAML files to control site structure and options: `_toc.yml` and `_config.yml`.

### A. Define the structure (`_toc.yml`)

Example `_toc.yml` snippet:

```yaml
format: jb-book
root: intro
chapters:
  - file: 01-JN_and_JSON
  - file: 02-Extracting_metadata
  - file: 03_JN_as_ELN
  - part: Examples
    chapters:
      - file: Example/ELN_Penguin_Experiment_Template
      - file: Example/ELN_results
```

Place notebook filenames (without the `.ipynb` suffix) or markdown pages relative to the book root.

### B. Set build options (`_config.yml`)

Example `_config.yml` with execution settings:

```yaml
title: "My Jupyter Electronic Lab Notebook"
author: "Your Name"
execute:
  execute_notebooks: auto
  timeout: 120
```

Adjust execution, theme, and plugin options as needed (for example, add `sphinx-book-theme` or `myst-parser` related settings if used).

## Building the book

From the book root directory run:

```bash
# Build the HTML site
jupyter-book build .
```

After a successful build the static site will be in `_build/html/`.

## View the site

Open `_build/html/index.html` in a browser to preview the built book.

```text
# Example local path
__build/html/index.html
```

## Notes and next steps

- If your notebooks use interactive widgets, ensure `ipywidgets` is supported in your build environment and consider disabling execution in CI if it requires UI interaction.
- Add `_config.yml`/`_toc.yml` to the repository root of the book directory and create a simple GitHub Actions workflow to build and deploy the book if desired.
- Validate rendered pages locally and adjust `_toc.yml` ordering to improve navigation.