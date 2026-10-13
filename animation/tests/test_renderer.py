import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from rig import StickmanRig, Pose, distance
import render_battle

class RigTests(unittest.TestCase):
    def test_arm_and_leg_segment_lengths_are_stable(self):
        rig = StickmanRig()
        p = Pose(400, render_battle.GROUND, right_hand=(460, 330), left_hand=(360, 330))
        j = rig.joints(p)
        self.assertAlmostEqual(distance(j['shoulder'], j['right_elbow']), rig.rig.upper_arm, places=3)
        self.assertAlmostEqual(distance(j['right_elbow'], j['right_hand']), rig.rig.forearm, places=3)
        self.assertAlmostEqual(distance(j['hip'], j['left_knee']), rig.rig.thigh, places=3)
        self.assertAlmostEqual(distance(j['left_knee'], j['left_foot']), rig.rig.shin, places=3)

    def test_feet_stay_on_ground(self):
        poses, _ = render_battle.scene_state(6.7)
        for pose in poses:
            joints = StickmanRig().joints(pose)
            self.assertEqual(joints['left_foot'][1], render_battle.GROUND)
            self.assertEqual(joints['right_foot'][1], render_battle.GROUND)

    def test_impact_is_not_active_before_contact(self):
        attack = render_battle.ATTACKS[0]
        self.assertEqual(render_battle.attack_weight(attack['start']-0.01, attack), 0)
        self.assertGreater(render_battle.attack_weight(attack['contact'], attack), 0.99)
        poses_before, active_before = render_battle.scene_state(attack['contact']-0.02)
        poses_after, active_after = render_battle.scene_state(attack['contact']+0.03)
        self.assertEqual(len(active_before), 1)
        self.assertEqual(len(active_after), 1)
        self.assertEqual(poses_before[1].crouch, 0)
        self.assertGreater(poses_after[1].crouch, 0)

    def test_render_output(self):
        frame = render_battle.render_frame(0)
        self.assertEqual(frame.size, (960,540))
        self.assertEqual(frame.mode, 'RGB')
        self.assertEqual(render_battle.render_frame(90).size, frame.size)

    def test_attack_schedule_is_ordered(self):
        contacts = [a['contact'] for a in render_battle.ATTACKS]
        self.assertEqual(contacts, sorted(contacts))
        for attack in render_battle.ATTACKS:
            self.assertLess(attack['start'], attack['contact'])
            self.assertLess(attack['contact'], attack['end'])

if __name__ == '__main__': unittest.main()
