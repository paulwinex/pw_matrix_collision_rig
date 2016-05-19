import maya.cmds as cmds
from functools import partial

############################################# NAMES
n_sideNaming={'left':'LFT',
              'right':'RGT',
              'center':'CNTR',
              'lower':'LWR',
              'upper':'UPR',
              '':''}
#objects
n_mainGroupName = 'collisionSetupGrp'
n_collisionSetupGrp = 'setupGrp'
n_collisionPlane = 'collisionPlane'
n_collisionSphere = 'collisionSphere'
n_collisionCurve = 'control'
n_bindOrientLocator = 'bindOrientLocator'
n_aimPoint = 'upVectorObject'
n_affectedObject = 'collidedObject'
n_collisionPoint = 'collPnt'
#n_collidedLocator = 'CollidedLocator'
#util nodes
n_closestPointNode = 'cpo'
n_decomposeMatrix = 'dcm'
n_vectorProductNode = 'vcp'
n_fourByFourMatrix = 'fbfm'
n_distanceBetweenNode = 'dtw'
n_multipleDivide = 'mdv'
#n_constraint = 'constraint'
n_setRange = 'sr'
n_reverse = 'rev'
n_plusMinusAverageName = 'pma'
n_multMatrix = 'mlm'
n_conditionNode = 'cnd'
n_pairBlendNode = 'prb'
n_blendCurve ='crv'

