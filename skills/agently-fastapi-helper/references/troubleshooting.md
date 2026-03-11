# Troubleshooting

- The helper rejects the payload:
  Check that the body has both `data` and `options`.
- The main question is now about business orchestration, not HTTP exposure:
  Switch to the appropriate TriggerFlow skill.
- The provider setup is failing before FastAPI matters:
  Switch to `agently-model-setup`.
- The service needs a broader architecture than helper wiring:
  Treat this as a playbook-level problem rather than a helper problem.
