# Reference-first animation workflow

## Target motion
A relaxed, ordinary walk cycle with both hands resting behind the head and elbows pointing outward.

## Source of truth
- `walk-hands-behind-head.svg` is the repository-native, editable key-pose reference sheet.
- The generated raster concept sheet is a visual planning aid; the SVG is the committed reference asset because it can be stored and reviewed as text in Git.

## Frame production procedure
1. Treat the eight poses in the SVG as keyframes, not as eight isolated finished frames.
2. Define one rig pose per keyframe: root position, torso lean, head angle, shoulder/elbow/wrist positions, hip position, and both feet.
3. Interpolate between adjacent keyframes using smooth curves; preserve planted-foot intervals to prevent sliding.
4. Keep both hands behind the head throughout the loop. Elbows should stay out to the sides and move only subtly with torso bob.
5. Add a small, consistent vertical body bob and slight hip/shoulder counter-rotation. Avoid large head movement.
6. Render all frames, then inspect a contact sheet and the MP4. Check for limb popping, feet sliding, changing limb lengths, abrupt timing, and a visible jump at the loop seam.
7. Do not call the animation finished based on passing unit tests alone; visual review is required.

## Acceptance checks
- First and last poses match closely enough to loop cleanly.
- Left and right steps alternate.
- The lifted foot clears the ground and the stance foot stays planted during its support interval.
- Hands remain behind the head in every frame.
- Head, torso, elbows, knees, and feet remain connected with stable proportions.
- Motion is continuous when played, not merely plausible in individual still frames.
