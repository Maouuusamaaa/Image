#!/usr/bin/env python3
"""Deterministic, code-drawn cinematic stickman choreography renderer.

Generates numbered PNG frames and optionally an H.264 MP4 using ffmpeg.
All action is stylized and non-graphic; characters are consistent procedural models.
"""
from __future__ import annotations
import argparse, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 960, 540
FPS, DURATION = 60, 30
BG = (9, 13, 27)
WHITE = (236, 243, 255)
CYAN = (60, 224, 255)
ORANGE = (255, 153, 74)
PURPLE = (145, 116, 255)


def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def smooth(t):
    t=clamp(t); return t*t*(3-2*t)
def ease_out(t):
    t=clamp(t); return 1-(1-t)**3
def mix(a,b,t): return a+(b-a)*t

def phase(t, start, end): return smooth((t-start)/(end-start))

def line(draw, pts, fill, width=7):
    draw.line([(int(x),int(y)) for x,y in pts], fill=fill, width=width, joint="curve")

def glow_circle(layer, x, y, radius, color, alpha=180):
    d=ImageDraw.Draw(layer)
    d.ellipse((x-radius,y-radius,x+radius,y+radius), fill=(*color,alpha))

def draw_character(base, x, ground, scale, color, facing, pose, t, accent, glow=0):
    """Draw fixed-proportion stickman using joint positions and pose offsets."""
    layer=Image.new("RGBA", base.size, (0,0,0,0))
    d=ImageDraw.Draw(layer)
    bob=math.sin(t*math.tau*2 + (0 if facing==1 else 1.2))*2.0*scale
    crouch=pose.get("crouch",0)*22*scale
    lean=pose.get("lean",0)*18*scale
    x=float(x); g=float(ground+bob)
    head_r=19*scale
    hip=(x+lean, g-112*scale+crouch)
    shoulder=(x+lean*0.7, g-160*scale+crouch)
    head=(shoulder[0]+facing*pose.get("head",0)*8*scale, shoulder[1]-29*scale)
    if glow:
        glow_circle(layer, head[0], head[1], 36*scale, accent, int(35*glow))
    leg_a=pose.get("leg_a",-0.22*facing)
    leg_b=pose.get("leg_b",0.24*facing)
    stride=pose.get("stride",0)
    knee1=(hip[0]+math.sin(leg_a)*30*scale+stride*16*scale, hip[1]+39*scale)
    foot1=(knee1[0]+math.sin(leg_a+0.45)*33*scale+stride*14*scale, g-3*scale-pose.get("air",0)*20*scale)
    knee2=(hip[0]+math.sin(leg_b)*29*scale-stride*13*scale, hip[1]+40*scale)
    foot2=(knee2[0]+math.sin(leg_b+0.42)*32*scale-stride*18*scale, g-2*scale-pose.get("air",0)*20*scale)
    arm1=pose.get("arm1",(-0.72*facing,0.25))
    arm2=pose.get("arm2",(0.8*facing,0.2))
    elbow1=(shoulder[0]+arm1[0]*27*scale, shoulder[1]+arm1[1]*32*scale)
    hand1=(elbow1[0]+arm1[0]*24*scale+pose.get("reach1",0)*facing*24*scale, elbow1[1]+arm1[1]*26*scale)
    elbow2=(shoulder[0]+arm2[0]*27*scale, shoulder[1]+arm2[1]*32*scale)
    hand2=(elbow2[0]+arm2[0]*24*scale+pose.get("reach2",0)*facing*24*scale, elbow2[1]+arm2[1]*26*scale)
    ink=(*color,255); thick=max(3,int(7*scale))
    line(d,[hip,knee2,foot2],ink,thick)
    line(d,[hip,shoulder],ink,thick+1)
    line(d,[shoulder,elbow2,hand2],ink,thick)
    line(d,[hip,knee1,foot1],ink,thick)
    line(d,[shoulder,elbow1,hand1],ink,thick+1)
    r=head_r
    d.ellipse((head[0]-r,head[1]-r,head[0]+r,head[1]+r), fill=(*BG,255), outline=ink, width=thick)
    eye_x=head[0]+facing*7*scale
    d.line((eye_x-3*scale,head[1]+1*scale,eye_x+4*scale,head[1]+1*scale), fill=(*accent,255), width=max(2,int(3*scale)))
    line(d,[foot1,(foot1[0]+facing*13*scale,foot1[1])],ink,max(3,int(5*scale)))
    line(d,[foot2,(foot2[0]+facing*13*scale,foot2[1])],ink,max(3,int(5*scale)))
    base.alpha_composite(layer)
    return (hand1,hand2,head,hip)

