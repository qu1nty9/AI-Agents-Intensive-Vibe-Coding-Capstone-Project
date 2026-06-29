# Kaggle Submission Bundle

This is the single handoff page for the final Kaggle submission.

## Project

- Title: **ReproBench Agent: Evidence-First Reproducibility Audits for ML Experiments**
- Track: **Freestyle**
- Tagline: ReproBench Agent turns ML claims into reproducible, auditable evidence.
- Repository: `https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project`
- Demo dashboard: `https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/`

## Submission Assets

- Final writeup draft: [kaggle_writeup_final.md](kaggle_writeup_final.md)
- Final video script: [video_script_final.md](video_script_final.md)
- Cover image: [assets/reprobench-cover.png](assets/reprobench-cover.png)
- Cover source: [assets/reprobench-cover.svg](assets/reprobench-cover.svg)
- Static dashboard source: [../reports/sample/dashboard/index.html](../reports/sample/dashboard/index.html)
- GitHub Pages dashboard source: [index.html](index.html)
- Benchmark summary: [../reports/sample/benchmark/benchmark_summary.md](../reports/sample/benchmark/benchmark_summary.md)
- Data leakage evidence report: [../reports/sample/data_leakage/report.md](../reports/sample/data_leakage/report.md)

## Proof Commands

Run these from the repository root:

```bash
make ci
make audit-cases
make sample-report
make dashboard
make mcp-demo
```

Expected proof points:

- `make ci` passes locally.
- Unit and integration tests pass.
- Benchmark verdicts match `5/5`.
- The data leakage case returns `partially_reproduced`.
- The MCP `audit_case` demo returns the same structured verdict and tool trace.

## Demo Narrative

The strongest live demo is the `data_leakage` case:

1. The experiment claims `accuracy = 1.0`.
2. ReproBench reproduces that metric exactly.
3. The leakage detector finds that `leaky_target_copy` exactly matches the target.
4. The final verdict becomes `partially_reproduced`, proving that the agent separates a reproduced number from trustworthy evidence.

## External Tasks Before Kaggle Submit

- Confirm GitHub Pages is enabled with the GitHub Actions source.
- Wait for the CI workflow to turn green after the final push.
- Record and upload the under-5-minute YouTube video.
- Add the YouTube URL to the Kaggle Writeup.
- Upload the cover image to the Kaggle media gallery.
- Select the Freestyle track before submitting.
