# Demonstration of autoware_universe splitting workflow

This repository is a mirror of `planning/` in https://github.com/autowarefoundation/autoware_universe and CI demonstration.
See `mirror` branch for mirrored result.

## Key recipe

The [mirror-upstream workflow](.github/workflows/mirror-upstream.yaml) extracts only histories related to `planning/` (and few other directories) and created

The history exactraction using `git filter-repo` is deterministic, which means the same SHA from the upstream autoware_universe is always the same SHA. Below is the simplified version of the workflow:

```bash
$ git clone git@github.com:autowarefoundation/autoware_universe.git .
$ git filter-repo --path planning/ --path .github/ --path docs/ --path-regex '^[^/]*$' --force
$ git push # successful non-force push proves that the extracted history is deterministic
```

Start with an empty repository and add the workflow, replacing `planning/` with your target directory such as `perception/` or `map/`. It will extract the corresponding directory history and mirrors the universe upstream.
