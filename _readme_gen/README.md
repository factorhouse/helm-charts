# Helm Chart README Generator

This directory contains the source code and automation script for generating the `README.md` files for our various Helm charts. The purpose of this tool is to solve the problem of keeping multiple, similar `README.md` files in sync.

## How It Works

The system is based on two key concepts: **Partials** and **Templates**.

- **Partials (`_partials/`):** These are small, reusable Markdown files that contain a single, specific piece of documentation, like installation instructions or prerequisites.
- **Templates (`templates/`):** These are the master "blueprint" files for each final `README.md`. They define the structure of the document and use a special directive, `@@include(...)`, to pull in the content from the partials.

The `generate.py` script reads a template, finds all the `@@include` directives, replaces them with the content from the corresponding partial files, and writes the final, assembled `README.md` to the correct chart directory.

### Directory Structure

The project is organized by product to keep the source files separate and clean.

```
_readme_gen/
├── README.md               # This file
├── generate.py             # The master Python script
│
├── flex/                   # Source files for the "flex" product
│   ├── _partials/          # Reusable Markdown snippets for flex
│   │   └── _... .md
│   └── templates/          # Master templates for each flex README
│       └── flex.template.md
│
└── kpow/                   # Source files for the "kpow" product
    ├── _partials/          # Reusable Markdown snippets for kpow
    │   └── _... .md
    └── templates/          # Master templates for each kpow README
        └── kpow.template.md
```

---

## Usage

The script can be run from the command line to generate READMEs for a specific product or for all products at once.

### Generating READMEs for a Specific Product

Provide the product name (`kpow`, `flex`, etc.) as an argument to the script. This is useful for local development when you are only working on one product.

**Syntax:**

```bash
python generate.py <product_name>
```

**Examples:**

```bash
# Generate all READMEs for Kpow
python generate.py kpow

# Generate all READMEs for Flex
python generate.py flex
```

### Generating All READMEs

Running the script without any arguments will default to generating the READMEs for **all** products defined in the configuration. This is the mode used by our CI/CD automation.

**Examples:**

```bash
# Generate all READMEs for all products
python generate.py
```

Or explicitly:

```bash
python generate.py all
```

### Getting Help

To see the list of available products and options, use the `--help` flag.

```bash
python generate.py --help
```

---

## Adding a New Product

To add a new product (e.g., "platform") to the generator, follow these steps:

1.  **Create the Directory Structure:**
    Create a new folder inside `_readme_gen/` with the product's name, and add `_partials` and `templates` subdirectories.

    ```
    _readme_gen/
    └── platform/
        ├── _partials/
        └── templates/
    ```

2.  **Add Content:**
    Create your reusable `.md` files in `_partials/` and your master `platform.template.md` files in `templates/`.

3.  **Update the Configuration:**
    Open `generate.py` and add a new top-level entry for `"platform"` inside the `README_CONFIG` dictionary. Follow the existing structure to define the template and output paths for each of your new chart's READMEs.

    **Example addition to `README_CONFIG`:**

    ```python
    "gizmo": [
        {
            "template": BASE_DIR / "platform" / "templates/platform.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/gizmo/README.md",
        },
        # ... more chart variations for platform
    ],
    ```
