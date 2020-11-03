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
           
    window = cmds.window (title= windowTitle,sizeable=False)

    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    #cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    cmds.formLayout(form,edit= True)

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

    # Callback per il caricamento dei materiali
    def loadMaterialsCallback( *pArgs ):
        #cmds.file("/Users/aleclock/Desktop/uni/ModGraf/src/material/mskinFace.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/pippo.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmHair00_08.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        #cmds.file("//Users/aleclock/Desktop/uni/ModGraf/src/material/SGskinFaceTexture.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmBody_Tee00_07.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmBody_Shirt00_12.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmBody_sweater00_04.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmTrousers_jeans00_03.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmTrousers_standard00_04.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")
        cmds.file("./src/material/SGmTrousers_velvet00_05.mb", type='mayaBinary', i= True, renameAll= True, mergeNamespacesOnClash=True, namespace=":", loadReferenceDepth= "all", importFrameRate= True, importTimeRange="override")


    # Callback per la rimozione dei materiali
    def deleteMaterialsCallback( *pArgs ):
        #TODO eliminare quelli giusti
        deleteElements("faceTexture*")
        deleteElements("mSkin*")
        deleteElements("mSkinFace*")
        deleteElements("mTee*")
        deleteElements("trousers_velvet*")
        deleteElements("place2dTexture*")

    # Callback per l'eliminazione del popup/ui 
    def cancelCallback(*pArgs):
        if cmds.window( window, exists=True ):
            cmds.deleteUI(window, window=True )

    tab_crowdCreation = cmds.rowColumnLayout( numberOfColumns=5, columnWidth=[(1,10),(2, 60), (3, 60), (4, 60),(5,10)] )

    addSeparator(5, 10) # number of separator, height

    cmds.separator(h=10, style="none")
    cmds.text (label = "Materials")
    cmds.button (label = "Load", command= loadMaterialsCallback )
    cmds.button (label = "Delete", command= deleteMaterialsCallback )
    cmds.separator( h=10, style='none' )

    addSeparator(5,2)

    cmds.separator(h=10, style="none")
    cmds.text (label = "Models")
    cmds.button (label = "Load", command= loadModelsCallback )
    cmds.button (label = "Delete", command= deleteModelsCallback )
    cmds.separator( h=10, style='none' )

    cmds.separator( h=10, style='none' )
    cmds.text (label = "Rows:")
    nRowsField = cmds.intField(minValue=1, value=4)
    addSeparator(2, 10)
    
    cmds.separator( h=10, style='none' )
    cmds.text (label = "Seats:")
    nSeatsField = cmds.intField(minValue=10, value=15)
    addSeparator(2, 10)

    addSeparator(5,10)

    addSeparator(2, 10)
    cmds.button (label = "Apply", command = functools.partial ( pApplyCallback,
                                                        nRowsField,
                                                        nSeatsField ))  

    addSeparator(5,10)
    
    cmds.setParent( '..' )

    tab_crowdAnimation = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,100),(2,100)])
    addSeparator(2, 10)
    cmds.text (label = "Wave")
    cmds.button( label='Create', command = animWaveCallback)
    cmds.text (label = "Exulting")
    cmds.button( label='Create', command = animExultanceCallback)
    cmds.setParent( '..' )

    cmds.tabLayout( tabs, edit=True, tabLabel=((tab_crowdCreation, 'Crowd creation'), (tab_crowdAnimation, 'Animation')) )
    cmds.showWindow()

# Callback per la creazione della folla 
def applyCallback(nRowsField, nSeatsField, *pArgs):
    nRows = cmds.intField (nRowsField, query =  True, value = True)
    nSeats = cmds.intField (nSeatsField, query =  True, value = True)
    deleteElements("row_group*")
    #TODO capire perchè elimino i capelli
    deleteElements("hair_*")
    drawModels(nRows, nSeats)

def animWaveCallback(*pArgs):
    print ("wave")


def animExultanceCallback(*pArgs):
    viewer_list = cmds.ls("viewer*")
    fileType = "atom"
    anim_folder  = r"./src/animation"
    animList = cmds.getFileList(folder = anim_folder, filespec = "*.%s" % fileType) # list of animation files 

    for v in viewer_list:
        coord = getLeftFootCoord(v)
        setAnimation(v, anim_folder + "/" + str(getRandomElement(animList)))
        translateAnimationKeys(v, coord)

