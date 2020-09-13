import maya.cmds as cmds
import random

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ---               SCRIPT CHE PERMETTE DI GENERARE I MATERIALI PER LA FACCIA
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

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

def createLayeredTexture(face, skin):
    layered = cmds.shadingNode('layeredTexture', asShader= True, name="mLayerSkinFace#")
    #layeredGroup = cmds.sets(layered, renderable= True, noSurfaceShader= True, empty= True, name= "SG" + layered)
    #cmds.connectAttr(layered + '.outColor',layeredGroup + '.surfaceShader')

    cmds.defaultNavigation(connectToExisting=True, force = True, source= face + '.outColor', destination= layered + '.inputs[0].color')
    cmds.defaultNavigation(connectToExisting=True, force = True, source= face + '.outAlpha', destination= layered + '.inputs[0].alpha')
    cmds.defaultNavigation(connectToExisting=True, force = True, source= skin + '.outColor', destination= layered + '.inputs[1].color')

    return layered

def createStandardSurface(layered):
    shader = cmds.shadingNode('aiStandardSurface', asShader= True, name='mSkinFace#')
    shaderGroup = cmds.sets(shader, renderable= True, noSurfaceShader= True, empty= True, name= "SG" + shader)
    cmds.connectAttr(shader + '.outColor',shaderGroup + '.surfaceShader')

    cmds.connectAttr(layered + '.outColor',shader + '.baseColor')
    cmds.setAttr( shader + '.specular', 0.4 )
    cmds.setAttr( shader + '.diffuseRoughness', 1 )
    cmds.setAttr( shader + '.specularRoughness', 1 )


folderFaces = r"/Users/aleclock/Desktop/uni/ModGraf/src/faces"
faceList = cmds.getFileList(folder = folderFaces, filespec = "face*.%s" % "png")

createFaceTextures(faceList)
cmds.file("/Users/aleclock/Desktop/uni/ModGraf/src/material/partial/skinMaterial.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")

skinList = cmds.ls("mSkin*")
faceList = cmds.ls("faceTexture*")


for i in faceList:
    skin = random.choice(skinList)
    layered = createLayeredTexture(i, skin)
    createStandardSurface(layered)

skinFaceList = cmds.ls("mSkinFace*")
skinFaceGroupList = cmds.ls("SGmSkinFace*")

cmds.select(skinFaceGroupList, toggle= True, ne=True)
#cmds.file("/Users/aleclock/Desktop/pippo.mb",type='mayaBinary',exportSelected= True)


"""shadingNode -asTexture layeredTexture;
// Result: layeredTexture2 // 
setAttr layeredTexture2.inputs[0].color -type "double3" 0.2 0.7 0.3;
setAttr layeredTexture2.inputs[0].alpha 1;
setAttr layeredTexture2.inputs[0].blendMode 1;
// Warning: layeredTexture2: could not set BOOL parameter "enable0" // 
// Warning: layeredTexture2: could not set BOOL parameter "enable0" // 
// Warning: layeredTexture2: could not set BOOL parameter "enable0" // 
defaultNavigation -ce -source faceTexture9 -destination layeredTexture2.inputs[0].color;
connectAttr -force faceTexture9.outColor layeredTexture2.inputs[0].color;
// Result: Connected faceTexture9.outColor to layeredTexture2.inputs.color. // 
// Warning: layeredTexture2: could not set BOOL parameter "enable0" // 
// Warning: layeredTexture2: could not set BOOL parameter "enable0" // 
connectAttr -f faceTexture9.outAlpha layeredTexture2.inputs[0].alpha;
// Result: Connected faceTexture9.outAlpha to layeredTexture2.inputs.alpha. // 
defaultNavigation -ce -source mSkin02 -destination layeredTexture2.inputs[1].color;
connectAttr -force mSkin02.outColor layeredTexture2.inputs[1].color;
// Result: Connected mSkin02.outColor to layeredTexture2.inputs.color. // 
// Warning: unable to connect standard_surface() to layer_rgba(input1) - types are not compatible (CLOSURE to RGBA) // 
// Warning: [mtoa] Could not link mSkin02 to layeredTexture2.input1. // 
rename aiStandardSurface1 "mSkinFace00" ;
// Result: mSkinFace20 // 
rename aiStandardSurface1SG "SGmSkinFace00" ;
// Result: SGmSkinFace01 // 
defaultNavigation -ce -source layeredTexture2 -destination mSkinFace20.baseColor;
connectAttr -force layeredTexture2.outColor mSkinFace20.baseColor;
// Result: Connected layeredTexture2.outColor to mSkinFace20.baseColor. // 
// Warning: unable to connect standard_surface() to layer_rgba(input1) - types are not compatible (CLOSURE to RGBA) // 
// Warning: [mtoa] Could not link mSkin02 to layeredTexture2.input1. // 
// Warning: unable to connect standard_surface() to layer_rgba(input1) - types are not compatible (CLOSURE to RGBA) // 
// Warning: [mtoa] Could not link mSkin02 to layeredTexture2.input1. // 
setAttr "mSkinFace20.specular" 0.4;
// Warning: unable to connect standard_surface() to layer_rgba(input1) - types are not compatible (CLOSURE to RGBA) // 
// Warning: [mtoa] Could not link mSkin02 to layeredTexture2.input1. // 
// Warning: unable to connect standard_surface() to layer_rgba(input1) - types are not compatible (CLOSURE to RGBA) // 
// Warning: [mtoa] Could not link mSkin02 to layeredTexture2.input1. // 
setAttr "mSkinFace20.diffuseRoughness" 0.608;
setAttr "mSkinFace20.diffuseRoughness" 1;
setAttr "mSkinFace20.specularRoughness" 1;"""
