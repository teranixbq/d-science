# D-Science Theme for Hugo

A vintage, ledger-style data science report theme for Hugo. Designed for analysts, quants, and tinkerers who appreciate clean, minimalist aesthetics.

## Features
- **Vintage Data Viz:** Built-in shortcode for rendering Chart.js with retro styling.
- **Editorial Grid:** Clean layout inspired by academic reports and financial ledgers.
- **Trending Sidebar:** (Optional) Show daily trending models from HuggingFace and Kaggle datasets.
- **Giscus Comments:** Built-in integration with GitHub Discussions for comments.

## Installation

Inside the folder of your Hugo site run:

```bash
git submodule add https://github.com/teranixbq/d-science.git themes/d-science
```

Then, add the theme to your `hugo.toml`:

```toml
theme = "d-science"
```

## Configuration

For a complete reference on how to configure this theme, please check the `hugo.toml` provided inside the `exampleSite/` folder.

### Enabling the Trending Sidebar
The theme includes a layout for displaying trending HuggingFace models and Kaggle datasets. The data for this is stored in `data/huggingface.json` and `data/kaggle.json`.

If you want to automate the fetching of this data, we provide example Python scripts and a GitHub Actions workflow inside the `exampleSite/` folder:

1. Copy the `exampleSite/scripts/` folder to your project root.
2. Copy `exampleSite/.github/workflows/fetch_kaggle.yml` to your project root.

The workflow will run every midnight to update the JSON files. You can toggle the display of this sidebar in your `hugo.toml`:

```toml
[params.sidebar]
    enable_trending = true
```

## License
MIT
