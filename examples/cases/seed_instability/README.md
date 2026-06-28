# Seed Instability

This case uses randomness without setting a seed.

Expected behavior:

- the script runs;
- repeated runs may report different accuracy values;
- static analysis should flag missing seed control;
- the final verdict should be `partially_reproduced`.

