import maya.cmds as cmds

# ---- place2dTexture
texture = cmds.shadingNode('file', asTexture= True, isColorManaged= True, name='face')
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

# ---- standardSurface
shader = cmds.shadingNode('standardSurface', asShader= True, name= 'Skin')
shaderGroup = cmds.sets(shader, renderable= True, noSurfaceShader= True, empty= True, name= "standardSurface1SG")

cmds.connectAttr(shader + '.outColor',shaderGroup + '.surfaceShader')

# Inserimento immagine del volto e del colore della surface
cmds.setAttr(texture + '.fileTextureName','/Users/aleclock/Desktop/uni/ModGraf/src/face.png',type="string")
cmds.setAttr(shader + '.baseColor', 1, 0.5882, 0.9352, type = 'double3')


# ---- layeredTexture
layered = cmds.shadingNode('layeredTexture', asTexture= True)

cmds.defaultNavigation(connectToExisting=True, force = True, source= texture + '.outColor', destination= layered + '.inputs[0].color')
cmds.defaultNavigation(connectToExisting=True, force = True, source= texture + '.outAlpha', destination= layered + '.inputs[0].alpha')
cmds.defaultNavigation(connectToExisting=True, force = True, source= shader + '.outColor', destination= layered + '.inputs[1].color')

# ---- blinnMaterial
blinnShader = cmds.shadingNode('blinn', asShader= True, name='mSkin')
blinnShaderGroup = cmds.sets(blinnShader, renderable= True, noSurfaceShader= True, empty= True, name= "blinn1SG")
cmds.connectAttr(blinnShader + '.outColor', blinnShaderGroup + '.surfaceShader')

 
cmds.connectAttr(layered + '.outColor', blinnShader + '.color')

cmds.select( 'head', r= True ) 
cmds.sets(forceElement = blinnShaderGroup)

#cmds.hilite(cube)
cmds.polyMapDel('head.f[0:71]', constructionHistory=True)
cmds.polyMapDel('head.f[73:293]', constructionHistory=True)
cmds.polyMapDel('hair.f[0:25]', constructionHistory=True)
cmds.select('head.f[72]', r= True)
cmds.polyEditUV( uValue=0, vValue=0.34) 
cmds.setAttr ('headShape.uvPivot',0.5, 0.45, type='double2')
cmds.polyEditUV(pivotU = 0.5, pivotV = 0.45, scaleU=3, scaleV=3)
#cmds.select(clear=True)