import re
import os
import maya.cmds as cmds

## import some database information
# import imageProxy
# import omoikane.client.functions as ocf
# import omoikane.client.datatypes as ocd

PRIMARY_PATTERN   = re.compile("(?P<variant>primary_v\d+|primary)")
SECONDARY_PATTERN = re.compile("(?P<variant>secondary_v\d+|secondary)")
TAKE_PATTERN      = re.compile("(?P<variant>take_v\d+|secondary)")

def GetAllRenderLayers():
    rl = [i for i in cmds.ls(type="renderLayer") if not re.match("\w+:\w+", i)]
    return rl

def GetActiveRenderLayers():
    rl = [i for i in GetAllRenderLayers() if cmds.getAttr("%s.renderable"%(i))==True]
    return rl

def GetCurrentRenderLayer():
    rl = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
    return rl

def SetCurrentRenderLayer(layer="defaultRenderLayer"):
    cmds.editRenderLayerGlobals(currentRenderLayer=layer)

def SetActiveRenderLayer(layer="defaultRenderLayer"):
    SetCurrentRenderLayer(layer)
    crl = GetCurrentRenderLayer()

    for eachRL in GetAllRenderLayers():
        if eachRL != crl:
            cmds.setAttr("%s.renderable"%(eachRL), 0)

def GetAllCameras():
    cameras = cmds.listCameras()
    return cameras

def GetRenderableCamera():
    camera = "persp"
    for cam in GetAllCameras():
        if cmds.getAttr("%s.renderable"%(cam)):
            camera = cam
            return camera

    return camera

# def GetProject():
#     proj = os.environ.get("VE_ENV_PROJ", os.environ.get("MZ_ENV_PROJ", "test"))
#     return proj

# def GetSequence():
#     seq = os.environ.get("VE_ENV_SEQ", os.environ.get("MZ_ENV_SEQ", "PROJ"))
#     return seq

# def GetShot():
#     shot = os.environ.get("VE_ENV_SHOT", os.environ.get("MZ_ENV_SHOT", "ALL"))
#     return shot

def GetCurrentSceneFile():
    scene = cmds.file(q=True, sn=True)
    return scene

def GetTimelineStartFrame(useInt=True):
    frame = cmds.playbackOptions(q=True, min=True)
    if useInt:
        return int(frame)
    return frame

def GetTimelineEndFrame(useInt=True):
    frame = cmds.playbackOptions(q=True, max=True)
    if useInt:
        return int(frame)
    return frame

def GetTimelineCurrentFrame(useInt=True):
    frame = cmds.currentTime(q=True)
    if useInt:
        return int(frame)
    return frame
