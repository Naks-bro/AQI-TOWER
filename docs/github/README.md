# Prototype CI template

`prototype-checks.yml` is a prepared workflow template, not an active GitHub Action. It checks local README targets and current standard-library D01 analysis tools on Linux.

The authenticated GitHub credentials used for this update have repository permission but lack the `workflow` scope, so GitHub rejected creating the file under `.github/workflows/`. The template is retained here without expanding account permissions.

To activate it, a maintainer with workflow write permission can copy it to `.github/workflows/prototype-checks.yml` and commit through the normal review process. No additional Python dependencies are needed. Tests remain arithmetic and abstract software checks; they do not certify the physical unit.
