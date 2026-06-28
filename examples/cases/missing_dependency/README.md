# Missing Dependency

This case intentionally imports a package that does not exist.

Expected behavior:

- the script fails before reporting a metric;
- the error is classified as an environment/dependency issue;
- the final verdict should be `blocked`, not `not_reproduced`.

