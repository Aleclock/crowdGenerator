import maya.cmds as cmds
import os 
import functools
import random
import pymel.core as pm

os.chdir("/Users/aleclock/Desktop/uni/ModGraf/crowdGenerator") # Go to path

"""
Create user interface
"""
def createUI( windowTitle, pApplyCallback ):

    windowID = 'myWindowID'

    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )

    # Callback per il caricamento dei materiali
    def loadMaterialsCallback( *pArgs ):
        cmds.file("./src/material/SGmComplete.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        """cmds.file("./src/material/SGmSkinFace.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmHair00_08.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmBody_Tee00_07.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmBody_Shirt00_12.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmBody_sweater00_04.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmTrousers_jeans00_03.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmTrousers_standard00_04.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmTrousers_velvet00_05.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")"""

        # Callback per la rimozione dei materiali
    def deleteMaterialsCallback( *pArgs ):
        #TODO eliminare quelli giusti
        deleteElements("faceTexture*")
        deleteElements("mSkin*")
        deleteElements("mSkinFace*")
        deleteElements("mTee*")
        deleteElements("trousers_velvet*")
        deleteElements("place2dTexture*")
    
    # Callback per il caricamento dei modelli
    def loadModelsCallback( *pArgs ):
        # Variabili per l'import del modello
        folderPerson = r"./src"
        folderHair  = r"./src/hair"
        fileType = "mb"

        baseModel = cmds.getFileList(folder = folderPerson, filespec = "person_newModel.%s" % fileType)
        haircutModel = cmds.getFileList(folder = folderHair, filespec = "haircut*.%s" % fileType)
        
        # Delete existing models
        deleteModelsCallback()

        cmds.group( em=True, name='models' )

        importModels(haircutModel, folderHair,':')
        cmds.parent(cmds.ls("hair*"),'models')

        importModels(baseModel, folderPerson,'stickman')
        cmds.parent(cmds.ls("*:person*"),'models')
    
    # Callback per la rimozione dei modelli
    def deleteModelsCallback( *pArgs ):
        deleteElements("*:person")
        deleteElements("models")
        deleteElements("row_group*")
        deleteElements("hair*")
        
    with pm.window(title= windowTitle ,sizeable=False):
        with pm.rowColumnLayout():
            with pm.frameLayout(label='Crowd creation', font = "boldLabelFont"):
                with pm.rowColumnLayout(numberOfColumns=5, columnWidth=[(1,10),(2, 60), (3, 60), (4, 60),(5,10)]):
                    addSeparator(5, 10) # number of separator, height
                    
                    cmds.separator(h=10, style="none")
                    cmds.text (label = "Materials", align = "left")
                    cmds.button (label = "Load", command= loadMaterialsCallback )
                    cmds.button (label = "Delete", command= deleteMaterialsCallback )
                    cmds.separator( h=10, style='none' )
                    
                    addSeparator(5,2)
                    
                    cmds.separator(h=10, style="none")
                    cmds.text (label = "Models", align = "left")
                    cmds.button (label = "Load", command= loadModelsCallback )
                    cmds.button (label = "Delete", command= deleteModelsCallback )
                    cmds.separator( h=10, style='none' )
                    
                    cmds.separator( h=10, style='none' )
                    cmds.text (label = "Rows", align = "left")
                    nRowsField = cmds.intField(minValue=1, value=4)
                    addSeparator(2, 10)
                    
                    cmds.separator( h=10, style='none' )
                    cmds.text (label = "Seats", align = "left")
                    nSeatsField = cmds.intField(minValue=10, value=15)
                    addSeparator(2, 10)
                    
                    addSeparator(5,10)

                    addSeparator(2, 10)
                    cmds.button (label = "Apply", command = functools.partial ( pApplyCallback, nRowsField,nSeatsField )) 
                    cmds.button (label = "Delete", command = deleteViewerCallback)
                    
                    addSeparator(5,10)
        
                    cmds.setParent( '..' )
                    
            with pm.frameLayout(label='Animation', font = "boldLabelFont"): #collapsable = True
                with pm.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,40),(2, 60), (3, 60),(4,40)]):
                    addSeparator(4, 10)
                    
                    cmds.separator(h=10, style="none")
                    cmds.text (label = "Exultance", align = "left")
                    cmds.button( label='Create', command = animExultanceCallback)
                    addSeparator(4,10)
        
                    cmds.setParent( '..' )

            with pm.frameLayout(label='Customization', font = "boldLabelFont"): #collapsable = True
                with pm.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,10),(2, 180), (3,10)]):
                    addSeparator(4, 10)
                    pm.text('Select item to change and click the action', wordWrap = True, align='left')
                    addSeparator(5, 10)
            
                    alertButton = cmds.text (label = "", wordWrap = True, align='center', font = "boldLabelFont")
                with pm.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,40),(2, 60), (3, 60),(4,40)]):
                    addSeparator(4, 10)
                    
                    cmds.separator(h=10, style="none")
                    cmds.text (label = "Stickman")
                    #cmds.button (label = "Change", command= changeViewerCallback )
                    cmds.button (label = "Change", command = functools.partial ( changeViewerCallback, alertButton))
                    addSeparator(2, 10)
                    cmds.text (label = "Animation")
                    cmds.button (label = "Change", command= functools.partial ( changeAnimationCallback, alertButton))
                    cmds.separator(h=10, style="none")
                    
                    addSeparator(4,10)
                    cmds.setParent( '..' )

# Callback per la creazione della folla 
def applyCallback(nRowsField, nSeatsField, *pArgs):
    nRows = cmds.intField (nRowsField, query =  True, value = True)
    nSeats = cmds.intField (nSeatsField, query =  True, value = True)
    deleteElements("row_group*")
    #TODO capire perchè elimino i capelli
    deleteElements("hair_*")
    drawModels(nRows, nSeats)

def deleteViewerCallback(*pArgs):
    deleteElements("row_group*")

def animExultanceCallback(*pArgs):
    viewerList = cmds.ls("viewer*")
    fileType = "atom"
    anim_folder  = r"./src/animation"
    animList = cmds.getFileList(folder = anim_folder, filespec = "*.%s" % fileType) # list of animation files 

    anim = getAnimationSequence(animList, viewerList)
    for v in viewerList:
        coord = getStickmanOrigin(v)
        setAnimation(v, anim_folder + "/" + str(anim[viewerList.index(v)]))
        translateAnimationKeys(v, coord)

"""
cutKey -clear -time ":" -hierarchy none -controlPoints 0 -shape 1 {"viewer_4|ikHandle_foot_L", "viewer_4|ikHandle_hand_L", "viewer_4|ikHandle_hand_R", "viewer_4|ikHandle_head", "viewer_4|ikHandle_foot_R"};
"""
def changeAnimationCallback(button, *pArgs):
    fileType = "atom"
    anim_folder  = r"./src/animation"
    animList = cmds.getFileList(folder = anim_folder, filespec = "*.%s" % fileType) # list of animation files 

    selected = cmds.ls (selection = True) # Selected items
    for s in selected:
        if s[0:6] == "viewer" and "|" not in s: # if the item selected can be animated
            pm.text(button, label="", edit = True )
            rowGroup = pm.listRelatives(s, allParents = True)[0] # Take the first (and unique) element
            coord = getStickmanOrigin(s)
            
            # https://help.autodesk.com/cloudhelp/2018/JPN/Maya-Tech-Docs/PyMel/generated/functions/pymel.core.animation/pymel.core.animation.cutKey.html
            pm.cutKey( {s + "|ikHandle_foot_L",s + "|ikHandle_hand_L",s + "|ikHandle_hand_R",s + "|ikHandle_head",s + "|ikHandle_foot_R"}, time=":", clear = True, hierarchy = "none", controlPoints = False, shape = True)
            
            setAnimation(s, anim_folder + "/" + str(getRandomElement(animList)))
            #print (pm.keyframe(s + "|ikHandle_foot_L", query = True, name = True))

            translateAnimationKeys(s, coord)
            cmds.select (rowGroup + ' | ' + s)
        else:
            pm.text(button, label="ATTENTION: <br/>Please select viewer's to modify", edit = True )

def changeViewerCallback(button, *pArgs):
    selected = cmds.ls (selection = True) # Selected items
    for s in selected:
        if s[0:6] == "viewer" and "|" not in s: # if the item selected can be animated
            pm.text(button, label="", edit = True )
            # https://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.nodetypes/pymel.core.nodetypes.DagNode.html
            rowGroup = pm.listRelatives(s, allParents = True)[0] # Take the first (and unique) element

            mBody = getRandomElement(cmds.ls("SGmBody*"))
            setMaterial(rowGroup + ' | ' + s + '|body',mBody)
            
            mTrousers = getRandomElement(cmds.ls("SGmTrousers*"))
            setMaterial(rowGroup + ' | ' + s + '|body|l_leg', mTrousers)
            setMaterial(rowGroup + ' | ' + s + '|body|r_leg', mTrousers)

            mSkinFace = cmds.ls("SGmSkinFace*")
            mSkinFace = getRandomElement(mSkinFace)
            setMaterial(rowGroup + ' | ' + s + '|body|head', mSkinFace)

            mSkin = getSkinMaterial(mSkinFace) + "SG"
            setMaterial(rowGroup + ' | ' + s + '|body|r_arm|r_hand', mSkin)
            setMaterial(rowGroup + ' | ' + s + '|body|l_arm|l_hand', mSkin)
            
            hairList = cmds.ls("hairstyle*")
            hairName = getRandomElement(hairList)
            hair = cmds.duplicate (hairName, name = "hair#") [0]
            hairCoord = pm.getAttr(rowGroup + ' | ' + s + '|body|head|hair*' + ".translate")
            cmds.parent(hair, rowGroup + ' | ' + s)
            cmds.select (rowGroup + ' | ' + s + '|body|head|hair*')
            cmds.select (rowGroup + ' | ' + s + '|' + hair ,add = True)
            pm.runtime.ReplaceObjects(scale = False)

            # Necessario in quanto altrimenti verrebbe traslato di un minimo (ReplaceObjects non mantiene perfettamente le coordinate precedenti)
            pm.setAttr( rowGroup + ' | ' + s + "|body|head|hair*" + ".translateX", hairCoord[0])
            pm.setAttr( rowGroup + ' | ' + s + "|body|head|hair*" + ".translateY", hairCoord[1])
            pm.setAttr( rowGroup + ' | ' + s + "|body|head|hair*" + ".translateZ", hairCoord[2])

            cmds.parentConstraint (s + "|joint_COG|joint_spine|joint_neck", rowGroup + ' | ' + s + '|body|head|hair*', maintainOffset = True, weight = True)

            cmds.select (rowGroup + ' | ' + s)
        else:
            pm.text(button, label="ATTENTION: <br/>Please select viewer's to modify", edit = True )



# Funzione che importa i vari modelli
def importModels(model, folder, ns):    # ns: namespace
    for item in model:
        fname = os.path.join(folder, item)
        objName, ext = os.path.splitext(os.path.basename(fname))
        # import each file
        imported_objects = cmds.file(fname, i=True, rnn=True, mergeNamespacesOnClash =False, namespace=ns, loadReferenceDepth='all', importFrameRate=True, type='mayaBinary') 

"""
Delete objects if exists
Input:
    el: element to delete
"""
def deleteElements(el):
    bodyList = cmds.ls(el)
    if len(bodyList)>0:
        cmds.delete(bodyList)

# Funzione che elimina materiali se già esistenti
"""
Delete materials if exists
Input:
    
"""
def deleteMaterials():
    skinList = cmds.ls("skin*")
    if len(skinList)>0:
        cmds.delete(skinList)
        skinList = []

# Add multiple separator
def addSeparator(n, height):
    for _ in range(n):
        cmds.separator(h=height, style="none")

createUI("Crowd generator", applyCallback)

def drawModels (nRows, nSeats):

    bodyList = cmds.ls("*:person")
    bodyName = bodyList[0]

    hairList = cmds.ls("hairstyle*")
    # Ciclo per creazione di file e posti
    count = 0
    for i in range (0,nRows):
        rowGroup = cmds.group(empty=True, name="row_group"+ str(i+1))
        for j in range (0,nSeats):
            body = cmds.duplicate (bodyName, name = "viewer_#", rr = True, un = True) [0]
            cmds.parent(body,rowGroup)
            
            mBody = getRandomElement(cmds.ls("SGmBody*"))
            setMaterial(rowGroup + ' | ' + body + '|body',mBody)
            
            mTrousers = getRandomElement(cmds.ls("SGmTrousers*"))
            setMaterial(rowGroup + ' | ' + body + '|body|l_leg', mTrousers)
            setMaterial(rowGroup + ' | ' + body + '|body|r_leg', mTrousers)

            mSkinFace = cmds.ls("SGmSkinFace*")
            mSkinFace = getRandomElement(mSkinFace)
            setMaterial(rowGroup + ' | ' + body + '|body|head', mSkinFace)
            uvMapskinFace(rowGroup,body)

            mSkin = getSkinMaterial(mSkinFace) + "SG"
            setMaterial(rowGroup + ' | ' + body + '|body|r_arm|r_hand', mSkin)
            setMaterial(rowGroup + ' | ' + body + '|body|l_arm|l_hand', mSkin)

            hairName = getRandomElement(hairList)
            hair = cmds.duplicate (hairName, name = "hair#") [0]
            cmds.parent(hair, rowGroup + ' | ' + body)
            cmds.select (rowGroup + ' | ' + body + '|body|head|hair')
            cmds.select (rowGroup + ' | ' + body + '|' + hair ,add = True)
            pm.runtime.ReplaceObjects(scale = False)

            mHair = cmds.ls("SGmHair*")
            mHair = getRandomElement(mHair)
            setMaterial(rowGroup + ' | ' + body + '|body|head|hair*' ,mHair)

            cmds.parentConstraint ("viewer_" + str(count+1) + "|joint_COG|joint_spine|joint_neck", rowGroup + ' | ' + body + '|body|head|hair*', maintainOffset = True, weight = True)

            selectRig('viewer_' + str(count+1)) # Si seleziona il Rig in quanto selezionando il gruppo lo spostamento viene male

            x = random.uniform(-0.5, 0.5) + (6 * j)
            y = 3 * i
            z = random.uniform(-0.5, 0.5) + (-3 * i)
            
            cmds.move(x,y,z, r = True)
            #freezeIkTransformation('viewer_' + str(count+1))
            
            count = count + 1
        cmds.xform(rowGroup,centerPivots=True)
    
    cmds.hide('models') # Hide models

def getRandomElement(sequence):
    return random.choice(sequence)

"""
Set material in path shape
Input:
    path: shape 
    material: material to set
"""
def setMaterial(path, material):
    cmds.select(path, r= True)
    cmds.sets(e=1, forceElement= material)

"""
Apply uv mapping to mSkinFace material
Input:
    rowGroup: root of shape (group)
    body: 
"""
def uvMapskinFace(rowGroup, body):
    #cmds.hilite(cube)
    cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head.f[0:71]', constructionHistory=True)
    cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head.f[73:293]', constructionHistory=True)
    cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head|hair.f[0:25]', constructionHistory=True)
    cmds.select(rowGroup + ' | ' + body + '|body|head.f[72]', r= True)
    cmds.polyEditUV( uValue=0, vValue=0.34) 
    cmds.setAttr (rowGroup + ' | ' + body + '|body|head|headShape.uvPivot',0.5, 0.45, type='double2')
    cmds.polyEditUV(pivotU = 0.5, pivotV = 0.45, scaleU=3.5, scaleV=3.5)

def getSkinMaterial(material):
    cmds.select("mLayer" + material[3:], visible = False)
    mSkin = pm.defaultNavigation(defaultTraversal=True, destination= "mLayer" + material[3:] + ".inputs[1].color")
    return mSkin[0]


"""
Select rig of path model
Input:
    path: path of model (rig root)
"""
def selectRig(path):
    #cmds.select(cl = True) # cl: clear
    cmds.select(path + "|joint_COG", visible = False)
    cmds.select(path + "|ikHandle_foot_L", visible = True, add = True)
    cmds.select(path + "|ikHandle_foot_R", visible = True, add = True)
    cmds.select(path + "|ikHandle_hand_L", visible = True, add = True)
    cmds.select(path + "|ikHandle_hand_R", visible = True, add = True)
    cmds.select(path + "|ikHandle_head", visible = True, add = True)

"""
Select all the Ik handle, so the rig withoud COG
Input:
    path: path of model (rig root)
"""
def selectIkHandle(path):
    cmds.select(path + "|ikHandle_foot_L", visible = True)
    cmds.select(path + "|ikHandle_foot_R", visible = True, add = True)
    cmds.select(path + "|ikHandle_hand_L", visible = True, add = True)
    cmds.select(path + "|ikHandle_hand_R", visible = True, add = True)
    cmds.select(path + "|ikHandle_head", visible = True, add = True)

"""
Freeze transformation of ik handle
Input:
    path: path of model

FREEZE TRANSFORMATION (ROTATION AND TRANSLATION)

select -r viewer_6|ikHandle_foot_L ;
select -add viewer_6|ikHandle_hand_L ;
select -add viewer_6|ikHandle_hand_R ;
select -add viewer_6|ikHandle_head ;
select -add viewer_6|ikHandle_foot_R ;
makeIdentity -apply true -t 1 -r 1 -s 0 -n 0 -pn 1;

https://download.autodesk.com/global/docs/maya2012/en_us/CommandsPython/makeIdentity.html
"""
def freezeIkTransformation(path):
    selectIkHandle(path)
    cmds.makeIdentity(apply=True, translate=True , rotate = True, scale = False, normal = False)

"""
IMPORT ANIMAZION
select -r ikHandle_foot_L ;
select -add ikHandle_hand_L ;
select -add ikHandle_hand_R ;
select -add ikHandle_head ;
select -add ikHandle_foot_R ;
makeIdentity -apply true -t 1 -r 1 -s 0 -n 0 -pn 1;     # Permette di fare freeze transformation
file -import -type "atomImport" -ra true -namespace "anim" -options ";;targetTime=1;srcTime=1:6;dstTime=1:6;option=scaleInsert;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=/Users/aleclock/Documents/maya/projects/default/data/;" "/Users/aleclock/Desktop/anim.atom";
file -import -type "atomImport" -ra true -namespace "anim_row_group01" -options ";;targetTime=3;option=insert;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=/Users/aleclock/Documents/maya/projects/default/data/;" "/Users/aleclock/Desktop/uni/ModGraf/crowdGenerator/src/anim_row_group01.atom";
"""
def setAnimation(viewer, anim_name):
    selectIkHandle(viewer)
    cmds.file(anim_name, type = "atomImport" , i= True, renameAll= True, namespace = ":", op =";;targetTime=3;option=insert;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=/Users/aleclock/Documents/maya/projects/default/data/;")

"""
Define a sequence of animation, in order to reduce the possibility of set the same animation to neighboring elements
Input:
    animList: animation list 
    viewerList: viewer list
Ouput:
    sequence of animation

L'idea è che, nel caso in cui i modelli da animare siano inferiori del numero di animazioni, venga restituita una lista contenente una sequenza ordinata casualmente 
di animazioni uniche (nella lista non ci sono doppioni). In caso contrario le animazioni vengono ripetute il meno possibile.
Questa procedura è perfetta nel caso di pubblico con poche persone, in quanto non ci saranno ripetizioni nelle animazioni
"""
def getAnimationSequence(animList, viewerList):
    if len(viewerList) < len(animList):
        return random.sample(animList, len(viewerList))
    else: 
        anim = []
        while len(anim) < len(viewerList):
            if (len(viewerList) - len(anim)) >= len(animList): 
                anim += random.sample(animList, len(animList))
            else:
                anim += random.sample(animList, len(viewerList) - len(anim))
        return anim

"""
Select animation keys

selectKey -clear ;
selectKey -add -k ikHandle_foot_L_translateX2 ikHandle_hand_L_translateX2 ikHandle_hand_R_translateX2 ikHandle_foot_R_translateX2 ;
keyframe -animation keys -relative -valueChange (0 + 12) ;

Siccome il nome del ikHandle termina con l'indice del viewer meno uno, è necessario determinare l'indice e aggiungerlo alla radice del nome
"""
def translateAnimationKeys(viewer, coord):
    index = int(viewer.find('_'))

    footL = pm.keyframe(viewer + "|ikHandle_foot_L", query = True, name = True)
    footR = pm.keyframe(viewer + "|ikHandle_foot_R", query = True, name = True)
    handL = pm.keyframe(viewer + "|ikHandle_hand_L", query = True, name = True)
    handR = pm.keyframe(viewer + "|ikHandle_hand_R", query = True, name = True)
    head = pm.keyframe(viewer + "|ikHandle_head", query = True, name = True)

    # Nel caso in cui lo stickman sia il primo, ovvero nel caso in cui dopo "_" ci sia solo "1" (i : permettono di discriminare il caso in cui non sia [10, 19])
    if (viewer[index+1:] == "1"):
        name = ""
    else:
        name = str(int(viewer[index+1:]) - 1)

    selectIkHandle(viewer)
    #pm.selectKey("ikHandle_foot_L_translateX" + name, addTo = True, keyframe = True)  # https://download.autodesk.com/global/docs/Maya2012/en_US/PyMel/generated/functions/pymel.core.general/pymel.core.general.selectKey.html
    pm.selectKey(footL[0], addTo = True, keyframe = True)
    pm.selectKey(footR[0], addTo = True, keyframe = True)
    pm.selectKey(handL[0], addTo = True, keyframe = True)
    pm.selectKey(handR[0], addTo = True, keyframe = True)
    pm.selectKey(head[0], addTo = True, keyframe = True)

    pm.keyframe(animation = "keys", relative = True, valueChange = (0+ coord[0])) # https://help.autodesk.com/cloudhelp/2018/JPN/Maya-Tech-Docs/PyMel/generated/functions/pymel.core.animation/pymel.core.animation.keyframe.html https://download.autodesk.com/global/docs/maya2012/en_us/PyMel/generated/functions/pymel.core.animation/pymel.core.animation.keyframe.html

    pm.selectKey(clear = True)
    pm.selectKey(footL[1], addTo = True, keyframe = True)
    pm.selectKey(footR[1], addTo = True, keyframe = True)
    pm.selectKey(handL[1], addTo = True, keyframe = True)
    pm.selectKey(handR[1], addTo = True, keyframe = True)
    pm.selectKey(head[1], addTo = True, keyframe = True)

    pm.keyframe(animation = "keys", relative = True, valueChange = (0+ coord[1]))

    pm.selectKey(clear = True)
    pm.selectKey(footL[2], addTo = True, keyframe = True)
    pm.selectKey(footR[2], addTo = True, keyframe = True)
    pm.selectKey(handL[2], addTo = True, keyframe = True)
    pm.selectKey(handR[2], addTo = True, keyframe = True)
    pm.selectKey(head[2], addTo = True, keyframe = True)

    pm.keyframe(animation = "keys", relative = True, valueChange = (0+ coord[2]))


"""
Calculate stickman center position
Input:
    viewer: stickman
Output:
    list: [coordX, coordY, coordZ]
"""
def getStickmanOrigin(viewer):
    coordLeft = getLeftFootCoord(viewer)
    coordRight = getRightFootCoord(viewer)
    return [(l + r) / 2 for l, r in zip(coordLeft, coordRight)]

"""
pm.getAttr('noseCone.translateX',lock=True)
"""
def getLeftFootCoord(viewer):
    return [pm.getAttr(viewer + "|ikHandle_foot_L.translateX"), pm.getAttr(viewer + "|ikHandle_foot_L.translateY"), pm.getAttr(viewer + "|ikHandle_foot_L.translateZ")]

def getRightFootCoord(viewer):
    return [pm.getAttr(viewer + "|ikHandle_foot_R.translateX"), pm.getAttr(viewer + "|ikHandle_foot_R.translateY"), pm.getAttr(viewer + "|ikHandle_foot_R.translateZ")]