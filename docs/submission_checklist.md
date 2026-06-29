# Submission Checklist

Use this checklist before submitting the Kaggle Writeup.

## Required Assets

- Kaggle Writeup under 2,500 words.
- Final writeup draft: `docs/kaggle_writeup_final.md`.
- Final video script: `docs/video_script_final.md`.
- Cover image: `docs/assets/reprobench-cover.png`.
- Cover source: `docs/assets/reprobench-cover.svg`.
- Submission bundle: `docs/submission_bundle.md`.
- Cover image uploaded to the Kaggle media gallery.
- YouTube video under 5 minutes.
- Public GitHub repository.
- Public project/demo link or reproducible setup instructions.

## Repository Checks

```bash
make test
make audit-cases
make benchmark-report
make sample-report
make dashboard
make pages
make mcp-demo
make demo
make compile
make ci
```

Expected results:

- tests pass;
- benchmark verdicts match `5/5`;
- `reports/sample/benchmark/benchmark_summary.md` is generated;
- `reports/sample/data_leakage/report.md` is generated;
- `reports/sample/dashboard/index.html` is generated;
- `docs/index.html` is generated for GitHub Pages;
- MCP `audit_case` demo returns `partially_reproduced` for `data_leakage`.
- GitHub Actions CI passes on Python 3.11 and Python 3.12.

## Writeup Evidence To Link

- [Benchmark summary](../reports/sample/benchmark/benchmark_summary.md)
- [Data leakage evidence report](../reports/sample/data_leakage/report.md)
- [Static demo dashboard](../reports/sample/dashboard/index.html)
- [GitHub Pages dashboard](index.html)
- [Architecture](architecture.md)
- [MCP server](mcp_server.md)
- [Security model](security.md)
- [Final Kaggle writeup draft](kaggle_writeup_final.md)
- [Final video script](video_script_final.md)
- [Submission bundle](submission_bundle.md)
- [Cover image](assets/reprobench-cover.png)
- [Cover source](assets/reprobench-cover.svg)

## Video Demo Flow

1. Show the problem: ML claims are often hard to verify.
2. Run `make audit-cases`.
3. Run `make mcp-demo`.
4. Open `reports/sample/data_leakage/report.md`.
5. Point out `validate_path_policy`, `scan_for_secrets`, `detect_data_leakage`, `run_python_script`, and `compare_metric`.
6. Close with the benchmark summary: `5/5` expected verdicts matched.

## Final QA

- No API keys or passwords in the repository.
- `.env.example` contains placeholders only.
- README quickstart works from a clean checkout.
- `make ci` passes locally.
- CI workflow is green on GitHub.
- GitHub repository is public.
- YouTube video is public or unlisted but accessible.
- Kaggle Writeup has the Freestyle track selected.
