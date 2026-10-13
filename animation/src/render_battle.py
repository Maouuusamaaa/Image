#!/usr/bin/env python3
"""Deterministic white-stage stickman battle renderer with contact-driven impacts."""
from __future__ import annotations
import argparse, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
try:
    from .rig import StickmanRig, Pose
except ImportError:
    from rig import StickmanRig, Pose

WIDTH, HEIGHT, FPS, DURATION = 960, 540, 30, 12
GROUND = 438
INK, WHITE = (20, 20, 20), (255, 255, 255)

# Hand-authored contact events: preparation -> contact -> follow-through/recovery.
ATTACKS = [
    {'start': 2.00, 'contact': 2.30, 'end': 2.72, 'attacker': 0, 'hand': 'right', 'target': 'head'},
    {'start': 4.05, 'contact': 4.34, 'end': 4.82, 'attacker': 1, 'hand': 'left', 'target': 'torso'},
    {'start': 6.30, 'contact': 6.58, 'end': 7.10, 'attacker': 0, 'hand': 'right', 'target': 'torso'},
    {'start': 8.55, 'contact': 8.86, 'end': 9.42, 'attacker': 1, 'hand': 'left', 'target': 'head'},
]

def clamp(x, lo=0.0, hi=1.0): return max(lo, min(hi, x))
def smooth(x):
    x = clamp(x); return x*x*(3-2*x)
def lerp(a, b, t): return a + (b-a)*t

def attack_weight(t, attack):
    """Drive the fist to contact, hold briefly, then retract smoothly.

    The short contact hold keeps the hit readable instead of making the fist
    reverse direction on the exact frame the impact reaction begins.
    """
    if t < attack['start'] or t > attack['end']: return 0.0
    if t <= attack['contact']:
        return smooth((t-attack['start'])/(attack['contact']-attack['start']))
    contact_hold = 0.07
    recovery_start = attack['contact'] + contact_hold
    if t <= recovery_start: return 1.0
    return 1.0 - smooth((t-recovery_start)/(attack['end']-recovery_start))

def scene_state(t):
    approach = smooth((t-0.4)/1.4)
    retreat = smooth((t-9.5)/1.2)
    left_x = lerp(270, 457, approach)
    right_x = lerp(690, 503, approach)
    left_x = lerp(left_x, 320, retreat); right_x = lerp(right_x, 640, retreat)
    # Walk cycles are active only while the characters are translating.
    approach_walk = smooth((t-0.42)/0.22) * (1.0-smooth((t-1.72)/0.24))
    retreat_walk = smooth((t-9.52)/0.22) * (1.0-smooth((t-10.92)/0.25))
    walk = clamp(max(approach_walk, retreat_walk))
    poses = [
        Pose(left_x, GROUND, gait_phase=t*2.0*math.pi*1.65,
             gait_weight=walk, idle_phase=t*2.0*math.pi*0.62, stance=13.0),
        Pose(right_x, GROUND, gait_phase=t*2.0*math.pi*1.65+math.pi,
             gait_weight=walk, idle_phase=t*2.0*math.pi*0.62+1.1, stance=13.0)
    ]
    active = []
    for attack in ATTACKS:
        w = attack_weight(t, attack)
        if w <= 0: continue
        active.append((attack, w))
        a = attack['attacker']; target = 1-a
        direction = 1 if a == 0 else -1
        target_point = (poses[target].x, GROUND-132 if attack['target'] == 'head' else GROUND-82)
        shoulder = (poses[a].x, GROUND-111)
        start_hand = (shoulder[0] + direction*19, shoulder[1]+35)
        hand = (lerp(start_hand[0], target_point[0]-direction*3, w),
                lerp(start_hand[1], target_point[1], w))
        if attack['hand'] == 'right': poses[a].right_hand = hand
        else: poses[a].left_hand = hand
        # Reaction begins at the event's contact time, never during the wind-up.
        if t >= attack['contact']:
            recoil = smooth((t-attack['contact'])/0.16) * (1.0-smooth((t-attack['contact']-0.24)/0.45))
            poses[target].lean += -direction * 17 * recoil
            poses[target].crouch += 0.25 * recoil
    # Do not overwrite gait-generated foot targets: stance feet stay on the floor,
    # while swing feet lift modestly during the walk cycle.
    return poses, active

