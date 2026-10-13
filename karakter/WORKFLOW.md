# Stickman Animation Asset Workflow

This folder is the persistent home for character references and animation-design artifacts.

## Rules for every iteration

1. Save every newly created asset, storyboard, reference sheet, animation source, render, test, and report in this repository as soon as it is created.
2. Put each category in a clear folder rather than scattering files across the repository.
3. Keep the original uploaded character reference unchanged. The intended normalized name is `karakter_0.jpeg`; only rename the existing file when the Git operation can preserve its original bytes.
4. Record each iteration in `CHANGELOG.md` with the date, files added/changed, purpose, and validation status.
5. Never claim a render, test, or commit succeeded unless it was actually run and verified.
6. Before adapting the character into animation code, locate and inspect the actual animation source repository. Do not place animation code in an unrelated repository just because it is accessible.

## Suggested structure

- `karakter/` — original and derived character references
- `storyboards/` — pose sheets and movement concepts
- `animation/` — animation source or interchange files, once the correct code repository is identified
- `renders/` — rendered previews and final videos
- `tests/` — motion/contact/pose validation artifacts
- `reports/` — comparison notes and quality reports

Large render files may be stored with Git LFS or as GitHub release artifacts if repository limits make normal Git storage unsuitable. Keep a small manifest in the repository pointing to every externally stored artifact.
