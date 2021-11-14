import maya.cmds as cmds

from autoRigger.base import bone
from autoRigger import util
from ..utility.rigging import joint, transform


class Chain(bone.Bone):
    """
    Abstract chain module
    """

    def __init__(self, side, name, segment=6):
        bone.Bone.__init__(self, side, name)

        self._rtype = 'chain'

        self.segment = segment
        self.interval = None
        self.dir = None
        self.curve = None

    def create_locator(self):
        for index in range(self.segment):
            cmds.spaceLocator(n=self.locs[index])
            if index:
                cmds.parent(self.locs[index], self.locs[index-1], relative=1)
                distance = (self.interval * self.dir).as_list
                util.move(self.locs[index], distance)
        cmds.parent(self.locs[0], util.G_LOC_GRP)

    def place_controller(self):
        for index in range(self.segment):
            cmds.duplicate(self._shape, name=self.ctrls[index])
            cmds.group(em=1, name=self.offsets[index])
            transform.match_xform(self.offsets[index], self.jnts[index])

            cmds.parent(self.ctrls[index], self.offsets[index], relative=1)
            if index:
                cmds.parent(self.offsets[index], self.ctrls[index-1])

        cmds.parent(self.offsets[0], util.G_CTRL_GRP)

    def create_joint(self):
        cmds.select(clear=1)
        for index, loc in enumerate(self.locs):
            pos = cmds.xform(loc, q=1, t=1, ws=1)
            cmds.joint(p=pos, name=self.jnts[index])

        cmds.parent(self.jnts[0], util.G_JNT_GRP)
        joint.orient_joint(self.jnts[0])
