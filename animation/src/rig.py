"""Fixed-length 2D stickman rig with two-bone inverse kinematics."""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Tuple

Point = Tuple[float, float]

def distance(a: Point, b: Point) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])

def reachable_target(root: Point, target: Point, upper: float, lower: float) -> Point:
    """Clamp a requested joint target to the rig's physically reachable annulus."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    raw = math.hypot(dx, dy)
    if raw < 1e-8:
        return (root[0] + upper + lower - 1e-5, root[1])
    d = min(max(raw, abs(upper - lower) + 1e-5), upper + lower - 1e-5)
    return (root[0] + dx / raw * d, root[1] + dy / raw * d)

def solve_two_bone(root: Point, target: Point, upper: float, lower: float, bend: int = 1) -> Point:
    """Return elbow/knee position while preserving both segment lengths."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    raw = math.hypot(dx, dy)
    if raw < 1e-8:
        dx, dy, raw = 1.0, 0.0, 1.0
    d = min(max(raw, abs(upper - lower) + 1e-5), upper + lower - 1e-5)
    ux, uy = dx / raw, dy / raw
    along = (upper * upper - lower * lower + d * d) / (2 * d)
    height = math.sqrt(max(0.0, upper * upper - along * along))
    bx, by = root[0] + ux * along, root[1] + uy * along
    sign = 1 if bend >= 0 else -1
    return (bx - uy * height * sign, by + ux * height * sign)

@dataclass(frozen=True)
class Rig:
    head_radius: float = 15.0
    torso: float = 49.0
    upper_arm: float = 27.0
    forearm: float = 26.0
    thigh: float = 32.0
    shin: float = 31.0

@dataclass
class Pose:
    x: float
    ground: float
    lean: float = 0.0
    crouch: float = 0.0
    head_turn: float = 0.0
    left_hand: Point | None = None
    right_hand: Point | None = None
    left_foot: Point | None = None
    right_foot: Point | None = None

class StickmanRig:
    def __init__(self, proportions: Rig | None = None):
        self.rig = proportions or Rig()

    def joints(self, pose: Pose) -> dict[str, Point]:
        r = self.rig
        hip = (pose.x + pose.lean * 0.25, pose.ground - 62 + pose.crouch * 12)
        shoulder = (hip[0] + pose.lean, hip[1] - r.torso)
        head = (shoulder[0] + pose.head_turn * 5, shoulder[1] - r.head_radius - 2)
        lf = pose.left_foot or (pose.x - 6, pose.ground)
        rf = pose.right_foot or (pose.x + 6, pose.ground)
        lf = reachable_target(hip, lf, r.thigh, r.shin)
        rf = reachable_target(hip, rf, r.thigh, r.shin)
        lk = solve_two_bone(hip, lf, r.thigh, r.shin, bend=-1)
        rk = solve_two_bone(hip, rf, r.thigh, r.shin, bend=1)
        lh = reachable_target(shoulder, pose.left_hand or (shoulder[0] - 20, shoulder[1] + 20), r.upper_arm, r.forearm)
        rh = reachable_target(shoulder, pose.right_hand or (shoulder[0] + 20, shoulder[1] + 20), r.upper_arm, r.forearm)
        le = solve_two_bone(shoulder, lh, r.upper_arm, r.forearm, bend=-1)
        re = solve_two_bone(shoulder, rh, r.upper_arm, r.forearm, bend=1)
        return {'hip': hip, 'shoulder': shoulder, 'head': head,
                'left_foot': lf, 'right_foot': rf, 'left_knee': lk, 'right_knee': rk,
                'left_hand': lh, 'right_hand': rh, 'left_elbow': le, 'right_elbow': re}