def pose_for(t, side):
    p={"arm1":(-0.72*side,0.25),"arm2":(0.8*side,0.2),"leg_a":-0.22*side,"leg_b":0.24*side}
    if t < 3.5:
        p["arm1"]=(-0.8*side,-0.25); p["arm2"]=(0.75*side,-0.15)
    elif t < 6.0:
        u=phase(t,3.5,6.0); p["stride"]=u; p["lean"]=-0.25*side*u
        p["arm1"]=(-0.7*side,-0.35); p["arm2"]=(0.85*side,-0.1)
    elif t < 8.2:
        u=phase(t,6.0,8.2); p["lean"]=0.5*side*u; p["reach1"]=math.sin(u*math.pi)
        p["arm1"]=(0.95*side,-0.15); p["arm2"]=(0.7*side,-0.7)
    elif t < 10.2:
        u=phase(t,8.2,10.2); p["crouch"]=math.sin(u*math.pi); p["lean"]=-0.9*side*u
        p["arm1"]=(-0.85*side,-0.7); p["arm2"]=(0.9*side,-0.5)
    elif t < 13.0:
        u=phase(t,10.2,13.0); p["stride"]=1.0; p["reach2"]=math.sin(u*math.pi); p["lean"]=0.7*side*u
        p["arm1"]=(-0.75*side,-0.5); p["arm2"]=(1.0*side,0.0)
    elif t < 16.2:
        u=phase(t,13.0,16.2); p["air"]=math.sin(u*math.pi); p["crouch"]=0.15
        p["leg_a"]=mix(-0.22*side,1.0*side,u); p["leg_b"]=mix(0.24*side,-0.9*side,u)
        p["arm1"]=(-0.9*side,-0.8); p["arm2"]=(0.95*side,-0.7)
    elif t < 19.4:
        u=phase(t,16.2,19.4); p["lean"]=-0.8*side*u; p["crouch"]=0.3*u
        p["arm1"]=(0.95*side,-0.1); p["arm2"]=(0.9*side,-0.75); p["reach1"]=math.sin(u*math.pi)
    elif t < 22.4:
        u=phase(t,19.4,22.4); p["stride"]=0.7; p["lean"]=0.35*side*u
        p["arm1"]=(-0.8*side,-0.65); p["arm2"]=(1.0*side,-0.25); p["reach2"]=math.sin(u*math.pi)
    elif t < 25.4:
        u=phase(t,22.4,25.4); p["air"]=math.sin(u*math.pi); p["crouch"]=0.1
        p["leg_a"]=mix(-0.2*side,0.95*side,u); p["leg_b"]=mix(0.2*side,-0.75*side,u)
        p["arm1"]=(-0.9*side,-0.9); p["arm2"]=(0.9*side,-0.85)
    elif t < 27.6:
        u=phase(t,25.4,27.6); p["crouch"]=1-u; p["lean"]=0.3*side*(1-u)
        p["arm1"]=(-0.8*side,-0.4); p["arm2"]=(0.8*side,-0.4)
    else:
        p["arm1"]=(-0.8*side,-0.5); p["arm2"]=(0.85*side,-0.5)
    return p

