# Data Leakage

This is the strongest planned demo case.

Expected behavior:

- the script reports `accuracy = 1.0`;
- a naive metric check would accept the claim;
- leakage analysis should flag `leaky_target_copy`;
- the final verdict should be `partially_reproduced` because the metric reproduces but the evidence is not trustworthy.