# Funzione che importa i vari modelli
# TODO capire perchè salvo i modelli nella lista transform
def importModels(model, folder, ns):    # ns: namespace
    transforms = []

    for item in model:
        fname = os.path.join(folder, item)
        objName, ext = os.path.splitext(os.path.basename(fname))
        # import each file
        imported_objects = cmds.file(fname, i=True, rnn=True, mergeNamespacesOnClash =False, namespace=ns, loadReferenceDepth='all', importFrameRate=True, type='mayaBinary') 
        transforms.append (cmds.ls(imported_objects, type='transform'))

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

            hairName = getRandomElement(hairList)
            hair = cmds.duplicate (hairName, name = "hair#") [0]
            cmds.parent(hair, rowGroup + ' | ' + body)
            cmds.select (rowGroup + ' | ' + body + '|body|head|hair')
            cmds.select (rowGroup + ' | ' + body + '|' + hair ,add = True)
            pm.runtime.ReplaceObjects(scale = False)

            mHair = cmds.ls("SGmHair*")
            mHair = getRandomElement(mHair)
            setMaterial(rowGroup + ' | ' + body + '|body|head|hair*' ,mHair)

            #rigReference = 'viewer_' + str(count+1) + "|QuickRigCharacter_Ctrl_Reference"
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
    print (anim_name)
    selectIkHandle(viewer)
    cmds.file(anim_name, type = "atomImport" , i= True, renameAll= True, namespace = ":", op =";;targetTime=3;option=insert;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=/Users/aleclock/Documents/maya/projects/default/data/;")

"""
Select animation keys

selectKey -clear ;
selectKey -add -k ikHandle_foot_L_translateX2 ikHandle_hand_L_translateX2 ikHandle_hand_R_translateX2 ikHandle_foot_R_translateX2 ;
keyframe -animation keys -relative -valueChange (0 + 12) ;

Siccome il nome del ikHandle termina con l'indice del viewer meno uno, è necessario determinare l'indice e aggiungerlo alla radice del nome
"""
def translateAnimationKeys(viewer, coord):
    index = int(viewer.find('_'))

    if (viewer[index+1:] == "1"):
        name = ""
    else:
        name = str(int(viewer[index+1:]) - 1)

    selectIkHandle(viewer)
    pm.selectKey("ikHandle_foot_L_translateX" + name, addTo = True, keyframe = True)  # https://download.autodesk.com/global/docs/Maya2012/en_US/PyMel/generated/functions/pymel.core.general/pymel.core.general.selectKey.html
    pm.selectKey("ikHandle_foot_R_translateX" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_hand_L_translateX" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_hand_R_translateX" + name, addTo = True, keyframe = True)
    #pm.selectKey("ikHandle_head_translateX" + name, addTo = True, keyframe = True)

    pm.keyframe(animation = "keys", relative = True, valueChange = (0+ coord[0])) # https://help.autodesk.com/cloudhelp/2018/JPN/Maya-Tech-Docs/PyMel/generated/functions/pymel.core.animation/pymel.core.animation.keyframe.html https://download.autodesk.com/global/docs/maya2012/en_us/PyMel/generated/functions/pymel.core.animation/pymel.core.animation.keyframe.html

    pm.selectKey(clear = True)
    pm.selectKey("ikHandle_foot_L_translateY" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_foot_R_translateY" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_hand_L_translateY" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_hand_R_translateY" + name, addTo = True, keyframe = True)

    pm.keyframe(animation = "keys", relative = True, valueChange = (0+ coord[1]))

    pm.selectKey(clear = True)
    pm.selectKey("ikHandle_foot_L_translateZ" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_foot_R_translateZ" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_hand_L_translateZ" + name, addTo = True, keyframe = True)
    pm.selectKey("ikHandle_hand_R_translateZ" + name, addTo = True, keyframe = True)

    pm.keyframe(animation = "keys", relative = True, valueChange = (0+ coord[2]))

    # TODO traslare anche la testa (mancano i keyframes nell'animazione)
    # TODO magar provare a traslare rispetto alla media tra la posizione del piede sinistro e destro


"""
pm.getAttr('noseCone.translateX',lock=True)
"""
def getLeftFootCoord(viewer):
    return [pm.getAttr(viewer + "|ikHandle_foot_L.translateX"), pm.getAttr(viewer + "|ikHandle_foot_L.translateY"), pm.getAttr(viewer + "|ikHandle_foot_L.translateZ")]