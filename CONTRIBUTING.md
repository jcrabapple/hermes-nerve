# Contributing

The project is contract-first. New integrations should usually add or reuse a bounded decision contract rather than embedding ad-hoc prompts in hooks.

For a new contract/recipe, include:

1. explicit allowed outputs
2. criteria for every output
3. deterministic policy around confidence/failure
4. privacy classification of state fields
5. fixtures covering ambiguous and adversarial cases
6. benchmark/eval methodology if making quality claims
