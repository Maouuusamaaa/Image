import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
import render_walk
from rig import StickmanRig, distance

class ReferenceWalkTests(unittest.TestCase):
    def test_keyframes_form_closed_loop(self):
        self.assertEqual(render_walk.KEYS[0][1:],render_walk.KEYS[-1][1:])

    def test_walk_changes_foot_positions(self):
        rig=StickmanRig()
        a=rig.joints(render_walk.make_pose(0.10))
        b=rig.joints(render_walk.make_pose(0.35))
        self.assertNotEqual(a["left_foot"],b["left_foot"])
        self.assertNotEqual(a["right_foot"],b["right_foot"])

    def test_hands_remain_near_head_and_arm_lengths_stable(self):
        rig=StickmanRig()
        for t in (0.0,0.2,0.4,0.6,0.8,1.0,2.0,3.0):
            j=rig.joints(render_walk.make_pose(t))
            hx,hy=j["head"]
            for side in ("left","right"):
                hand=j[f"{side}_hand"]
                self.assertLess(abs(hand[0]-hx),55)
                self.assertLess(hand[1],hy+25)
                self.assertAlmostEqual(distance(j["shoulder"],j[f"{side}_elbow"]),rig.rig.upper_arm,places=3)
                self.assertAlmostEqual(distance(j[f"{side}_elbow"],hand),rig.rig.forearm,places=3)

    def test_frame_dimensions(self):
        frame=render_walk.render_frame(0)
        self.assertEqual(frame.size,(960,540))
        self.assertEqual(frame.mode,"RGB")

if __name__=="__main__": unittest.main()
