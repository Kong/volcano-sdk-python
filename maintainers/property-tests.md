# Property tests

Hypothesis runs 200 generated examples per property and shrinks failures. The
seed for the run is saved in `reports/hypothesis/seed.txt`. Replay the same
inputs with the pinned Hypothesis version:

```sh
VOLCANO_PROPERTY_SEED=12345 uv run pytest tests/unit/test_encoding_properties.py
```

The quality command writes `reports/unit.xml`, including Hypothesis's minimized
counterexamples and reproduction instructions. CI preserves that report and the
seed on failure. Add a discovered counterexample as an explicit regression
example when fixing the bug.