############################################# VALUES
v_collisionPlaneRadius = 2
v_mainUpVector = (0,0,1)
baseSize = 1.0
collPointScale = 0.5
aimObjectPoints = [(0.0, 1.0, 0.0), (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
collisionPointColor = 17 #yellow
upObjectColor = 13       #red
affectedObjectColor = 18 #light blue
softPointCOlor = 5       #blue
############################################# ATTRIBS
n_collisionDistanceAttr = 'collisionDistance'
n_softCollisionDistanceAttr = 'softCollisionDistance'
n_mainBlendAttr = 'collisionBlend'
n_VisAttr='controlVisibility'
####################################################
plugins = ['matrixNodes']

class matrixCollisionMaker():
    def __init__(self):
        self.winName = 'pw_matrixCollisonUI'
        if cmds.window(self.winName, q=1, ex=1):
            cmds.deleteUI(self.winName)
        self.buildUi()
        self.element=''

    def showUi(self):
        cmds.showWindow(self.wind)

    def buildUi(self):
        self.wind = cmds.window(self.winName,
                                title='Matrix collision setup | PaulWinex | v2.0',
                                widthHeight=[390,270])
        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout( label='Naming' )
        self.elementName = cmds.textFieldGrp(label='Element Name')
        self.sideNameMenu = cmds.optionMenuGrp( label='Side',columnWidth=(2, 180) )
        for k in '','center','left','right','lower','upper':
            cmds.menuItem( label=k )
        cmds.setParent( '..' )

        cmds.frameLayout( label='Orient collision plane to' )
        cmds.rowLayout( numberOfColumns=4)
        cmds.columnLayout()
        collection1 = cmds.radioCollection()
        self.rbMeshNormal = cmds.radioButton( label='Mesh Normal', sl=1 )
        self.rbRigControl = cmds.radioButton( label='Rig Control' )
        cmds.setParent( '..' )

        cmds.columnLayout()
        self.fromCamera = cmds.radioButton( label='From Camera' )
        self.ontocamera = cmds.radioButton( label='Onto Camera' )
        cmds.setParent( '..' )

        cmds.columnLayout()
        self.rbX = cmds.radioButton( label='X' )
        self.rbY = cmds.radioButton( label='Y' )
        self.rbZ = cmds.radioButton( label='Z' )
        cmds.setParent( '..' )

        cmds.columnLayout()
        self.rbXn = cmds.radioButton( label='-X' )
        self.rbYn = cmds.radioButton( label='-Y' )
        self.rbZn = cmds.radioButton( label='-Z' )
        cmds.setParent( '..' )

        cmds.setParent( '..' )

        cmds.frameLayout( label='Source Objects' )
        cmds.rowLayout( numberOfColumns=3, columnWidth3=(90, 75, 40), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )
        cmds.text('Rig Control')
        self.text2 = cmds.textField(editable=0)
        self.set2 = cmds.button(label='set', c=partial(self.setObject,2))
        cmds.setParent('..')
        cmds.rowLayout( numberOfColumns=3, columnWidth3=(90, 75, 40), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )
        cmds.text('Collision Mesh')
        self.text3 = cmds.textField(editable=0)
        self.set3 = cmds.button(label='set', c=partial(self.setObject,3))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.columnLayout(adjustableColumn=True)
        self.export = cmds.button(label='Do setup', c=self.doSetup)

    def setObject(self, i, tmp):
        sel = cmds.ls(sl=1, l=1)
        if sel:
            obj = sel[0]
            if i == 2:
                if cmds.nodeType(obj) == 'transform':
                    cmds.textField(self.text2, e=1, text = obj)
                    if cmds.textField(self.text3, q=1, text=1) == obj:
                        cmds.textField(self.text3, e=1, text = '')
            elif i == 3: #mesh
                if cmds.nodeType(obj) == 'transform':
                    sh = cmds.listRelatives(obj, s=1)
                    if sh:
                        sh = sh[0]
                        if cmds.nodeType(sh) == 'mesh':
                            cmds.textField(self.text3, e=1, text = obj)
                            if cmds.textField(self.text2, q=1, text=1) == obj:
                                cmds.textField(self.text2, e=1, text = '')

    def setAttr(self, node, attr, *value):
        cmds.setAttr('.'.join([node,attr]), *value)

    def connect(self, node1, attr1, node2, attr2):
        cmds.connectAttr('.'.join([node1,attr1]),
                         '.'.join([node2, attr2]),
                         f=1)

    def lock(self, object, *attrs):
        for a in attrs:
            if a == 't':
                for atr in ['tx','ty','tz']:
                    cmds.setAttr('.'.join([object, atr]),lock=True)
            elif a == 'r':
                for atr in ['rx','ry','rz']:
                    cmds.setAttr('.'.join([object, atr]),lock=True)
            elif a == 's':
                for atr in ['sx','sy','sz']:
                    cmds.setAttr('.'.join([object, atr]),lock=True)

    def doSetup(self, tmp):
        self.loadPlugins()
        control = cmds.textField(self.text2, q=1, text=1)
        if not control:
            cmds.warning('Not enough control!!!')
        collision = cmds.textField(self.text3, q=1, text=1)
        if not collision:
            cmds.warning('Not enough collision!!!')

        if cmds.objExists(control):
            if cmds.objExists(collision):
                #element name
                self.element = cmds.textFieldGrp(self.elementName, q=1, tx=1)
                if not self.element:
                    cmds.confirmDialog( title='Error',
                                        message='Object name not set!!!',
                                        button=['Ok'],
                                        defaultButton='Ok',
                                        icon='critical')
                    return

                #side
                self.sideName = n_sideNaming[cmds.optionMenuGrp(self.sideNameMenu, q=1, v=1)]
                #default orient
                if cmds.radioButton(self.rbMeshNormal, q=1, sl=1):
                    orient = 1
                elif cmds.radioButton(self.rbRigControl, q=1, sl=1):
                    orient = 2
                elif cmds.radioButton(self.fromCamera, q=1, sl=1):
                    orient = 3
                elif cmds.radioButton(self.ontocamera, q=1, sl=1):
                    orient = 4
                elif cmds.radioButton(self.rbX, q=1, sl=1):
                    orient = 5
                elif cmds.radioButton(self.rbY, q=1, sl=1):
                    orient = 6
                elif cmds.radioButton(self.rbZ, q=1, sl=1):
                    orient = 7
                elif cmds.radioButton(self.rbXn, q=1, sl=1):
                    orient = 8
                elif cmds.radioButton(self.rbYn, q=1, sl=1):
                    orient = 9
                else:
                    orient = 10


                self.buildSetup(control, collision, orient)
            else:
                cmds.confirmDialog( title='Error',
                                        message='Collision object not found!!!',
                                        button=['Ok'],
                                        defaultButton='Ok',
                                        icon='critical')
                return
                #cmds.warning('Collision obj not found')
        else:
            cmds.confirmDialog( title='Error',
                                        message='Control object not found!!!',
                                        button=['Ok'],
                                        defaultButton='Ok',
                                        icon='critical')
            return
            #cmds.warning('Control obj not found')

    def getOrientRigControl(self, control):
        pass

    def getOrientCamera(self, fromCam=True):
        pass

    def buildSetup(self,control, collision, orient):
        #attribs
        self.addControlAttribs(control)
        #main grps
        mainGrp = cmds.createNode('transform', name=self.getName(n_mainGroupName), ss=1) #MAIN GRP
        mainSetupGrp = cmds.createNode('transform', name=self.getName(n_collisionSetupGrp), ss=1) #MAIN SETUP GRP
        collisionPlane = self.createCollisionPlaneGuide(self.getName(n_collisionPlane))
        bindOrientLocator = cmds.spaceLocator(name=self.getName(n_bindOrientLocator))[0]    #Bind orient locator
        affectedObject = self.createAffectedObject(name=self.getName(n_affectedObject))
        #collidedLocator = cmds.spaceLocator(name=self.getName(n_collidedLocator))[0]
        cmds.parent(bindOrientLocator, collisionPlane, mainSetupGrp)
        cmds.parent(mainSetupGrp, affectedObject, mainGrp)
        self.setAttr(cmds.listRelatives(bindOrientLocator, s=1)[0], 'visibility', 0)

        #aim point
        aimPoint = self.createAimObject(self.getName(n_aimPoint))
        cmds.parent(aimPoint, affectedObject, r=1)
        cmds.xform(aimPoint, t=[0,1,0])

        #closest point
        closest = cmds.createNode('closestPointOnMesh', name = self.getName(n_closestPointNode), ss=1)
        colShape = cmds.listRelatives(collision, s=1)[0]
        self.connect(colShape,'outMesh', closest, 'inMesh')
        self.connect(collision,'worldMatrix[0]', closest, 'inputMatrix')

        decomp1 = cmds.createNode('decomposeMatrix', name=self.getName(n_decomposeMatrix), ss=1)
        self.connect(collisionPlane,'worldMatrix[0]',
                     decomp1, 'inputMatrix')
        self.connect(decomp1,'outputTranslate',
                     closest, 'inPosition')

        #products
        prod1 = cmds.createNode('vectorProduct', name=self.getName(n_vectorProductNode), ss=1)
        self.setAttr(prod1,'operation', 3)
        self.setAttr(prod1,'normalizeOutput', 1)
        self.setAttr(prod1,'input1', v_mainUpVector[0],v_mainUpVector[1],v_mainUpVector[2])
        self.connect(collisionPlane,'worldMatrix[0]',
                     prod1, 'matrix')
        #
        prod2 = cmds.createNode('vectorProduct', name=self.getName(n_vectorProductNode), ss=1)
        self.setAttr(prod2,'operation', 3)
        self.setAttr(prod2,'normalizeOutput', 1)
        self.connect(prod1,'output',
                     prod2, 'input1')
        self.connect(closest,'normal',
                     prod2, 'input2')
        #
        prod3 = cmds.createNode('vectorProduct', name=self.getName(n_vectorProductNode), ss=1)
        self.setAttr(prod3,'operation', 2)
        self.setAttr(prod3,'normalizeOutput', 1)
        self.connect(prod2,'output',
                     prod3, 'input2')
        self.connect(closest,'normal',
                     prod3, 'input1')
        #4x4 matrix
        m4x41 = cmds.createNode('fourByFourMatrix', name=self.getName(n_fourByFourMatrix), ss=1)
        self.connect(prod3,'outputX', m4x41, 'in00')
        self.connect(prod3,'outputY', m4x41, 'in01')
        self.connect(prod3,'outputZ', m4x41, 'in02')
        self.connect(prod2,'outputX', m4x41, 'in20')
        self.connect(prod2,'outputY', m4x41, 'in21')
        self.connect(prod2,'outputZ', m4x41, 'in22')
        self.connect(closest,'normalX', m4x41, 'in10')
        self.connect(closest,'normalY', m4x41, 'in11')
        self.connect(closest,'normalZ', m4x41, 'in12')
        self.connect(closest,'positionX', m4x41, 'in30')
        self.connect(closest,'positionY', m4x41, 'in31')
        self.connect(closest,'positionZ', m4x41, 'in32')

        #4x4 matrix
        m4x42 = cmds.createNode('fourByFourMatrix', name=self.getName(n_fourByFourMatrix), ss=1)
        self.connect(closest,'positionX', m4x42, 'in30')
        self.connect(closest,'positionY', m4x42, 'in31')
        self.connect(closest,'positionZ', m4x42, 'in32')
        #
        #distance
        dist = cmds.createNode('distanceBetween', name=self.getName(n_distanceBetweenNode), ss=1)
        self.connect(m4x42,'output', dist, 'inMatrix2')
        self.connect(collisionPlane,'worldMatrix[0]', dist, 'inMatrix1')
        #plusmunus
        plus1 = cmds.createNode('plusMinusAverage', name=self.getName(n_plusMinusAverageName), ss=1)
        self.setAttr(plus1,'operation', 1)
        self.connect(control,n_collisionDistanceAttr,
                     plus1, 'input1D[0]')
        self.connect(control,n_softCollisionDistanceAttr,
                     plus1, 'input1D[1]')
        #soft range
        rng1 = cmds.createNode('setRange', name=self.getName(n_setRange), ss=1)
        self.setAttr(rng1, 'minX', 0)
        self.setAttr(rng1, 'maxX', 1)
        self.connect(plus1, 'output1D', rng1, 'oldMaxX')
        self.connect(control, n_collisionDistanceAttr, rng1, 'oldMinX')
        self.connect(dist, 'distance', rng1, 'valueX')

        rng2 = cmds.createNode('setRange', name=self.getName(n_setRange), ss=1)
        self.setAttr(rng2, 'minX', 0)
        self.setAttr(rng2, 'maxX', 1)
        self.connect(dist, 'distance', rng2, 'valueX')
        self.connect(control, n_collisionDistanceAttr, rng2, 'oldMaxX')

        plus2 = cmds.createNode('plusMinusAverage', name=self.getName(n_plusMinusAverageName), ss=1)
        self.setAttr(plus2,'operation', 2)
        self.connect(decomp1, 'outputTranslate',
                     plus2, 'input3D[0]')
        self.connect(closest, 'position',
                     plus2, 'input3D[1]')

        prod4 = cmds.createNode('vectorProduct', name=self.getName(n_vectorProductNode), ss=1)
        self.setAttr(prod4,'operation', 1)
        self.setAttr(prod4,'normalizeOutput', 1)
        self.connect(plus2,'output3D',
                     prod4, 'input1')
        self.connect(closest, 'normal',
                     prod4, 'input2')

        cond1 = cmds.createNode('condition', name=self.getName(n_conditionNode), ss=1)
        self.setAttr(cond1, 'secondTerm', 0)
        self.setAttr(cond1, 'operation', 2)
        self.setAttr(cond1, 'colorIfTrue', 1,0,0)
        self.setAttr(cond1, 'colorIfFalse', 0,1,1)
        self.connect(prod4, 'outputX', cond1, 'firstTerm')

        mult1 = cmds.createNode('multiplyDivide', name=self.getName(n_multipleDivide), ss=1)
        mult2 = cmds.createNode('multiplyDivide', name=self.getName(n_multipleDivide), ss=1)
        self.connect(rng1,'outValueX',
                     mult1, 'input1X')
        self.connect(cond1, 'outColorR',
                     mult1, 'input2X')
        self.connect(rng2,'outValueX',
                     mult2, 'input1X')
        self.connect(cond1, 'outColorR',
                     mult2, 'input2X')

        rev1 = cmds.createNode('reverse', name= self.getName(n_reverse), ss=1)
        rev2 = cmds.createNode('reverse', name= self.getName(n_reverse), ss=1 )
        self.connect(mult1,'outputX',
                     rev1, 'inputX')
        self.connect(mult2,'outputX',
                     rev2, 'inputX')

        mult3 = cmds.createNode('multiplyDivide', name=self.getName(n_multipleDivide), ss=1)
        self.connect(closest, 'normal',
                     mult3, 'input1')
        for a in 'X', 'Y', 'Z':
            self.connect(control, n_collisionDistanceAttr,
                         mult3, 'input2%s' % a)

        plus3 = cmds.createNode('plusMinusAverage', name=self.getName(n_plusMinusAverageName), ss=1) #OUT POS
        self.setAttr(plus3,'operation', 1)
        self.connect(mult3, 'output',
                     plus3, 'input3D[1]')
        self.connect(closest, 'position',
                     plus3, 'input3D[0]')


        #multMatrix
        multMx1 = cmds.createNode('multMatrix', name=self.getName(n_multMatrix), ss=1)
        multMx2 = cmds.createNode('multMatrix', name=self.getName(n_multMatrix), ss=1)
        self.connect(bindOrientLocator,'worldInverseMatrix[0]',
                     multMx1, 'matrixIn[1]')
        self.connect(m4x41,'output', multMx1,
                     'matrixIn[0]')
        self.connect(mainSetupGrp,'worldMatrix[0]',
                     multMx2, 'matrixIn[1]')
        self.connect(multMx1,'matrixSum',
                     multMx2, 'matrixIn[0]')

        decomp2 = cmds.createNode('decomposeMatrix', name=self.getName(n_decomposeMatrix), ss=1)
        self.connect(multMx2, 'matrixSum', decomp2, 'inputMatrix')

        #constr = cmds.parentConstraint(control, collidedLocator, mo=0, w=1)#, name=self.getName(n_constraint))[0]

        decomp3 = cmds.createNode('decomposeMatrix', name=self.getName(n_decomposeMatrix), ss=1)
        self.connect(mainSetupGrp, 'worldMatrix[0]', decomp3, 'inputMatrix')


        #blend curves
        blendCurveRotate = self.createRotateBlendCurve(self.getName(n_blendCurve))
        self.connect(rev1, 'outputX',
                     blendCurveRotate, 'input')
        blendCurveTranslate = self.createTranslateBlendCurve(self.getName(n_blendCurve))
        self.connect(rev2, 'outputX',
                     blendCurveTranslate, 'input')

        #pair blends
        pairRotate = cmds.createNode('pairBlend', name=self.getName(n_pairBlendNode), ss=1)
        pairTranslate = cmds.createNode('pairBlend', name=self.getName(n_pairBlendNode), ss=1)
        pairMain = cmds.createNode('pairBlend', name=self.getName(n_pairBlendNode), ss=1)

        self.connect(decomp1, 'outputRotate', pairRotate, 'inRotate1')
        self.connect(decomp2, 'outputRotate', pairRotate, 'inRotate2')
        self.connect(blendCurveRotate, 'output', pairRotate, 'weight')

        self.connect(decomp1, 'outputTranslate', pairTranslate, 'inTranslate1')
        self.connect(plus3, 'output3D', pairTranslate, 'inTranslate2')
        self.connect(blendCurveTranslate, 'output', pairTranslate, 'weight')

        self.connect(pairRotate, 'outRotate', pairMain, 'inRotate2')
        self.connect(pairTranslate, 'outTranslate', pairMain, 'inTranslate2')
        self.connect(decomp3, 'outputRotate', pairMain, 'inRotate1')
        self.connect(decomp3, 'outputTranslate', pairMain, 'inTranslate1')
        self.connect(control, n_mainBlendAttr, pairMain, 'weight')

        #self.connect(control, n_VisAttr, collisionPoint, 'visibility')

        #pos
        cmds.delete(cmds.pointConstraint(control, mainSetupGrp, mo=0, weight=1))


        #afected object
        self.connect(pairMain, 'outTranslate',
                     affectedObject, 'translate')
        self.connect(pairMain, 'outRotate',
                     affectedObject, 'rotate')

        #collision guide
        sphereGeo, sphereProc = self.createCollisionSphereGuide(self.getName(n_collisionSphere))
        self.connect(pairRotate, 'outRotate',
                     sphereGeo, 'rotate')
        self.connect(pairTranslate, 'outTranslate',
                     sphereGeo, 'translate')
        self.connect(control, n_collisionDistanceAttr,
                         sphereProc, 'radius')
        self.connect(control, n_VisAttr,
                     sphereGeo,'visibility')
        cmds.parent(sphereGeo, mainGrp)

        #orient before constraint
        if orient == 1: #mesh normal
            pos = cmds.getAttr(closest+'.position')[0]
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, -1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)

        elif orient == 2: #rig control
            R = cmds.xform(control, q=1, ro=1, ws=1)
            print R
            cmds.xform(mainSetupGrp, ro=R, ws=1)

        elif orient == 3: #from camera
            cam = cmds.lookThru( q=True )
            cmds.delete(cmds.aimConstraint(cam, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, -1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,]))

        elif orient == 4: #onto camera
            cam = cmds.lookThru( q=True )
            cmds.delete(cmds.aimConstraint(cam, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,]))
        elif orient == 5: #X axis
            pos = cmds.xform(mainSetupGrp, q=1, t=1, ws=1)
            pos[0] += 2
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)
        elif orient == 6: #Y axis
            pos = cmds.xform(mainSetupGrp, q=1, t=1, ws=1)
            pos[1] += 2
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)
        elif orient == 7: #Z axis
            pos = cmds.xform(mainSetupGrp, q=1, t=1, ws=1)
            pos[2] += 2
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)
        elif orient == 8: #-X axis
            pos = cmds.xform(mainSetupGrp, q=1, t=1, ws=1)
            pos[0] -= 2
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)
        elif orient == 9: #-Y axis
            pos = cmds.xform(mainSetupGrp, q=1, t=1, ws=1)
            pos[1] -= 2
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)
        elif orient == 10: #-Z axis
            pos = cmds.xform(mainSetupGrp, q=1, t=1, ws=1)
            pos[2] -= 2
            aimLoc = cmds.spaceLocator()[0]
            cmds.xform(aimLoc, t=pos)
            aim = cmds.aimConstraint(aimLoc, mainSetupGrp,
                                     weight=1,
                                     aimVector=[0, 1, 0],
                                     upVector=[0, 1, 0],
                                     worldUpType="vector",
                                     worldUpVector=[0, 1, 0,])
            cmds.delete(aim)
            cmds.delete(aimLoc)



        #constrain to control
        cmds.parentConstraint(control, mainSetupGrp, mo=1)


        #lock
        self.lock(aimPoint, 't', 's', 'r')
        self.lock(affectedObject, 't', 'r')
        self.lock(collisionPlane, 't')

        #colorize
        self.setAttr(collisionPlane,'overrideEnabled', 1)
        self.setAttr(collisionPlane,'overrideColor', collisionPointColor)
        ##
        self.setAttr(affectedObject,'overrideEnabled', 1)
        self.setAttr(affectedObject,'overrideColor', affectedObjectColor)
        #
        self.setAttr(aimPoint,'overrideEnabled', 1)
        self.setAttr(aimPoint,'overrideColor', upObjectColor)

        #control visibility
        self.connect(control, n_VisAttr,
                     mainSetupGrp,'visibility')
        self.connect(control, n_VisAttr,
                     aimPoint,'visibility')


        #finish
        cmds.select(control)



    def createCollisionPlaneGuide(self, name):
        collisionPlane = cmds.curve(d=1, name=name,
                                    p=collisionPlanePoints)
        return collisionPlane

    def createCollisionSphereGuide(self, name):
        shpere = cmds.polySphere(name=n_collisionSphere, sx=6, sy=6)
        cmds.polyColorPerVertex(shpere[0],  rgb=(0.75,0.75,0))
        cmds.polyColorPerVertex(shpere[0], colorDisplayOption=1)
        self.setAttr(shpere[0],'overrideEnabled', 1)
        self.setAttr(shpere[0],'overrideDisplayType', 2)
        return shpere

    def createAffectedObject(self, name):
        #return cmds.circle(ch=0, r=v_collisionPlaneRadius,nr=[0,1,0], s=8, name = name)[0]
        crv = cmds.curve( per=True, d=1, p=affectedObjectPoints, name=self.getName(n_collisionCurve) )
        return crv

    def createAimObject(self, name):
        aimPoint = cmds.curve(d=1, name=name,
                                    p=aimObjectPoints)
        return aimPoint

    def addControlAttribs(self, node):
        if not cmds.attributeQuery(n_mainBlendAttr, ex=True, n=node):
            cmds.addAttr(node, ln=n_mainBlendAttr, at='double',  min=0, max=1, dv=1)
            cmds.setAttr('.'.join([node, n_mainBlendAttr]), e=1, keyable=1)

        if not cmds.attributeQuery(n_collisionDistanceAttr, ex=True, n=node):
            cmds.addAttr(node, ln=n_collisionDistanceAttr, at='double',  min=0, smx=3, dv=1)
            cmds.setAttr('.'.join([node, n_collisionDistanceAttr]), e=1, keyable=1)

        if not cmds.attributeQuery(n_softCollisionDistanceAttr, ex=True, n=node):
            cmds.addAttr(node, ln=n_softCollisionDistanceAttr, at='double',  min=0.01, smx=3, dv=1)
            cmds.setAttr('.'.join([node, n_softCollisionDistanceAttr]), e=1, keyable=1)

        if not cmds.attributeQuery(n_VisAttr, ex=True, n=node):
            #cmds.addAttr(node, ln=n_VisAttr,  at='bool')
            cmds.addAttr(node,ln=n_VisAttr, at="enum", en="Off:On:")
            cmds.setAttr('.'.join([node, n_VisAttr]), e=1, keyable=1)
        cmds.setAttr('.'.join([node, n_VisAttr]), 0)

    def createAnimCurve(self, name):
        curve = cmds.createNode('animCurveUU', name=name, ss=1)
        cmds.setKeyframe(curve, f=0,v=0)
        cmds.setKeyframe(curve, f=1,v=1)
        cmds.keyTangent(curve, edit=True, weightedTangents=True)
        return curve

    def createTranslateBlendCurve(self, name):
        blendCurve = self.createAnimCurve(name)
        cmds.keyTangent(blendCurve, index=(0,1), weightLock=0)
        cmds.keyTangent(blendCurve , edit=True, absolute=True, index=(0,0), outAngle=90, outWeight=1)
        cmds.keyTangent(blendCurve , edit=True, absolute=True, index=(1,1), inAngle=0, inWeight=25 )
        return blendCurve

    def createRotateBlendCurve(self, name):
        blendCurve = self.createAnimCurve(name)
        cmds.keyTangent(blendCurve, itt='flat', ott='flat')
        return blendCurve

    def getName(self, name):
        i = 1
        newName = self.element + str(i) + self.sideName+'_'+name
        while cmds.ls(newName):
            i += 1
            newName = self.element + str(i) + self.sideName+'_'+name
        return newName

    def loadPlugins(self):
        for plg in plugins:
            if not cmds.pluginInfo( plg, query=True, loaded=True):
                try:
                    cmds.loadPlugin(plg)
                except:
                    cmds.warning('Plugin %s NOT FOUND', plg)

