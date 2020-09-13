# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ---------    CREAZIONE DEI MATERIALI
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

# *****************************************
# Skin surfaces
# *****************************************

def createSkinSurfaces(r,g,b):

    shader = cmds.shadingNode('standardSurface', asShader= True, name= 'skinSurface#')
    shaderGroup = cmds.sets(shader, renderable= True, noSurfaceShader= True, empty= True, name= "standardSurface1SG")   # Capire come cambiare nome standardSurface#SG
    cmds.connectAttr(shader + '.outColor',shaderGroup + '.surfaceShader')
    cmds.setAttr(shader + '.baseColor', r, g, b, type = 'double3')

# *****************************************
# Face textures
# *****************************************

def createFaceTextures(faceList):
    
    for f in faceList:
        texture = cmds.shadingNode('file', asTexture= True, isColorManaged= True, name='faceTexture#')
        utility = cmds.shadingNode('place2dTexture', asUtility= True)

        cmds.connectAttr(utility + '.coverage',texture + '.coverage')
        cmds.connectAttr(utility + '.translateFrame',texture + '.translateFrame')
        cmds.connectAttr(utility + '.rotateFrame',texture + '.rotateFrame')
        cmds.connectAttr(utility + '.mirrorU',texture + '.mirrorU')
        cmds.connectAttr(utility + '.mirrorV',texture + '.mirrorV')
        cmds.connectAttr(utility + '.stagger',texture + '.stagger')
        cmds.connectAttr(utility + '.wrapU',texture + '.wrapU')
        cmds.connectAttr(utility + '.wrapV',texture + '.wrapV')
        cmds.connectAttr(utility + '.repeatUV',texture + '.repeatUV')
        cmds.connectAttr(utility + '.offset',texture + '.offset')
        cmds.connectAttr(utility + '.rotateUV',texture + '.rotateUV')
        cmds.connectAttr(utility + '.noiseUV',texture + '.noiseUV')
        cmds.connectAttr(utility + '.vertexUvOne',texture + '.vertexUvOne')
        cmds.connectAttr(utility + '.vertexUvTwo',texture + '.vertexUvTwo')
        cmds.connectAttr(utility + '.vertexUvThree',texture + '.vertexUvThree')
        cmds.connectAttr(utility + '.vertexCameraOne',texture + '.vertexCameraOne')
        cmds.connectAttr(utility + '.outUV',texture + '.uv')
        cmds.connectAttr(utility + '.outUvFilterSize',texture + '.uvFilterSize')

        cmds.setAttr(texture + '.fileTextureName','/Users/aleclock/Desktop/uni/ModGraf/src/faces/' + f,type="string")

# *****************************************
# Layered textures
# *****************************************

# TODO se decido di usare una layered Texture anche per gli altri materiali, utilizzare questa per generalizzare e passargli i valori dei livelli 
def createLayeredTexture():
    faceTextures = cmds.ls("faceTexture*")
    skinSurface = cmds.ls("skinSurface*")

    face = getRandomElement(faceTextures)
    skin = getRandomElement(skinSurface)

    layered = cmds.shadingNode('layeredTexture', asTexture= True)

    cmds.defaultNavigation(connectToExisting=True, force = True, source= face + '.outColor', destination= layered + '.inputs[0].color')
    cmds.defaultNavigation(connectToExisting=True, force = True, source= face + '.outAlpha', destination= layered + '.inputs[0].alpha')
    cmds.defaultNavigation(connectToExisting=True, force = True, source= skin + '.outColor', destination= layered + '.inputs[1].color')
    
    return layered

# *****************************************
# lambert material
# *****************************************

def createLambertMaterial(layeredTexture):
    lambertShader = cmds.shadingNode('lambert', asShader= True, name='lambertSkin#')
    lambertShaderGroup = cmds.sets(lambertShader, renderable= True, noSurfaceShader= True, empty= True, name= "SG" + lambertShader)

    cmds.connectAttr(lambertShader + '.outColor',lambertShaderGroup + '.surfaceShader')
    cmds.connectAttr(layeredTexture + '.outColor',lambertShader + '.color')

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