import maya.cmds as cmds
import os 
import functools
import random
import pymel.core as pm

os.chdir("/Users/aleclock/Desktop/uni/ModGraf")
# TODO sostituire i vari percorsi con una variabile per rendere il tutto più modificabile

# ----------------------------------------------------------------------------------------------------------------
# Funzione per la creazione dell'interfaccia grafica
# ----------------------------------------------------------------------------------------------------------------

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
        
        # Prima di importare i modelli elimina quelli già presenti
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

    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")

    cmds.separator(h=10, style="none")
    cmds.text (label = "Materials")
    cmds.button (label = "Load", command= loadMaterialsCallback )
    cmds.button (label = "Delete", command= deleteMaterialsCallback )
    cmds.separator( h=10, style='none' )

    cmds.separator(h=2, style="none")
    cmds.separator(h=2, style="none")
    cmds.separator(h=2, style="none")
    cmds.separator(h=2, style="none")
    cmds.separator(h=2, style="none")

    cmds.separator(h=10, style="none")
    cmds.text (label = "Models")
    cmds.button (label = "Load", command= loadModelsCallback )
    cmds.button (label = "Delete", command= deleteModelsCallback )
    cmds.separator( h=10, style='none' )

    cmds.separator( h=10, style='none' )
    cmds.text (label = "Rows:")
    nRowsField = cmds.intField(minValue=1, value=4)
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    
    cmds.separator( h=10, style='none' )
    cmds.text (label = "Seats:")
    nSeatsField = cmds.intField(minValue=10, value=15)
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )

    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")

    cmds.separator( h=10, style='none' )
    cmds.separator(h=10, style="none")
    cmds.button (label = "Apply", command = functools.partial ( pApplyCallback,
                                                        nRowsField,
                                                        nSeatsField ))  

    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    cmds.separator(h=10, style="none")
    
    cmds.setParent( '..' )


    tab_crowdAnimation = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,100),(2,100)])
    cmds.separator(h=10, style="none")  
    cmds.separator(h=10, style="none")  
    cmds.text (label = "Wave")
    cmds.button( label='Create', command=cancelCallback)
    cmds.text (label = "Exulting")
    cmds.button( label='Create', command=cancelCallback)
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

# Funzione che importa i vari modelli
def importModels(model, folder, ns):    # ns: namespace
    transforms = []

    for item in model:
        fname = os.path.join(folder, item)
        objName, ext = os.path.splitext(os.path.basename(fname))
        # import each file
        imported_objects = cmds.file(fname, i=True, rnn=True, mergeNamespacesOnClash =False, namespace=ns, loadReferenceDepth='all', importFrameRate=True, type='mayaBinary') 
        transforms.append (cmds.ls(imported_objects, type='transform'))

# Funzione che elimina elementi/oggetti se presenti
def deleteElements(el):
    bodyList = cmds.ls(el)
    if len(bodyList)>0:
        cmds.delete(bodyList)

# Funzione che elimina materiali se già esistenti
def deleteMaterials():
    skinList = cmds.ls("skin*")
    if len(skinList)>0:
        cmds.delete(skinList)
        skinList = []

createUI("Crowd generator", applyCallback)

def drawModels (nRows, nSeats):

    bodyList = cmds.ls("*:person")
    bodyName = bodyList[0] # Prende il primo elemento della lista transforms e il primo elemento dell'elemento

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

            rigReference = 'viewer_' + str(count+1) + "|QuickRigCharacter_Ctrl_Reference"

            # TODO il rig reference è formato da queste cose qua sotto
            """select -r joint_COG ;
            select -r joint_COG ikHandle_foot_L ;
            select -r joint_COG ikHandle_foot_L ikHandle_hand_L ;
            select -r joint_COG ikHandle_foot_L ikHandle_hand_L ikHandle_hand_R ;
            select -r joint_COG ikHandle_foot_L ikHandle_hand_L ikHandle_hand_R ikHandle_head ;
            select -r joint_COG ikHandle_foot_L ikHandle_hand_L ikHandle_hand_R ikHandle_head ikHandle_foot_R ;
            select -add hair2 ;
            doCreateParentConstraintArgList 1 { "1","0","0","0","0","0","0","0","1","","1" };
            parentConstraint -mo -weight 1
            """

            # TODO dopo aver selezionaro il rif reference è necessario selezionare hari* e fare parentConstraint

            cmds.parentConstraint (rigReference, rowGroup + ' | ' + body + '|body|head|hair*', maintainOffset = True, weight = True)

            # Viene selezionato il Rig in quanto selezionando il gruppo lo spostamento viene male
            cmds.select(rigReference, visible= True)

            x = random.uniform(-0.5, 0.5) + (6 * j)
            y = 3 * i
            z = random.uniform(-0.5, 0.5) + (-3 * i)
            
            cmds.move(x,y,z) 
            
            count = count + 1
        cmds.xform(rowGroup,centerPivots=True)
    
    # Nasconde i modelli
    cmds.hide('models')

def getRandomElement(sequence):
    return random.choice(sequence)

# Funzione utile a settare i materiali
def setMaterial(path, material):
    cmds.select(path, r= True) # Selezione della testa del personaggio corrente
    cmds.sets(e=1, forceElement= material)

# Funzione per fare l'uv mapping del mSkinFace
def uvMapskinFace(rowGroup, body):
    #cmds.hilite(cube)
    cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head.f[0:71]', constructionHistory=True)
    #cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head.f[0:71]', constructionHistory=True)
    cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head.f[73:293]', constructionHistory=True)
    cmds.polyMapDel(rowGroup + ' | ' + body + '|body|head|hair.f[0:25]', constructionHistory=True)
    cmds.select(rowGroup + ' | ' + body + '|body|head.f[72]', r= True)
    cmds.polyEditUV( uValue=0, vValue=0.34) 
    cmds.setAttr (rowGroup + ' | ' + body + '|body|head|headShape.uvPivot',0.5, 0.45, type='double2')
    cmds.polyEditUV(pivotU = 0.5, pivotV = 0.45, scaleU=3.5, scaleV=3.5)