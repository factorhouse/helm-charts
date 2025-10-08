import re
import argparse
from pathlib import Path

# --- Configurations ---
BASE_DIR = Path(__file__).resolve().parent
CHART_FOLDER = "charts"
README_CONFIG = {
    "kpow": [
        {
            "template": BASE_DIR / "kpow" / "templates/kpow.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/kpow/README.md",
        },
        {
            "template": BASE_DIR / "kpow" / "templates/kpow-ce.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/kpow-ce/README.md",
        },
        {
            "template": BASE_DIR / "kpow" / "templates/kpow-aws-annual.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/kpow-aws-annual/README.md",
        },
        {
            "template": BASE_DIR / "kpow" / "templates/kpow-aws-hourly.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/kpow-aws-hourly/README.md",
        },
    ],
    "flex": [
        {
            "template": BASE_DIR / "flex" / "templates/flex.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/flex/README.md",
        },
        {
            "template": BASE_DIR / "flex" / "templates/flex-ce.template.md",
            "output": BASE_DIR / f"../{CHART_FOLDER}/flex-ce/README.md",
        },
        # {
        #     "template": BASE_DIR / "flex" / "templates/flex-aws-annual.template.md",
        #     "output": BASE_DIR / f"../{CHART_FOLDER}/flex-aws-annual/README.md",
        # },
        # {
        #     "template": BASE_DIR / "flex" / "templates/flex-aws-hourly.template.md",
        #     "output": BASE_DIR / f"../{CHART_FOLDER}/flex-aws-hourly/README.md",
        # },
    ],
}


def generate_readmes(product_to_generate):
    """
    Generates README files for a specific product or for all products.
    """
    print(f"Starting README generation for: {product_to_generate.upper()}")
    include_pattern = re.compile(r"@@include\(([^)]+)\)")

    if product_to_generate == "all":
        products_to_process = README_CONFIG.keys()
    else:
        products_to_process = [product_to_generate]

    for product_name in products_to_process:
        configs_list = README_CONFIG.get(product_name)
        if not configs_list:
            print(
                f"  ⚠️ WARNING: No configuration found for product '{product_name}'. Skipping."
            )
            continue

        print(f"\n--- Processing product: {product_name.upper()} ---")

        for config in configs_list:
            template_path = config["template"]
            output_path = config["output"]

            try:
                if not template_path.exists():
                    print(
                        f"  ❌ ERROR: Template file not found at {template_path}. Skipping."
                    )
                    continue

                print(f"Processing {template_path.name}...")

                template_content = template_path.read_text(encoding="utf-8")

                def replacer(match):
                    """
                    Replaces an @@include directive with the content of the partial file.
                    This function now cleans the captured path before using it.
                    """
                    raw_partial_path = match.group(1)
                    cleaned_partial_path = raw_partial_path.strip()
                    if (
                        cleaned_partial_path.startswith('"')
                        and cleaned_partial_path.endswith('"')
                    ) or (
                        cleaned_partial_path.startswith("'")
                        and cleaned_partial_path.endswith("'")
                    ):
                        cleaned_partial_path = cleaned_partial_path[1:-1]

                    cleaned_partial_path = cleaned_partial_path.replace("\\", "")
                    partial_path = BASE_DIR / product_name / cleaned_partial_path

                    if not partial_path.exists():
                        error_msg = f"<!-- ERROR: Partial file not found at: {cleaned_partial_path} -->"
                        print(f"  ❌ ERROR: Partial not found at {partial_path}")
                        return error_msg

                    return partial_path.read_text(encoding="utf-8")

                final_content = include_pattern.sub(replacer, template_content)

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(final_content, encoding="utf-8")
                print(f"  ✅ Successfully generated {output_path}")

            except Exception as e:
                print(f"  ❌ FAILED to process {template_path.name}: {e}")

    print("\nREADME generation finished.")


if __name__ == "__main__":
    # --- Command-Line Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="Generate README files for Helm charts from templates and partials."
    )

    # The list of valid choices is dynamically created from the keys in your config dictionary.
    valid_products = list(README_CONFIG.keys()) + ["all"]

    parser.add_argument(
        "product",
        nargs="?",
        default="all",
        choices=valid_products,
        help="Specify which product's READMEs to generate. Defaults to 'all'.",
    )

    args = parser.parse_args()

    generate_readmes(args.product)
