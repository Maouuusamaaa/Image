# Changelog

## 2026-10-13 — Natural stance and gait pass

- Added a cyclical gait phase to the rig with alternating foot swing and subtle foot lift while walking.
- Added arm counter-swing, subtle idle breathing/settling, and a wider neutral stance.
- Changed the default relaxed arm targets so hands hang closer to the waist instead of extending straight sideways.
- Connected approach/retreat movement to the gait envelope in the scene timeline.
- Added tests for gait variation and relaxed idle posture while retaining contact timing and limb-length checks.
- Still requires visual review of the newly rendered video/contact sheet; code-level tests cannot prove that the silhouette looks natural or that stance feet are perfectly world-locked.
