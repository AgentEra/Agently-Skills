# Troubleshooting

- Parent state changes are not visible in the child:
  Check `capture`. Only captured data crosses into the child.
- Child result did not update the parent as expected:
  Check `write_back`. Child changes do not automatically mutate parent state.
- Child flow unexpectedly reused old state:
  Re-check which data came from the child template, which data was captured, and which data was written back.
- Runtime stream only shows parent events:
  Make sure the child actually emits stream events and consume the parent execution stream.
- Child flow pauses and the parent fails:
  This is a current boundary. Sub flows do not support child pause/resume or external re-entry.