def render_frame(index, width=W, height=H):
    t=index/FPS
    img=Image.new("RGBA",(W,H),(*BG,255)); d=ImageDraw.Draw(img)
    for y in range(0,H,4):
        k=y/H; c=(int(9+8*k),int(13+10*k),int(27+20*k))
        d.rectangle((0,y,W,y+4),fill=(*c,255))
    horizon=408
    d.line((0,horizon,W,horizon), fill=(49,63,91,255), width=2)
    for x in range(-200,W+200,80):
        d.line((W/2+(x-W/2)*0.25,horizon,x,H),fill=(30,42,67,170),width=1)
    for y in range(horizon+20,H,28): d.line((0,y,W,y),fill=(25,36,58,100),width=1)
    beats=[(0,3.5,"FACE OFF"),(3.5,8.2,"FIRST EXCHANGE"),(8.2,13,"DODGE / COUNTER"),(13,19.4,"ACROBATIC COMBO"),(19.4,25.4,"FINAL EXCHANGE"),(25.4,30,"STANDOFF")]
    label=next((name for a,b,name in beats if a<=t<b),"")
    d.text((42,32), "STICKMAN // CINEMATIC TEST", fill=(148,170,207,220))
    d.text((42,55), label, fill=(231,239,255,240))
    d.text((W-115,32), f"{index:04d}", fill=(117,138,177,210))
    approach=phase(t,3.5,6.0); exchange=phase(t,6.0,8.2); final=phase(t,25.4,27.6)
    left_x=mix(245,390,approach)-22*exchange+8*math.sin(t*1.4)
    right_x=mix(715,570,approach)+22*exchange+8*math.sin(t*1.35+1)
    left_x=mix(left_x,325,final); right_x=mix(right_x,635,final)
    impact=max(math.exp(-((t-c)/0.12)**2) for c in (7.4,11.8,17.5,21.2,24.4))
    sx=math.sin(index*2.1)*impact*5; sy=math.cos(index*1.7)*impact*3
    d.ellipse((left_x-48,horizon-6,left_x+48,horizon+12),fill=(3,6,15,220))
    d.ellipse((right_x-48,horizon-6,right_x+48,horizon+12),fill=(3,6,15,220))
    p1=pose_for(t,1); p2=pose_for(t,-1)
    if 8.2<t<10.2:
        p2["crouch"]=max(p2.get("crouch",0),math.sin((t-8.2)/2*math.pi)*0.7)
    if 16.2<t<19.4:
        p2["lean"]=-0.8*phase(t,16.2,19.4); p2["arm1"]=(0.9,-0.3); p2["arm2"]=(0.85,-0.8)
    draw_character(img,left_x+sx,horizon-4,1.0,WHITE,1,p1,t,CYAN,glow=0.6+0.4*impact)
    draw_character(img,right_x+sx,horizon-4,1.0,WHITE,-1,p2,t,ORANGE,glow=0.6+0.4*impact)
    fx=(left_x+right_x)/2+sx; fy=292+sy
    for center, strength, color in [(7.4,impact,CYAN),(11.8,impact,ORANGE),(17.5,impact,PURPLE),(21.2,impact,CYAN),(24.4,impact,ORANGE)]:
        if strength>0.035:
            rr=18+strength*72; alpha=int(180*strength)
            d.arc((fx-rr,fy-rr,fx+rr,fy+rr),start=205,end=520,fill=(*color,alpha),width=max(2,int(3+strength*5)))
            for j in range(8):
                ang=(j/8)*math.tau+t*3
                r1=rr*0.7; r2=rr*(1.15+0.25*math.sin(t*13+j))
                d.line((fx+math.cos(ang)*r1,fy+math.sin(ang)*r1,fx+math.cos(ang)*r2,fy+math.sin(ang)*r2),fill=(*color,int(alpha*0.8)),width=2)
    vign=Image.new("L",(W,H),0); vd=ImageDraw.Draw(vign)
    vd.ellipse((-120,-150,W+120,H+170),fill=205)
    vign=vign.filter(ImageFilter.GaussianBlur(75))
    shade=Image.new("RGBA",(W,H),(0,0,0,110)); shade.putalpha(Image.eval(vign,lambda p: 110-p//2))
    img=Image.alpha_composite(img,shade)
    if (width,height)!=(W,H): img=img.resize((width,height),Image.Resampling.LANCZOS)
    return img.convert("RGB")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--frames-dir",default="animated/scene-01")
    ap.add_argument("--output",default="output/stickman-battle-scene-01.mp4")
    ap.add_argument("--fps",type=int,default=FPS)
    ap.add_argument("--duration",type=float,default=DURATION)
    ap.add_argument("--width",type=int,default=W)
    ap.add_argument("--height",type=int,default=H)
    ap.add_argument("--frames-only",action="store_true")
    ap.add_argument("--limit-frames",type=int,default=0,help="Render only the first N frames for quick testing")
    args=ap.parse_args()
    if args.fps<=0 or args.duration<=0 or args.width<=0 or args.height<=0: ap.error("fps, duration, width and height must be positive")
    root=Path(__file__).resolve().parents[1]
    frame_dir=(root/args.frames_dir).resolve()
    frame_dir.mkdir(parents=True,exist_ok=True)
    count=int(round(args.fps*args.duration))
    if args.limit_frames: count=min(count,args.limit_frames)
    for i in range(count):
        frame_path=frame_dir/f"frame_{i:06d}.png"
        if not frame_path.exists():
            render_frame(i,args.width,args.height).save(frame_path,compress_level=3)
        if (i+1)%120==0 or i+1==count: print(f"frames: {i+1}/{count}")
    if args.frames_only: return
    ffmpeg=shutil.which("ffmpeg")
    if not ffmpeg: raise SystemExit("ffmpeg was not found; frames were generated but MP4 was not encoded")
    out=(root/args.output).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    cmd=[ffmpeg,"-y","-framerate",str(args.fps),"-i",str(frame_dir/"frame_%06d.png"),"-frames:v",str(count),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
    subprocess.run(cmd,check=True)
    print(f"video: {out} ({count} frames, {args.fps} fps, {count/args.fps:.2f}s)")

if __name__=="__main__": main()