def show():
    ui = matrixCollisionMaker()
    ui.showUi()


collisionPlanePoints = [[-0.0,    0.0,   -1.0],
                        [-0.192,  0.158, -0.965],
                        [-0.547,  0.158, -0.818],
                        [-0.707,  0.0,   -0.707],
                        [-0.818,  0.158, -0.547],
                        [-0.965,  0.158, -0.192],
                        [-1.0,    0.0,    0.0],
                        [-0.965,  0.158,  0.192],
                        [-0.818,  0.158,  0.547],
                        [-0.707,  0.0,    0.707],
                        [-0.547,  0.158,  0.818],
                        [-0.192,  0.158,  0.965],
                        [ 0.0,    0.0,    1.0],
                        [ 0.192,  0.158,  0.965],
                        [ 0.547,  0.158,  0.818],
                        [ 0.707,  0.0,    0.707],
                        [ 0.818,  0.158,  0.547],
                        [ 0.965,  0.158,  0.192],
                        [ 1.0,    0.0,    0.0],
                        [ 0.965,  0.158,  -0.192],
                        [ 0.818,  0.158,  -0.547],
                        [ 0.707,  0.0,    -0.707],
                        [ 0.547,  0.158,  -0.818],
                        [ 0.192,  0.158,  -0.965],
                        [-0.0,    0.0,    -1.0]]

affectedObjectPoints = pos = [(3.0, 0.0, 0.0),
                              (2.0, 0.0, -1.0),
                              (2.0, 0.0, -2.0),
                              (1.0, 0.0, -2.0),
                              (0.0, 0.0, -3.0),
                              (-1.0, 0.0, -2.0),
                              (-2.0, 0.0, -2.0),
                              (-2.0, 0.0, -1.0),
                              (-3.0, 0.0, 0.0),
                              (-2.0, 0.0, 1.0),
                              (-2.0, 0.0, 2.0),
                              (-1.0, 0.0, 2.0),
                              (0.0, 0.0, 3.0),
                              (1.0, 0.0, 2.0),
                              (2.0, 0.0, 2.0),
                              (2.0, 0.0, 1.0),
                              (3.0, 0.0, 0.0)]
