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

## Project initialization (Jupyter Book v2)

Initialize a minimal Jupyter Book skeleton and add your content. For v2 the lightweight entrypoint is `init`.

```bash
# Initialize a new book (creates a minimal skeleton in `mybook`)
jupyter-book init mybook

# (alternate) some installations use 'create' instead
# jupyter-book create mybook
```

Place your notebooks and markdown pages in `mybook/` (common layouts: `mybook/content/` or `mybook/notebooks/`). Example structure:

```text
mybook/
  ├─ _config.yml
  ├─ _toc.yml
  ├─ content/
  │   ├─ index.md
  │   └─ 01-JN_and_JSON.ipynb
  └─ notebooks/  # optional
```

If you prefer the cookiecutter template you can still use it, but `init` is the recommended quick start for v2.

### MyST configuration (`myst.yml`)

Jupyter Book v2 commonly uses `myst.yml` at the book root to configure the MyST parser and site metadata. It can hold parser extension flags, project metadata, and even a canonical table-of-contents (though `_toc.yml` is still supported).

Below is an example `myst.yml` adapted from this repository (place at `mybook/myst.yml` or at the repo root if you prefer a single config):

```yaml
# See docs at: https://mystmd.org/guide/frontmatter
version: 1
project:
  id: 6c784919-2ea5-4705-9f76-c1e30cb1c89b
  title: Example ELN with Jupyter Notebook
  description: This repository contains an example of how to use Jupyter Notebook as an Electronic Lab Notebook (ELN).
  authors: [Martin Schätz]
  github: https://github.com/martinschatz-cz/jupyter-ELN-example
  license: MIT

# Optional: a canonical TOC you maintain in myst.yml instead of _toc.yml
toc:
  - file: README.md
  - file: 00_jupyter_book.md
  - title: Jupyter Notebook
    children:
      - file: Jupyter Notebook/01-JN_and_JSON.ipynb
      - file: Jupyter Notebook/02-Extracting_metadata.ipynb
      - file: Jupyter Notebook/03_JN_as_ELN.ipynb
  - title: ELN Example
    children:
      - file: Jupyter Notebook/Example/ELN_Adelie_Penguins.ipynb
      - file: Jupyter Notebook/Example/ELN_Chinstrap_Penguins.ipynb
      - file: Jupyter Notebook/Example/ELN_Gentoo_Penguins.ipynb
      - file: Jupyter Notebook/Example/ELN_results.ipynb

site:
  template: book-theme
  options:
    footer: |
      <p>Copyright © 2026 Martin Schätz. Licensed under <a href="https://opensource.org/licenses/MIT">MIT</a>.</p>

# MyST parser options
myst_enable_extensions:
  - deflist
  - html_admonition
  - html_image
  - linkify

myst_heading_anchors: 3
```

Notes:
- If `jupyter-book init` already created a `myst.yml`, edit it to enable extensions and add project metadata.
- You can put parser options either in `myst.yml` or under the `myst:` key inside `_config.yml`; `myst.yml` is the preferred standalone file for MyST frontmatter and site metadata in recent templates.
- If you maintain a `toc:` in `myst.yml`, avoid duplicating it in `_toc.yml` to prevent conflicting navigation.

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

## Building the book (HTML)

Build the site as HTML (default). From the repository root or the book folder run:

```bash
# start and show the content
jupyter-book start

# standard build (HTML is the default output)
jupyter-book build --html
```

After a successful build the static site will be in `mybook/_build/html/` (or `_build/html/` if run from inside the book folder).

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