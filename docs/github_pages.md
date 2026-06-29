# GitHub Pages Demo

The repository includes a static dashboard that can be published as the public project demo link for Kaggle.

The dashboard is generated as a project-detail evidence view: it shows the Freestyle track, current audit verdict, benchmark match rate, agent roles, generated artifacts, audit findings, and tool trace in one responsive page.

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

The workflow asks `actions/configure-pages` to enable Pages automatically with the GitHub Actions source. If repository settings or organization policy block automatic enablement, configure it manually in GitHub:

1. Open repository settings.
2. Go to **Pages**.
3. Set **Build and deployment** source to **GitHub Actions**.
4. Push to `main` or run the workflow manually.

Expected public URL:

```text
https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/
```

Use that URL as the Kaggle project link once the workflow has completed successfully.
