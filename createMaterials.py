 import maya.cmds as cmds

def createSkinMaterials():

    # *****************************************
    # Skin materials
    # *****************************************

    # Elimina materiali se già esistenti
    skinList = cmds.ls("skin*")
    if len(skinList)>0:
        cmds.delete(skinList)
        skinList = []

    shd = cmds.shadingNode('lambert', name="skin#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 1, 0.8588, 0.6745, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    skinList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="skin#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.945, 0.7607, 0.4901, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    skinList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="skin#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.8784, 0.6745, 0.4117, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    skinList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="skin#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.7764, 0.5254, 0.2588, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    skinList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="skin#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.5529, 0.3333, 0.1411, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    skinList.append(shdSG)
    
    return skinList

def createHairMaterials():

    # *****************************************
    # Hair materials
    # *****************************************

    # Elimina materiali se già esistenti
    hairList = cmds.ls("hairM*")
    if len(hairList)>0:
        cmds.delete(hairList)
        hairList = []

    shd = cmds.shadingNode('lambert', name="hairM#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.0901, 0.0705, 0.0431, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    hairList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="hairM#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0, 0, 0, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    hairList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="hairM#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.8, 0.6, 0.4, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    hairList.append(shdSG)

    shd = cmds.shadingNode('lambert', name="hairM#", asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.setAttr ( (shd + '.color'), 0.3529, 0.2196, 0.145, type = 'double3' )
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    hairList.append(shdSG)

    return hairList