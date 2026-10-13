#!/usr/bin/env python3
"""Reference-driven walk cycle: hands behind head, interpolated key poses."""
from __future__ import annotations
import argparse, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
try:
    from .rig import StickmanRig, Pose
except ImportError:
    from rig import StickmanRig, Pose

WIDTH, HEIGHT, FPS, DURATION, GROUND = 960, 540, 30, 4.0, 438
INK, WHITE = (20, 20, 20), (255, 255, 255)

# Eight authored key poses plus a duplicate start pose to close the loop.
# Each tuple is (cycle phase, normalized step direction, normalized foot lift).
KEYS = [
    (0.00, 0.00, 0.00), (0.125, 0.85, 0.65),
    (0.25, 1.00, 0.35), (0.375, 0.15, 0.00),
    (0.50, -1.00, 0.35), (0.625, -0.85, 0.65),
    (0.75, -0.15, 0.00), (0.875, 0.65, 0.35),
    (1.00, 0.00, 0.00),
]

def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def smooth(v):
    v = clamp(v)
    return v*v*(3.0-2.0*v)

def sample_key(phase):
    phase %= 1.0
    for i in range(len(KEYS)-1):
        p0, stride0, lift0 = KEYS[i]
        p1, stride1, lift1 = KEYS[i+1]
        if p0 <= phase <= p1:
            u = smooth((phase-p0)/(p1-p0))
            return stride0+(stride1-stride0)*u, lift0+(lift1-lift0)*u
    return 0.0, 0.0

def make_pose(t, fps=FPS):
    phase = (t % 1.0)
    stride, lift = sample_key(phase)
    gait_phase = phase * math.tau
    pose = Pose(
        x=WIDTH/2, ground=GROUND, gait_phase=gait_phase, gait_weight=1.0,
        idle_phase=t*math.tau*0.45, stance=11.0,
        body_bob=abs(math.sin(gait_phase*2))*1.2,
    )
    # Keep both hands beside/behind the head; fixed-length IK solves the elbows.
    pose.left_hand = (pose.x-31 + math.sin(gait_phase)*1.5, GROUND-60-49-15)
    pose.right_hand = (pose.x+31 - math.sin(gait_phase)*1.5, GROUND-60-49-15)
    # Reference-keyed feet: alternating stride and lift are interpolated per frame.
    pose.left_foot = (pose.x-11 - stride*17, GROUND-lift*7)
    pose.right_foot = (pose.x+11 + stride*17, GROUND-(1.0-lift)*7)
    return pose

def render_frame(index, fps=FPS):
    t=index/fps
    img=Image.new("RGB",(WIDTH,HEIGHT),WHITE)
    draw=ImageDraw.Draw(img)
    draw.line((0,GROUND+2,WIDTH,GROUND+2),fill=(90,90,90),width=2)
    rig=StickmanRig()
    j=rig.joints(make_pose(t,fps))
    def limb(points,width):
        draw.line([(round(x),round(y)) for x,y in points],fill=INK,width=width,joint="curve")
    limb([j["hip"],j["left_knee"],j["left_foot"]],5)
    limb([j["hip"],j["right_knee"],j["right_foot"]],5)
    limb([j["hip"],j["shoulder"]],6)
    limb([j["shoulder"],j["left_elbow"],j["left_hand"]],5)
    limb([j["shoulder"],j["right_elbow"],j["right_hand"]],5)
    hx,hy=j["head"]; r=rig.rig.head_radius
    draw.ellipse((hx-r,hy-r,hx+r,hy+r),outline=INK,width=5)
    for key in ("left_hand","right_hand"):
        x,y=j[key]; draw.ellipse((x-4,y-4,x+4,y+4),fill=INK)
    return img

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="output/stickman-walk-hands-behind-head.mp4")
    parser.add_argument("--frames-dir",default="output/walk-frames")
    parser.add_argument("--fps",type=int,default=FPS)
    parser.add_argument("--duration",type=float,default=DURATION)
    parser.add_argument("--frames-only",action="store_true")
    args=parser.parse_args()
    if args.fps<=0 or args.duration<=0: parser.error("fps and duration must be positive")
    root=Path(__file__).resolve().parents[1]
    frames=root/args.frames_dir; frames.mkdir(parents=True,exist_ok=True)
    count=round(args.fps*args.duration)
    for i in range(count):
        render_frame(round(i*FPS/args.fps),args.fps).save(frames/f"frame_{i:06d}.png")
    if args.frames_only: return
    ffmpeg=shutil.which("ffmpeg")
    if not ffmpeg: raise SystemExit("FFmpeg is required to encode MP4.")
    output=root/args.output; output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([ffmpeg,"-y","-framerate",str(args.fps),"-i",str(frames/"frame_%06d.png"),
                    "-frames:v",str(count),"-c:v","libx264","-pix_fmt","yuv420p",
                    "-movflags","+faststart",str(output)],check=True)
    print(f"Wrote {count} frames to {output}")

if __name__=="__main__": main()