def draw_limb(draw, points, width=5):
    draw.line([(round(x), round(y)) for x, y in points], fill=INK, width=width, joint='curve')

def draw_character(draw, rig, pose):
    j = rig.joints(pose)
    draw_limb(draw, [j['hip'], j['left_knee'], j['left_foot']], 5)
    draw_limb(draw, [j['hip'], j['right_knee'], j['right_foot']], 5)
    draw_limb(draw, [j['hip'], j['shoulder']], 6)
    draw_limb(draw, [j['shoulder'], j['left_elbow'], j['left_hand']], 5)
    draw_limb(draw, [j['shoulder'], j['right_elbow'], j['right_hand']], 5)
    hx, hy = j['head']; rr = rig.rig.head_radius
    draw.ellipse((hx-rr, hy-rr, hx+rr, hy+rr), outline=INK, width=5)
    for key in ('left_hand', 'right_hand'):
        x, y = j[key]
        draw.ellipse((x-4, y-4, x+4, y+4), fill=INK)

def render_frame(index, width=WIDTH, height=HEIGHT):
    t = index / FPS
    image = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)
    draw.line((0, GROUND+2, WIDTH, GROUND+2), fill=(90,90,90), width=2)
    poses, active = scene_state(t)
    rig = StickmanRig()
    for pose in poses: draw_character(draw, rig, pose)
    # A hit marker exists only after a scheduled contact event.
    for attack, weight in active:
        if attack['contact'] <= t <= attack['contact'] + 0.18:
            target = poses[1-attack['attacker']]
            cx = target.x
            cy = GROUND-132 if attack['target'] == 'head' else GROUND-82
            radius = 12 + 24*weight
            draw.arc((cx-radius,cy-radius,cx+radius,cy+radius), 205, 510, fill=INK, width=3)
            for angle in range(0,360,45):
                a = math.radians(angle)
                draw.line((cx+math.cos(a)*radius,cy+math.sin(a)*radius,
                           cx+math.cos(a)*(radius+9),cy+math.sin(a)*(radius+9)), fill=INK, width=2)
    if (width,height)!=(WIDTH,HEIGHT): image = image.resize((width,height), Image.Resampling.LANCZOS)
    return image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='output/stickman-battle-v1.mp4')
    parser.add_argument('--frames-dir', default='output/frames')
    parser.add_argument('--fps', type=int, default=FPS)
    parser.add_argument('--duration', type=float, default=DURATION)
    parser.add_argument('--limit-frames', type=int, default=0)
    parser.add_argument('--frames-only', action='store_true')
    args = parser.parse_args()
    if args.fps <= 0 or args.duration <= 0: parser.error('fps and duration must be positive')
    root = Path(__file__).resolve().parents[1]
    frame_dir = root / args.frames_dir; frame_dir.mkdir(parents=True, exist_ok=True)
    count = int(args.fps*args.duration)
    if args.limit_frames: count = min(count, args.limit_frames)
    for i in range(count):
        render_frame(round(i*FPS/args.fps)).save(frame_dir/f'frame_{i:06d}.png')
    if args.frames_only: return
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg: raise SystemExit('FFmpeg is required to encode MP4; PNG frames were generated.')
    output = root/args.output; output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([ffmpeg,'-y','-framerate',str(args.fps),'-i',str(frame_dir/'frame_%06d.png'),
                    '-frames:v',str(count),'-c:v','libx264','-pix_fmt','yuv420p',
                    '-movflags','+faststart',str(output)], check=True)
    print(f'Wrote {count} frames to {output}')

if __name__ == '__main__': main()
