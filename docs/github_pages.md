# GitHub Pages Demo

The repository includes a static dashboard that can be published as the public project demo link for Kaggle.

## Local Generation

```bash
make benchmark-report
make sample-report
make pages
```

This writes:

```text
docs/index.html
```

The page is generated from:

- `reports/sample/benchmark/benchmark_summary.json`
- `reports/sample/data_leakage/report.json`

## GitHub Pages Deployment

The workflow `.github/workflows/pages.yml` deploys the `docs/` directory to GitHub Pages on pushes to `main`.

In GitHub:

1. Open repository settings.
2. Go to **Pages**.
3. Set **Build and deployment** source to **GitHub Actions**.
4. Push to `main` or run the workflow manually.

Expected public URL:

```text
https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/
```

Use that URL as the Kaggle project link once the workflow has completed successfully.

