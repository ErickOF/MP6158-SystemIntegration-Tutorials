# Automatically generated file proj.py"

# Generated with $Id: extrusion_to_empro.cpp 11193 2012-11-22 13:42:22Z mdewilde $ 

import empro, empro.toolkit

def getVersion():
	return 11

def getSessionVersion(session):
	try:
		return session.getVersion()
	except AttributeError:
		return 0

def get_ads_import_version():
	try:
		ads_import_version = empro.toolkit.ads_import.getVersion()
	except AttributeError:
		ads_import_version = 0
	return ads_import_version

def ads_simulation_settings():
	set_frequency_plan_and_common_options()
	set_FEM_options()

def set_frequency_plan_and_common_options():
	try:
		sim=empro.activeProject.simulationSettings
	except AttributeError:
		sim=empro.activeProject.createSimulationData()
	# Frequency plan:
	frequency_plan_list=sim.femFrequencyPlanList()
	frequency_plan=empro.simulation.FrequencyPlan()
	frequency_plan.type="Adaptive"
	frequency_plan.startFrequency=0
	frequency_plan.stopFrequency=10000000000
	frequency_plan.samplePointsLimit=50
	frequency_plan_list.append(frequency_plan)
	if 'minFreq' in empro.activeProject.parameters:
		empro.activeProject.parameters.setFormula('minFreq','0 GHz')
	if 'maxFreq' in empro.activeProject.parameters:
		empro.activeProject.parameters.setFormula('maxFreq','10 GHz')
	sim.saveFieldsFor="NoFrequencies"

def set_FEM_options():
	# Simulation options:
	try:
		sim=empro.activeProject.simulationSettings
	except AttributeError:
		sim=empro.activeProject.createSimulationData()
	sim.simulator = "com.keysight.xxpro.simulator.fem"
	try:
		sim.ambientConditions.backgroundTemperature = "25 degC"
	except AttributeError:
		pass
	try:
		sim.femEigenMode = False
	except AttributeError:
		pass
	try:
		sim.portOnlyMode = False
	except AttributeError:
		pass
	try:
		sim.transfinitePorts  = False
	except AttributeError:
		pass
	sim.femMeshSettings.minimumNumberOfPasses      = 2
	sim.femMeshSettings.maximumNumberOfPasses      = 15
	sim.femMeshSettings.deltaError                 = 0.02
	sim.femMeshSettings.refineAtSpecificFrequency  = False
	sim.femMeshSettings.refinementFrequency        = "0 GHz"
	sim.femMeshSettings.requiredConsecutivePasses  = 1
	sim.femMeshSettings.meshRefinementPercentage   = 25
	sim.femMeshSettings.orderOfBasisFunctions      = 2
	try:
		sim.femMeshSettings.useMinMeshSize               = False
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.minMeshSize                  = "0 m" 
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.autoTargetMeshSize           = True
		sim.femMeshSettings.useTargetMeshSize            = True
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.targetMeshSize               = "0 m" 
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.edgeMeshLength               = "0 m" 
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.vertexMeshLength               = "0 m" 
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.mergeObjectsOfSameMaterial = True
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.alwaysSolveOnFinestMesh = False
	except AttributeError:
		pass
	try:
		sim.femMeshSettings.autoConductorMeshing = False
	except AttributeError:
		pass
	try:
		empro.activeProject.gridGenerator.femPadding.useDefault = False
	except AttributeError:
		pass
	try:
		sim.dataSetFileName                            = ''
	except AttributeError:
		pass
	try:
		sim.femMatrixSolver.solverType                    = "MatrixSolverAuto"
	except ValueError: # Old versions of EMPro (< 2017) do not have the auto-select solver option
		sim.femMatrixSolver.solverType                    = "MatrixSolverDirect"
	sim.femMatrixSolver.maximumNumberOfIterations     = 500
	sim.femMatrixSolver.tolerance                     = 1e-05
	try:
		sim.femMeshSettings.refinementStrategy="maxFrequency"
	except AttributeError:
		pass

def get_session(usedFlow="ADS"):
	ads_import_version = get_ads_import_version()
	if ads_import_version >= 3:
		session=empro.toolkit.ads_import.Import_session(units="mm", wall_boundary="Radiation",usedFlow=usedFlow,adsProjVersion=getVersion())
		return session
	try:
		session=empro.toolkit.ads_import.Import_session(units="mm", wall_boundary="Radiation",usedFlow=usedFlow)
	except TypeError: # usedFlow may not be available in old FEM bits
		session=empro.toolkit.ads_import.Import_session(units="mm", wall_boundary="Radiation")
	return session

def _dummyUpdateProgress(value):
	pass

def _createIfToggleExtensionToBoundingBoxExpression(exprTrue,exprFalse):
	if get_ads_import_version() >= 11:
		return "if(toggleExtensionToBoundingBox, %s, %s)" % (exprTrue, exprFalse)
	else:
		return exprFalse

def ads_import(usedFlow="ADS",topAssembly=None,session=None,demoMode=False,includeInvalidPorts=True,suppressNotification=False,updateProgressFunction=_dummyUpdateProgress,materialForEachLayer=False):
	ads_simulation_settings()
	importer = projImporter(usedFlow,session,updateProgressFunction)
	rv = importer.ads_import(usedFlow,topAssembly,demoMode,includeInvalidPorts,suppressNotification,materialForEachLayer)
	try:
		empro.activeProject.gridGenerator.femPadding.useDefault = False
	except AttributeError:
		pass
	return rv

class projImporter():
	def __init__(self,usedFlow="ADS",session=None,updateProgressFunction=_dummyUpdateProgress):
		self.usedFlow = usedFlow
		if session==None:
			self.session=get_session(usedFlow)
		else:
			self.session = session
		if getSessionVersion(self.session) >= 8:
			self.session.setProjImporter(self)
		self.roughnesses={}
		self.materials={}
		self.substratePartNameMap={}
		self.substrateLayers=[] # ordered list with substrate layers
		self.waveforms={}
		self.circuitComponentDefinitions={}
		self.initNetlists()
		self.updateProgressFunction = updateProgressFunction
		if updateProgressFunction == _dummyUpdateProgress:
			if getSessionVersion(self.session) >= 10:
				self.updateProgressFunction = self.session.getUpdateProgressFunction()
		self.geoProgress = 0

	def _updateProgress(self,progress):
		self.updateProgressFunction(progress)

	def _setModelTypeForMetals(self,material,value):
		if getSessionVersion(self.session) >= 2:
			self.session.setModelTypeForMetals(material,value)
			return
		try:
			material.details.electricProperties.parameters.useSurfaceConductivityCorrection = value
		except:
			pass
	def _checked_roughness(self,roughnessTypeString,*args):
		try:
			roughnessConstructor = getattr(empro.material,roughnessTypeString)
			return roughnessConstructor(*args)
		except AttributeError:
			print("Warning: unsupported surface roughness type %s. Roughness will be ignored." % roughnessTypeString)
			return None
	def _create_parameter(self,iParName,iFormula,iNotes,iUserEditable,fixGridAxis=""):
		if getSessionVersion(self.session) >= 2:
			self.session.create_parameter(iParName,iFormula,iNotes,iUserEditable,fixGridAxis)
			return
		try:
			self.session.create_parameter(iParName,iFormula,iNotes,iUserEditable)
		except AttributeError:
			empro.activeProject.parameters.append(iParName,iFormula,iNotes,iUserEditable)
		if fixGridAxis in ['X','Y','Z']:
			gG = empro.activeProject.gridGenerator
			newFP = empro.libpyempro.mesh.FixedPoint()
			if fixGridAxis == 'X':
				location = (iParName,0,0)
			elif fixGridAxis == 'Y':
				location = (0,iParName,0)
			elif fixGridAxis == 'Z':
				location = (0,0,iParName)
			newFP.location = location
			newFP.axes=fixGridAxis
			gG.addManualFixedPoint(newFP)
	def _circularGridRegion(self,x,y,radius):
		radius = empro.core.Expression(radius)
		newGRP = empro.libpyempro.mesh.ManualGridRegionParameters()
		newGRP.cellSizes.target = (radius,radius,0)
		newGRP.gridRegionDirections="X|Y"
		newGRP.regionBounds.lower = (x-radius,y-radius,0)
		newGRP.regionBounds.upper = (x+radius,y+radius,0)
		return newGRP
	def _partGridParameters(self,targetCellSize):
		targetCellSize = empro.core.Expression(targetCellSize)
		newGP = empro.libpyempro.mesh.PartGridParameters()
		newGP.cellSizes.target = (targetCellSize,targetCellSize,0)
		newGP.gridRegionDirections="X|Y"
		newGP.useGridRegions = True
		return newGP
	def _create_sketch(self,pointString,sketch=None,closed=True):
		if getSessionVersion(self.session) >= 4:
			return self.session.create_sketch(pointString,sketch,closed)
		V=empro.geometry.Vector3d
		L=empro.geometry.Line
		def stringToPoint(s):
			sList = s.split('#')
			return V(sList[0],sList[1],0)
		if sketch == None:
			sketch=empro.geometry.Sketch()
		pointList = [ stringToPoint(x) for x in pointString.split(';') ]
		if closed:
			edges = [ L(pointList[i-1],pointList[i]) for i in range(len(pointList)) ]
		else:
			edges = [ L(pointList[2*i],pointList[2*i+1]) for i in range(len(pointList)/2) ]
		sketch.addEdges(edges)
		return sketch
	def _create_extrude(self, pointStrings, height, up):
		if getSessionVersion(self.session) >= 14:
			return self.session.create_extrude(pointStrings, height, up)
		else:
			sketch = None
			for pointString in pointStrings:
				sketch = self._create_sketch(pointString, sketch)
			part = empro.geometry.Model()
			part.recipe.append(empro.geometry.Extrude(sketch, height, empro.geometry.Vector3d(0, 0, (-1, 1)[up])))
			return part
	def _create_cover(self, pointStrings):
		if getSessionVersion(self.session) >= 14:
			return self.session.create_cover(pointStrings)
		else:
			sketch = None
			for pointString in pointStrings:
				sketch = self._create_sketch(pointString, sketch)
			part = empro.geometry.Model()
			part.recipe.append(empro.geometry.Cover(sketch))
			return part
	def _create_bondwire(self,radius, segments, points, name=None,bwAssembly=None,topAssembly=None,material=None,partModifier=(lambda x : x),profile=None,above=True):
		if getSessionVersion(self.session) >= 13:
			part = self.session.create_bondwire(radius, segments, points, name, bwAssembly,topAssembly,material,partModifier,profile,above)
		else:
			if profile is not None:
				part = empro.geometry.Model()
				try:
					part.recipe.append(empro.geometry.Bondwire(points[0],points[-1],profile))
				except TypeError:
					# Only for compatibility with EMPro 2011.02 or older
					self.session.warnings.append('For importing bondwires with profile definitions it is advised to use EMPro 2012.09 or later.')
					bw=empro.geometry.Bondwire(points[0],points[-1],empro.geometry.BondwireDefinition(name,radius,segments))
					bw.definition=profile
					part.recipe.append(bw)
				if not above:
					import math
					part.coordinateSystem.rotate(math.pi,0,0)
				part = partModifier(part)
				bwAssembly.append(part)
				part.name = name
				empro.toolkit.applyMaterial(part,material)
			else:
				try:
					part = self.session.create_bondwire(radius, segments, points, name, bwAssembly,topAssembly,material,partModifier)
				except TypeError:
					part = self.session.create_bondwire(radius, segments, points)
					part = partModifier(part)
					bwAssembly.append(part)
					part.name = name
					empro.toolkit.applyMaterial(part,material)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=2000
		return part
	def _create_internal_port(self, name, definitionString, head, tail, extent=None):
		if getSessionVersion(self.session) < 15 and (isinstance(head, list) or isinstance(tail, list)):
			raise RuntimeError("Ports having multiple positive or negative pins are not yet supported")
		if getSessionVersion(self.session) >= 9:
			return self.session.create_internal_port(name, definitionString, head, tail, extent)
		port=empro.components.CircuitComponent()
		port.name=name
		port.definition=self.circuitComponentDefinitions[definitionString]
		port.head=head
		port.tail=tail
		if extent != None:
			port.extent=extent
			port.useExtent=True
		return port
	def _set_extra_port_info(self, port, termType, number, name, feedType, mode = -1):
		try:
			if get_ads_import_version() >= 17:
				self.session.set_extra_port_info(port=port, termType=termType, number=number, name=name, mode=mode, feedType=feedType)
			else:
				self.session.set_extra_port_info(port=port, termType=termType, number=number, name=name, mode=mode)
		except AttributeError:
			pass
		global g_portNbToName
		g_portNbToName[number] = (name, mode)
	def _setAssemblyMeshSettings(self,a,vertexMeshLength=0,edgeMeshLength=0,surfaceMeshLength=0):
		if vertexMeshLength==0 and edgeMeshLength==0 and surfaceMeshLength==0:
			return
		if getSessionVersion(self.session) >= 12:
			self.session.setAssemblyMeshSettings(a,vertexMeshLength,edgeMeshLength,surfaceMeshLength)
			return
		parts = [x for x in a.flatList(False)]
		for x in parts:
			x.meshParameters.vertexMeshLength=vertexMeshLength
			x.meshParameters.edgeMeshLength=edgeMeshLength
			x.meshParameters.surfaceMeshLength=surfaceMeshLength
	def _getEMProMaterialName(self,ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1):
		EMProMaterialName=ADSmaterialName
		if ADSmaterialName in [x for (x,y) in ADSmaterialMap.keys()]:
			EMProMaterialName+="_"+str(extraMaterialProperties)
			if not ADSmaterialName in ADSmaterialsNo1to1:
				ADSmaterialsNo1to1.append(ADSmaterialName)
				self.session.warnings.append('The ADS material '+ADSmaterialName+' is used on masks with different precedence, sheet thickness or modeltype for metals and has therefore been mapped to multiple EMPro materials.')
		return EMProMaterialName
	def create_bondwire_definitions(self):
		self.bondwire_definitions={}
		if not hasattr(empro.activeProject,"bondwireDefinitions"):
			return
	def create_materials(self,materialForEachLayer=False):
		ADSmaterialMap={}
		EMProNameMaterialMap={}
		layerEMProMaterialNameMap={}
		ADSmaterialsNo1to1=[]
		ADSmaterialName=["AIR","simulation_box"][materialForEachLayer]
		extraMaterialProperties=(0,None,None,False) # (priority,thickness,modelTypeForMetals,convertedToResistance)
		material=ADSmaterialMap.get((ADSmaterialName,extraMaterialProperties),None)
		if material == None:
			EMProMaterialName = self._getEMProMaterialName(ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1)
			material=self.session.create_material(name=EMProMaterialName, color=(255,255,255,0), permittivity=1, permeability=1)
			try:
				material.priority=0
				material.autoPriority=False
			except AttributeError:
				pass
			ADSmaterialMap[(ADSmaterialName,extraMaterialProperties)]=material
			EMProNameMaterialMap[EMProMaterialName]=material
		else:
			EMProMaterialName=material.name
		self.materials["simulation_box"]=material
		layerEMProMaterialNameMap["simulation_box"]=EMProMaterialName
		ADSmaterialName=["Copper","cond"][materialForEachLayer]
		extraMaterialProperties=(162,3.5e-05,False,True) # (priority,thickness,modelTypeForMetals,convertedToResistance)
		material=ADSmaterialMap.get((ADSmaterialName,extraMaterialProperties),None)
		if material == None:
			EMProMaterialName = self._getEMProMaterialName(ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1)
			material=self.session.create_material(name=EMProMaterialName, color=(238,106,80,255), thickness="3.5e-05 m", resistance=1.72413793103448e-08/3.5e-05, permeability=1)
			try:
				material.details.electricProperties.parameters.thickness = "3.5e-05 m"
			except AttributeError:
				pass
			self._setModelTypeForMetals(material,False)
			try:
				material.priority=162
				material.autoPriority=False
			except AttributeError:
				pass
			ADSmaterialMap[(ADSmaterialName,extraMaterialProperties)]=material
			EMProNameMaterialMap[EMProMaterialName]=material
		else:
			EMProMaterialName=material.name
		self.materials["cond"]=material
		layerEMProMaterialNameMap["cond"]=EMProMaterialName
		ADSmaterialName=["Copper","cond2"][materialForEachLayer]
		extraMaterialProperties=(160,3.5e-05,False,True) # (priority,thickness,modelTypeForMetals,convertedToResistance)
		material=ADSmaterialMap.get((ADSmaterialName,extraMaterialProperties),None)
		if material == None:
			EMProMaterialName = self._getEMProMaterialName(ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1)
			material=self.session.create_material(name=EMProMaterialName, color=(255,255,0,255), thickness="3.5e-05 m", resistance=1.72413793103448e-08/3.5e-05, permeability=1)
			try:
				material.details.electricProperties.parameters.thickness = "3.5e-05 m"
			except AttributeError:
				pass
			self._setModelTypeForMetals(material,False)
			try:
				material.priority=160
				material.autoPriority=False
			except AttributeError:
				pass
			ADSmaterialMap[(ADSmaterialName,extraMaterialProperties)]=material
			EMProNameMaterialMap[EMProMaterialName]=material
		else:
			EMProMaterialName=material.name
		self.materials["cond2"]=material
		layerEMProMaterialNameMap["cond2"]=EMProMaterialName
		ADSmaterialName=["Copper","hole"][materialForEachLayer]
		extraMaterialProperties=(64,None,False,False) # (priority,thickness,modelTypeForMetals,convertedToResistance)
		material=ADSmaterialMap.get((ADSmaterialName,extraMaterialProperties),None)
		if material == None:
			EMProMaterialName = self._getEMProMaterialName(ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1)
			material=self.session.create_material(name=EMProMaterialName, color=(0,191,255,255), conductivity=58000000, imag_conductivity=0, permeability=1)
			self._setModelTypeForMetals(material,False)
			try:
				material.priority=64
				material.autoPriority=False
			except AttributeError:
				pass
			ADSmaterialMap[(ADSmaterialName,extraMaterialProperties)]=material
			EMProNameMaterialMap[EMProMaterialName]=material
		else:
			EMProMaterialName=material.name
		self.materials["hole"]=material
		layerEMProMaterialNameMap["hole"]=EMProMaterialName
		ADSmaterialName=["Copper","closed_bottom"][materialForEachLayer]
		extraMaterialProperties=(140,None,None,False) # (priority,thickness,modelTypeForMetals,convertedToResistance)
		material=ADSmaterialMap.get((ADSmaterialName,extraMaterialProperties),None)
		if material == None:
			EMProMaterialName = self._getEMProMaterialName(ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1)
			material=self.session.create_material(name=EMProMaterialName, color=(210,210,210,255), conductivity=58000000, imag_conductivity=0, permeability=1)
			try:
				material.priority=140
				material.autoPriority=False
			except AttributeError:
				pass
			ADSmaterialMap[(ADSmaterialName,extraMaterialProperties)]=material
			EMProNameMaterialMap[EMProMaterialName]=material
		else:
			EMProMaterialName=material.name
		self.materials["closed_bottom"]=material
		layerEMProMaterialNameMap["closed_bottom"]=EMProMaterialName
		ADSmaterialName=["Rogers_4003C","__SubstrateLayer2___SubstrateLayer1"][materialForEachLayer]
		extraMaterialProperties=(50,None,None,False) # (priority,thickness,modelTypeForMetals,convertedToResistance)
		material=ADSmaterialMap.get((ADSmaterialName,extraMaterialProperties),None)
		if material == None:
			EMProMaterialName = self._getEMProMaterialName(ADSmaterialName,ADSmaterialMap,extraMaterialProperties,ADSmaterialsNo1to1)
			material=self.session.create_material(name=EMProMaterialName, color=(202,225,255,128), permittivity=3.55, losstangent=0.0021, permeability=1, use_djordjevic=True, lowfreq=1000, evalfreq=2500000000, highfreq=1000000000000)
			try:
				material.priority=50
				material.autoPriority=False
			except AttributeError:
				pass
			ADSmaterialMap[(ADSmaterialName,extraMaterialProperties)]=material
			EMProNameMaterialMap[EMProMaterialName]=material
		else:
			EMProMaterialName=material.name
		self.materials["__SubstrateLayer2___SubstrateLayer1"]=material
		layerEMProMaterialNameMap["__SubstrateLayer2___SubstrateLayer1"]=EMProMaterialName
		self.substratePartNameMap["__SubstrateLayer2___SubstrateLayer1"]=ADSmaterialName
		self.substrateLayers.append("__SubstrateLayer2___SubstrateLayer1")
		self.numberSubstratePartNameMap()
		if getSessionVersion(self.session) >= 6:
			self.session.appendUniqueMaterials(EMProNameMaterialMap)
		else:
			for name,material in EMProNameMaterialMap.items():
				empro.activeProject.materials().append(material)
				EMProNameMaterialMap[name] = empro.activeProject.materials().at(empro.activeProject.materials().size()-1)
		self.materials={}
		for layerName in layerEMProMaterialNameMap.keys():
			self.materials[layerName]=EMProNameMaterialMap.get(layerEMProMaterialNameMap.get(layerName,None),None)
		# End of create_materials
	def numberSubstratePartNameMap(self):
		materialCount={}
		for m in self.substratePartNameMap.keys():
			materialCount[self.substratePartNameMap[m]] = materialCount.get(self.substratePartNameMap[m],0) + 1
		multipleUsedMaterials = [m for m in materialCount.keys() if materialCount[m] > 1]
		for layer in self.substrateLayers:
			mat=self.substratePartNameMap.get(layer,None)
			if mat in multipleUsedMaterials:
				self.substratePartNameMap[layer]+=' '+str(materialCount[mat])
				materialCount[mat]-=1
	def setBoundaryConditions(self):
		pass
		# End of setBoundaryConditions
	def setPortWarnings(self,includeInvalidPorts):
		pass
		# End of setPortWarnings
	def initNetlists(self):
		netlistNames = ['net_0','net_1','net_2','net_3_P3','net_4','net_5','net_6_P4','net_7','net_8','net_9','net_10','net_11','net_12','net_13','net_14','net_15','net_16','net_17','net_18','net_19','net_20','net_21','net_22','net_23','net_24','net_25','net_26','net_27','net_28','net_29','net_30','net_31','net_32','net_33','net_34','net_35','net_36','net_37','net_38','net_39','net_40','net_41','net_42','net_43','net_44','net_45','net_46','net_47','net_48','net_49','net_50','net_51','net_52','net_53','net_54','net_55','net_56']
		if getSessionVersion(self.session) >= 5:
			self.session.initNetlists(netlistNames)
			return
		self.groupList = []
		try:
			for i in netlistNames:
				g = empro.core.ShortcutGroup(i)
				self.groupList.append(g)
		except:
			pass
	def addShortcut(self,netId,part):
		if getSessionVersion(self.session) >= 5:
			self.session.addShortcut(netId,part)
			return
		try:
			s = empro.core.Shortcut(part)
			self.groupList[netId].append(s)
		except:
			pass
	def addShortcutsToProject(self):
		if getSessionVersion(self.session) >= 5:
			self.session.addShortcutsToProject()
			return
		try:
			for g in self.groupList:
				empro.activeProject.shortcuts().append(g)
		except:
			pass

	def ads_import(self,usedFlow="ADS",topAssembly=None,demoMode=False,includeInvalidPorts=True,suppressNotification=False,materialForEachLayer=False):
		if getSessionVersion(self.session) >= 1:
			self.session.prepare_import()
		self.create_materials(materialForEachLayer=materialForEachLayer)
		self.create_parameters()
		if topAssembly != None:
			topAssemblyShouldBeAdded = False
		else:
			topAssembly = empro.geometry.Assembly()
			topAssembly.name = usedFlow+'_import'
			if demoMode:
				empro.activeProject.geometry.append(topAssembly)
				topAssemblyShouldBeAdded = False
			else:
				topAssemblyShouldBeAdded = True
		param_list = empro.activeProject.parameters
		param_list.setFormula( "lateralExtension", "0 mm")
		param_list.setFormula( "verticalExtension", "0 mm")
		self.create_bondwire_definitions()
		self.setBoundaryConditions()
		symbPinData = self.create_geometry(topAssembly)
		self.create_ports( topAssembly, includeInvalidPorts, symbPinData )
		if get_ads_import_version() >= 11 :
			Expr=empro.core.Expression
			if topAssembly != None:
				bbox_geom = topAssembly.boundingBox()
			else:
				bbox_geom = empro.activeProject.geometry.boundingBox()
			param_list = empro.activeProject.parameters
			param_list.setFormula( "xLowerBoundingBox", str(bbox_geom.lower.x.formula()) +" m - xLowerExtension" )
			param_list.setFormula( "xUpperBoundingBox", str(bbox_geom.upper.x.formula()) +" m + xUpperExtension" )
			param_list.setFormula( "yLowerBoundingBox", str(bbox_geom.lower.y.formula()) +" m - yLowerExtension" )
			param_list.setFormula( "yUpperBoundingBox", str(bbox_geom.upper.y.formula()) +" m + yUpperExtension" )
			param_list.setFormula( "zLowerBoundingBox", str(bbox_geom.lower.z.formula()) +" m - zLowerExtension" )
			param_list.setFormula( "zUpperBoundingBox", str(bbox_geom.upper.z.formula()) +" m + zUpperExtension" )
			param_list.setFormula( "toggleExtensionToBoundingBox", "1" )
		param_list.setFormula( "lateralExtension", "3.125 mm")
		param_list.setFormula("verticalExtension", "5 mm")
		self.addShortcutsToProject()
		if topAssemblyShouldBeAdded:
			empro.activeProject.geometry.append(topAssembly)
			self.session.adjust_view()
		self.session.renumber_waveguides()
		if getSessionVersion(self.session) >= 10:
			self.session.post_import()
		if not suppressNotification:
			self.session.notify_success()
		return self.session.warnings
		#End of ads_import method

	def create_geometry(self,topAssembly):
		V=empro.geometry.Vector3d
		L=empro.geometry.Line
		unit2meterFactor = 0.001
		symbPinData = None
		assembly=empro.geometry.Assembly()
		assembly.name="bondwires"
		assembly=empro.geometry.Assembly()
		part=empro.geometry.Model()
		simBox = empro.geometry.Box( _createIfToggleExtensionToBoundingBoxExpression("xUpperBoundingBox-xLowerBoundingBox", "abs((-0.0023579-xLowerExtension)-(0.0039125+xUpperExtension))"), _createIfToggleExtensionToBoundingBoxExpression("zUpperBoundingBox-zLowerBoundingBox", "((((stack_substrate1_layer_5_Z) + (zUpperExtension)) - (stack_substrate1_layer_1_Z)))"), _createIfToggleExtensionToBoundingBoxExpression("yUpperBoundingBox-yLowerBoundingBox" , " abs((-0.00174-yLowerExtension)-(0.0028895+yUpperExtension))"))
		part.recipe.append(simBox)
		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(_createIfToggleExtensionToBoundingBoxExpression("(xUpperBoundingBox+xLowerBoundingBox)/2", "(0.0039125+xUpperExtension+-0.0023579-xLowerExtension)/2"), _createIfToggleExtensionToBoundingBoxExpression("(yUpperBoundingBox+yLowerBoundingBox)/2", "(0.0028895+yUpperExtension+-0.00174-yLowerExtension)/2"), _createIfToggleExtensionToBoundingBoxExpression("zLowerBoundingBox","((stack_substrate1_layer_1_Z) - (0))")))
		part.name="Simulation box"
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=0
		empro.toolkit.applyMaterial(part,self.materials["simulation_box"])
		assembly.append(part)
		assembly.name="simulation_box"
		self.session.hide_part(assembly)
		topAssembly.append(assembly)
		self.session.adjust_view()
		assembly=empro.geometry.Assembly()
		pointString='0.0039125+xUpperExtension#-0.00174-yLowerExtension;0.0039125+xUpperExtension#0.0028895+yUpperExtension;-0.0023579-xLowerExtension#0.0028895+yUpperExtension;-0.0023579-xLowerExtension#-0.00174-yLowerExtension'
		sketch = self._create_sketch(pointString)
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex0",V(_createIfToggleExtensionToBoundingBoxExpression("xLowerBoundingBox","-0.0023579-xLowerExtension"),_createIfToggleExtensionToBoundingBoxExpression("yLowerBoundingBox","-0.00174-yLowerExtension"),0)))
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex1",V(_createIfToggleExtensionToBoundingBoxExpression("xUpperBoundingBox","0.0039125+xUpperExtension"),_createIfToggleExtensionToBoundingBoxExpression("yLowerBoundingBox","-0.00174-yLowerExtension"),0)))
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex2",V(_createIfToggleExtensionToBoundingBoxExpression("xUpperBoundingBox","0.0039125+xUpperExtension"),_createIfToggleExtensionToBoundingBoxExpression("yUpperBoundingBox","0.0028895+yUpperExtension"),0)))
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex3",V(_createIfToggleExtensionToBoundingBoxExpression("xLowerBoundingBox","-0.0023579-xLowerExtension"),_createIfToggleExtensionToBoundingBoxExpression("yUpperBoundingBox","0.0028895+yUpperExtension"),0)))
		part=empro.geometry.Model()
		part.recipe.append(empro.geometry.Extrude(sketch,"(stack_substrate1_layer_5_Z) - (stack_substrate1_layer_1_Z)",V(0,0,1)))
		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(stack_substrate1_layer_1_Z) - (0)"))
		part.name=self.substratePartNameMap["__SubstrateLayer2___SubstrateLayer1"]
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=50
		empro.toolkit.applyMaterial(part,self.materials["__SubstrateLayer2___SubstrateLayer1"])
		self.session.hide_part(part)
		assembly.append(part)
		assembly.name="substrate"
		topAssembly.append(assembly)
		assembly=empro.geometry.Assembly()
		pointStrings=['-0.0023412#-0.00087;-0.0022679#-0.0009316;-0.0021721#-0.0009316;-0.0020988#-0.00087;-0.0020821#-0.0007757;-0.00213#-0.0006927;-0.00222#-0.00066;-0.00231#-0.0006927;-0.0023579#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(19,part)
		self._update_geoProgress()
		pointStrings=['-0.0023412#-0.00047;-0.0022679#-0.0005316;-0.0021721#-0.0005316;-0.0020988#-0.00047;-0.0020821#-0.0003757;-0.00213#-0.0002927;-0.00222#-0.00026;-0.00231#-0.0002927;-0.0023579#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(28,part)
		pointStrings=['-0.0023412#-7e-05;-0.0022679#-0.0001316;-0.0021721#-0.0001316;-0.0020988#-7e-05;-0.0020821#2.43e-05;-0.00213#0.0001073;-0.00222#0.00014;-0.00231#0.0001073;-0.0023579#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(4,part)
		pointStrings=['-0.0023412#0.00033;-0.0022679#0.0002684;-0.0021721#0.0002684;-0.0020988#0.00033;-0.0020821#0.0004243;-0.00213#0.0005073;-0.00222#0.00054;-0.00231#0.0005073;-0.0023579#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(23,part)
		pointStrings=['-0.0023412#0.00073;-0.0022679#0.0006684;-0.0021721#0.0006684;-0.0020988#0.00073;-0.0020821#0.0008243;-0.00213#0.0009073;-0.00222#0.00094;-0.00231#0.0009073;-0.0023579#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(31,part)
		pointStrings=['-0.0023412#0.00113;-0.0022679#0.0010684;-0.0021721#0.0010684;-0.0020988#0.00113;-0.0020821#0.0012243;-0.00213#0.0013073;-0.00222#0.00134;-0.00231#0.0013073;-0.0023579#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(16,part)
		self._update_geoProgress()
		pointStrings=['-0.0023412#0.00153;-0.0022679#0.0014684;-0.0021721#0.0014684;-0.0020988#0.00153;-0.0020821#0.0016243;-0.00213#0.0017073;-0.00222#0.00174;-0.00231#0.0017073;-0.0023579#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(18,part)
		pointStrings=['-0.0019412#-0.00087;-0.0018679#-0.0009316;-0.0017721#-0.0009316;-0.0016988#-0.00087;-0.0016821#-0.0007757;-0.00173#-0.0006927;-0.00182#-0.00066;-0.00191#-0.0006927;-0.0019579#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(35,part)
		pointStrings=['-0.0019412#-0.00047;-0.0018679#-0.0005316;-0.0017721#-0.0005316;-0.0016988#-0.00047;-0.0016821#-0.0003757;-0.00173#-0.0002927;-0.00182#-0.00026;-0.00191#-0.0002927;-0.0019579#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(38,part)
		pointStrings=['-0.0019412#-7e-05;-0.0018679#-0.0001316;-0.0017721#-0.0001316;-0.0016988#-7e-05;-0.0016821#2.43e-05;-0.00173#0.0001073;-0.00182#0.00014;-0.00191#0.0001073;-0.0019579#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(21,part)
		pointStrings=['-0.0019412#0.00033;-0.0018679#0.0002684;-0.0017721#0.0002684;-0.0016988#0.00033;-0.0016821#0.0004243;-0.00173#0.0005073;-0.00182#0.00054;-0.00191#0.0005073;-0.0019579#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(24,part)
		self._update_geoProgress()
		pointStrings=['-0.0019412#0.00073;-0.0018679#0.0006684;-0.0017721#0.0006684;-0.0016988#0.00073;-0.0016821#0.0008243;-0.00173#0.0009073;-0.00182#0.00094;-0.00191#0.0009073;-0.0019579#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(44,part)
		pointStrings=['-0.0019412#0.00113;-0.0018679#0.0010684;-0.0017721#0.0010684;-0.0016988#0.00113;-0.0016821#0.0012243;-0.00173#0.0013073;-0.00182#0.00134;-0.00191#0.0013073;-0.0019579#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(45,part)
		pointStrings=['-0.0019412#0.00153;-0.0018679#0.0014684;-0.0017721#0.0014684;-0.0016988#0.00153;-0.0016821#0.0016243;-0.00173#0.0017073;-0.00182#0.00174;-0.00191#0.0017073;-0.0019579#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(27,part)
		pointStrings=['-0.00152#0.0011021;-0.00142#0.00106;-0.00132#0.0011021;-0.00128#0.001201;-0.0013214#0.0012993;-0.00142#0.00134;-0.0015186#0.0012993;-0.00156#0.001201']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(6,part)
		pointStrings=['-0.0015412#-0.00087;-0.0014679#-0.0009316;-0.0013721#-0.0009316;-0.0012988#-0.00087;-0.0012821#-0.0007757;-0.00133#-0.0006927;-0.00142#-0.00066;-0.00151#-0.0006927;-0.0015579#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(46,part)
		self._update_geoProgress()
		pointStrings=['-0.0015412#-0.00047;-0.0014679#-0.0005316;-0.0013721#-0.0005316;-0.0012988#-0.00047;-0.0012821#-0.0003757;-0.00133#-0.0002927;-0.00142#-0.00026;-0.00151#-0.0002927;-0.0015579#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(29,part)
		pointStrings=['-0.0015412#-7e-05;-0.0014679#-0.0001316;-0.0013721#-0.0001316;-0.0012988#-7e-05;-0.0012821#2.43e-05;-0.00133#0.0001073;-0.00142#0.00014;-0.00151#0.0001073;-0.0015579#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(37,part)
		pointStrings=['-0.0015412#0.00033;-0.0014679#0.0002684;-0.0013721#0.0002684;-0.0012988#0.00033;-0.0012821#0.0004243;-0.00133#0.0005073;-0.00142#0.00054;-0.00151#0.0005073;-0.0015579#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(9,part)
		pointStrings=['-0.0015412#0.00073;-0.0014679#0.0006684;-0.0013721#0.0006684;-0.0012988#0.00073;-0.0012821#0.0008243;-0.00133#0.0009073;-0.00142#0.00094;-0.00151#0.0009073;-0.0015579#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(40,part)
		pointStrings=['-0.0015412#0.00153;-0.0014679#0.0014684;-0.0013721#0.0014684;-0.0012988#0.00153;-0.0012821#0.0016243;-0.00133#0.0017073;-0.00142#0.00174;-0.00151#0.0017073;-0.0015579#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(7,part)
		self._update_geoProgress()
		pointStrings=['-0.0011412#-0.00087;-0.0010679#-0.0009316;-0.0009721#-0.0009316;-0.0008988#-0.00087;-0.0008821#-0.0007757;-0.00093#-0.0006927;-0.00102#-0.00066;-0.00111#-0.0006927;-0.0011579#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(49,part)
		pointStrings=['-0.0011412#-0.00047;-0.0010679#-0.0005316;-0.0009721#-0.0005316;-0.0008988#-0.00047;-0.0008821#-0.0003757;-0.00093#-0.0002927;-0.00102#-0.00026;-0.00111#-0.0002927;-0.0011579#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(32,part)
		pointStrings=['-0.0011412#-7e-05;-0.0010679#-0.0001316;-0.0009721#-0.0001316;-0.0008988#-7e-05;-0.0008821#2.43e-05;-0.00093#0.0001073;-0.00102#0.00014;-0.00111#0.0001073;-0.0011579#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(42,part)
		pointStrings=['-0.0011412#0.00033;-0.0010679#0.0002684;-0.0009721#0.0002684;-0.0008988#0.00033;-0.0008821#0.0004243;-0.00093#0.0005073;-0.00102#0.00054;-0.00111#0.0005073;-0.0011579#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(1,part)
		pointStrings=['-0.0011412#0.00073;-0.0010679#0.0006684;-0.0009721#0.0006684;-0.0008988#0.00073;-0.0008821#0.0008243;-0.00093#0.0009073;-0.00102#0.00094;-0.00111#0.0009073;-0.0011579#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(14,part)
		self._update_geoProgress()
		pointStrings=['-0.0011412#0.00113;-0.0010679#0.0010684;-0.0009721#0.0010684;-0.0008988#0.00113;-0.0008821#0.0012243;-0.00093#0.0013073;-0.00102#0.00134;-0.00111#0.0013073;-0.0011579#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(10,part)
		pointStrings=['-0.0011412#0.00153;-0.0010679#0.0014684;-0.0009721#0.0014684;-0.0008988#0.00153;-0.0008821#0.0016243;-0.00093#0.0017073;-0.00102#0.00174;-0.00111#0.0017073;-0.0011579#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(50,part)
		pointStrings=['-0.0007412#-0.00087;-0.0006679#-0.0009316;-0.0005721#-0.0009316;-0.0004988#-0.00087;-0.0004821#-0.0007757;-0.00053#-0.0006927;-0.00062#-0.00066;-0.00071#-0.0006927;-0.0007579#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(51,part)
		pointStrings=['-0.0007412#-0.00047;-0.0006679#-0.0005316;-0.0005721#-0.0005316;-0.0004988#-0.00047;-0.0004821#-0.0003757;-0.00053#-0.0002927;-0.00062#-0.00026;-0.00071#-0.0002927;-0.0007579#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(39,part)
		pointStrings=['-0.0007412#-7e-05;-0.0006679#-0.0001316;-0.0005721#-0.0001316;-0.0004988#-7e-05;-0.0004821#2.43e-05;-0.00053#0.0001073;-0.00062#0.00014;-0.00071#0.0001073;-0.0007579#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(43,part)
		self._update_geoProgress()
		pointStrings=['-0.0007412#0.00033;-0.0006679#0.0002684;-0.0005721#0.0002684;-0.0004988#0.00033;-0.0004821#0.0004243;-0.00053#0.0005073;-0.00062#0.00054;-0.00071#0.0005073;-0.0007579#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(33,part)
		pointStrings=['-0.0007412#0.00073;-0.0006679#0.0006684;-0.0005721#0.0006684;-0.0004988#0.00073;-0.0004821#0.0008243;-0.00053#0.0009073;-0.00062#0.00094;-0.00071#0.0009073;-0.0007579#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(8,part)
		pointStrings=['-0.0007412#0.00113;-0.0006679#0.0010684;-0.0005721#0.0010684;-0.0004988#0.00113;-0.0004821#0.0012243;-0.00053#0.0013073;-0.00062#0.00134;-0.00071#0.0013073;-0.0007579#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(26,part)
		pointStrings=['-0.0007412#0.00153;-0.0006679#0.0014684;-0.0005721#0.0014684;-0.0004988#0.00153;-0.0004821#0.0016243;-0.00053#0.0017073;-0.00062#0.00174;-0.00071#0.0017073;-0.0007579#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(15,part)
		pointStrings=['-0.0003412#-0.00087;-0.0002679#-0.0009316;-0.0001721#-0.0009316;-9.88e-05#-0.00087;-8.21e-05#-0.0007757;-0.00013#-0.0006927;-0.00022#-0.00066;-0.00031#-0.0006927;-0.0003579#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(5,part)
		self._update_geoProgress()
		pointStrings=['-0.0003412#-0.00047;-0.0002679#-0.0005316;-0.0001721#-0.0005316;-9.88e-05#-0.00047;-8.21e-05#-0.0003757;-0.00013#-0.0002927;-0.00022#-0.00026;-0.00031#-0.0002927;-0.0003579#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(54,part)
		pointStrings=['-0.0003412#-7e-05;-0.0002679#-0.0001316;-0.0001721#-0.0001316;-9.88e-05#-7e-05;-8.21e-05#2.43e-05;-0.00013#0.0001073;-0.00022#0.00014;-0.00031#0.0001073;-0.0003579#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(30,part)
		pointStrings=['-0.0003412#0.00033;-0.0002679#0.0002684;-0.0001721#0.0002684;-9.88e-05#0.00033;-8.21e-05#0.0004243;-0.00013#0.0005073;-0.00022#0.00054;-0.00031#0.0005073;-0.0003579#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(55,part)
		pointStrings=['-0.0003412#0.00073;-0.0002679#0.0006684;-0.0001721#0.0006684;-9.88e-05#0.00073;-8.21e-05#0.0008243;-0.00013#0.0009073;-0.00022#0.00094;-0.00031#0.0009073;-0.0003579#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(48,part)
		pointStrings=['-0.0003412#0.00113;-0.0002679#0.0010684;-0.0001721#0.0010684;-9.88e-05#0.00113;-8.21e-05#0.0012243;-0.00013#0.0013073;-0.00022#0.00134;-0.00031#0.0013073;-0.0003579#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(22,part)
		self._update_geoProgress()
		pointStrings=['-0.0003412#0.00153;-0.0002679#0.0014684;-0.0001721#0.0014684;-9.88e-05#0.00153;-8.21e-05#0.0016243;-0.00013#0.0017073;-0.00022#0.00174;-0.00031#0.0017073;-0.0003579#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(12,part)
		pointStrings=['-0.0002979#-0.0017;-0.0002#-0.00174;-0.0001021#-0.0017;0.0033#-0.0017;0.0033555#-0.0016832;0.0036555#-0.0014832;0.0036882#-0.0014472;0.0037#-0.0014;0.0037#-0.00035;0.0039125#-0.00035;0.0039125#-0.0001;0.0032875#-0.0001;0.0032875#-0.00035;0.0035#-0.00035;0.0035#-0.0013465;0.0032697#-0.0015;-0.0001021#-0.0015;-0.0002#-0.00146;-0.0002979#-0.0015;-0.00034#-0.0016']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(6,part)
		pointStrings=['0.00028#0.0023385;0.000631#0.0026895;0.0033555#0.0026895;0.0035#0.0025562;0.0035#0.0009;0.0032875#0.0009;0.0032875#0.00065;0.0039125#0.00065;0.0039125#0.0009;0.0037#0.0009;0.0037#0.0026;0.0036678#0.0026735;0.0034624#0.002863;0.0033946#0.0028895;0.0005896#0.0028895;0.0005189#0.0028602;0.0001093#0.0024506;8e-05#0.0023799;8e-05#0.0016979;4e-05#0.001599;8.14e-05#0.0015007;0.00018#0.00146;0.0002786#0.0015007;0.00032#0.001599;0.00028#0.0016979']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(3,part)
		pointStrings=['5.88e-05#-0.00087;0.0001321#-0.0009316;0.0002279#-0.0009316;0.0003012#-0.00087;0.0003179#-0.0007757;0.00027#-0.0006927;0.00018#-0.00066;9e-05#-0.0006927;4.21e-05#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(11,part)
		pointStrings=['5.88e-05#-0.00047;0.0001321#-0.0005316;0.0002279#-0.0005316;0.0003012#-0.00047;0.0003179#-0.0003757;0.00027#-0.0002927;0.00018#-0.00026;9e-05#-0.0002927;4.21e-05#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(13,part)
		self._update_geoProgress()
		pointStrings=['5.88e-05#-7e-05;0.0001321#-0.0001316;0.0002279#-0.0001316;0.0003012#-7e-05;0.0003179#2.43e-05;0.00027#0.0001073;0.00018#0.00014;9e-05#0.0001073;4.21e-05#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(25,part)
		pointStrings=['5.88e-05#0.00033;0.0001321#0.0002684;0.0002279#0.0002684;0.0003012#0.00033;0.0003179#0.0004243;0.00027#0.0005073;0.00018#0.00054;9e-05#0.0005073;4.21e-05#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(47,part)
		pointStrings=['5.88e-05#0.00073;0.0001321#0.0006684;0.0002279#0.0006684;0.0003012#0.00073;0.0003179#0.0008243;0.00027#0.0009073;0.00018#0.00094;9e-05#0.0009073;4.21e-05#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(52,part)
		pointStrings=['5.88e-05#0.00113;0.0001321#0.0010684;0.0002279#0.0010684;0.0003012#0.00113;0.0003179#0.0012243;0.00027#0.0013073;0.00018#0.00134;9e-05#0.0013073;4.21e-05#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(41,part)
		pointStrings=['0.0004588#-0.00087;0.0005321#-0.0009316;0.0006279#-0.0009316;0.0007012#-0.00087;0.0007179#-0.0007757;0.00067#-0.0006927;0.00058#-0.00066;0.00049#-0.0006927;0.0004421#-0.0007757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(56,part)
		self._update_geoProgress()
		pointStrings=['0.0004588#-0.00047;0.0005321#-0.0005316;0.0006279#-0.0005316;0.0007012#-0.00047;0.0007179#-0.0003757;0.00067#-0.0002927;0.00058#-0.00026;0.00049#-0.0002927;0.0004421#-0.0003757']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(36,part)
		pointStrings=['0.0004588#-7e-05;0.0005321#-0.0001316;0.0006279#-0.0001316;0.0007012#-7e-05;0.0007179#2.43e-05;0.00067#0.0001073;0.00058#0.00014;0.00049#0.0001073;0.0004421#2.43e-05']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(34,part)
		pointStrings=['0.0004588#0.00033;0.0005321#0.0002684;0.0006279#0.0002684;0.0007012#0.00033;0.0007179#0.0004243;0.00067#0.0005073;0.00058#0.00054;0.00049#0.0005073;0.0004421#0.0004243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(53,part)
		pointStrings=['0.0004588#0.00073;0.0005321#0.0006684;0.0006279#0.0006684;0.0007012#0.00073;0.0007179#0.0008243;0.00067#0.0009073;0.00058#0.00094;0.00049#0.0009073;0.0004421#0.0008243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(2,part)
		pointStrings=['0.0004588#0.00113;0.0005321#0.0010684;0.0006279#0.0010684;0.0007012#0.00113;0.0007179#0.0012243;0.00067#0.0013073;0.00058#0.00134;0.00049#0.0013073;0.0004421#0.0012243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(0,part)
		self._update_geoProgress()
		pointStrings=['0.0004588#0.00153;0.0005321#0.0014684;0.0006279#0.0014684;0.0007012#0.00153;0.0007179#0.0016243;0.00067#0.0017073;0.00058#0.00174;0.00049#0.0017073;0.0004421#0.0016243']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 1)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=162
		empro.toolkit.applyMaterial(part,self.materials["cond"])
		assembly.append(part)
		self.addShortcut(20,part)
		self._setAssemblyMeshSettings(assembly,0,0,0)
		assembly.name="cond"
		topAssembly.append(assembly)
		assembly=empro.geometry.Assembly()
		pointStrings=['-0.0014987#-0.0013805;-0.0012787#-0.0016616;-0.0012438#-0.0016899;-0.0012#-0.0017;-0.0002979#-0.0017;-0.0002#-0.00174;-0.0001021#-0.0017;-6e-05#-0.0016;-0.0001021#-0.0015;-0.0002#-0.00146;-0.0002979#-0.0015;-0.0011513#-0.0015;-0.00132#-0.0012844;-0.00132#0.0011021;-0.00128#0.001201;-0.0013214#0.0012993;-0.00142#0.00134;-0.0015186#0.0012993;-0.00156#0.001201;-0.00152#0.0011021;-0.00152#-0.0013189']
		part = self._create_cover(pointStrings)

		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_cond2_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 2)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=160
		empro.toolkit.applyMaterial(part,self.materials["cond2"])
		assembly.append(part)
		self.addShortcut(6,part)
		self._setAssemblyMeshSettings(assembly,0,0,0)
		assembly.name="cond2"
		topAssembly.append(assembly)
		assembly=empro.geometry.Assembly()
		pointStrings=['-0.0014843#0.001137;-0.00142#0.00111;-0.0013557#0.001137;-0.00133#0.0012006;-0.0013566#0.0012639;-0.00142#0.00129;-0.0014834#0.0012639;-0.00151#0.0012006']
		part = self._create_extrude(pointStrings, "(mask_hole_Zmax) - (mask_hole_Zmin)", up=True)
		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_hole_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 5)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=64
		empro.toolkit.applyMaterial(part,self.materials["hole"])
		assembly.append(part)
		self.addShortcut(6,part)
		pointStrings=['-0.000263#-0.0016643;-0.0002#-0.00169;-0.000137#-0.0016643;-0.00011#-0.0016;-0.000137#-0.0015357;-0.0002#-0.00151;-0.000263#-0.0015357;-0.00029#-0.0016']
		part = self._create_extrude(pointStrings, "(mask_hole_Zmax) - (mask_hole_Zmin)", up=True)
		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(mask_hole_Zmin) - (0)"))
		part.setAttribute('LtdLayerNumber', 5)
		part.meshParameters=empro.mesh.ModelMeshParameters()
		part.meshParameters.priority=64
		empro.toolkit.applyMaterial(part,self.materials["hole"])
		assembly.append(part)
		self.addShortcut(6,part)
		self._setAssemblyMeshSettings(assembly,0,0,0)
		assembly.name="hole"
		topAssembly.append(assembly)
		assembly=empro.geometry.Assembly()
		pointStrings=['0.0070375#-0.004865;0.0070375#0.0060145;-0.0054829#0.0060145;-0.0054829#-0.004865']
		sketch = None
		for pointString in pointStrings:
			sketch = self._create_sketch(pointString, sketch)
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex0",V(_createIfToggleExtensionToBoundingBoxExpression("xLowerBoundingBox","-0.0023579-xLowerExtension"),_createIfToggleExtensionToBoundingBoxExpression("yLowerBoundingBox","-0.00174-yLowerExtension"),0)))
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex1",V(_createIfToggleExtensionToBoundingBoxExpression("xUpperBoundingBox","0.0039125+xUpperExtension"),_createIfToggleExtensionToBoundingBoxExpression("yLowerBoundingBox","-0.00174-yLowerExtension"),0)))
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex2",V(_createIfToggleExtensionToBoundingBoxExpression("xUpperBoundingBox","0.0039125+xUpperExtension"),_createIfToggleExtensionToBoundingBoxExpression("yUpperBoundingBox","0.0028895+yUpperExtension"),0)))
		sketch.constraintManager().append(empro.geometry.FixedPositionConstraint("vertex3",V(_createIfToggleExtensionToBoundingBoxExpression("xLowerBoundingBox","-0.0023579-xLowerExtension"),_createIfToggleExtensionToBoundingBoxExpression("yUpperBoundingBox","0.0028895+yUpperExtension"),0)))
		part=empro.geometry.Model()
		part.recipe.append(empro.geometry.Cover(sketch))
		part.coordinateSystem.anchorPoint = empro.geometry.CoordinateSystemPositionExpression(V(0,0,"(stack_substrate1_layer_1_Z) - (0)"))
		part.meshParameters=empro.mesh.ModelMeshParameters()
		try:
			mtrl = self.materials["closed_bottom"]
			if mtrl.details.materialType() == "Physical": 
				eProp = mtrl.details.electricProperties
				if eProp.propertyType() == "PEC" or eProp.parameters.parametersType() == "PEC":
					if topAssembly != None:
						bbox_3dcs = topAssembly.boundingBox()
					else:
						bbox_3dcs = empro.activeProject.geometry.boundingBox()
					SPAresabs=empro.activeProject.newPartModelingUnit.toReferenceUnits(1e-6)
					if (float(empro.core.Expression("((stack_substrate1_layer_1_Z) - (0))")) <= bbox_3dcs.lower.z + SPAresabs ) :
						part.meshParameters.includeInMesh=False
						empro.activeProject.parameters.setFormula( "zLowerExtension", "0 mm")
		except AttributeError:
			part.meshParameters.includeInMesh=False
		part.meshParameters.priority=140
		empro.toolkit.applyMaterial(part,self.materials["closed_bottom"])
		assembly.append(part)
		self.addShortcut(17,part)
		self._update_geoProgress()
		self._setAssemblyMeshSettings(assembly,0,0,0)
		assembly.name="closed_bottom"
		topAssembly.append(assembly)
		return symbPinData
		# End of create_geometry

	def _update_geoProgress(self):
		self.geoProgress+= 1
		if self.geoProgress % 1 == 0:
			progress = (self.geoProgress * 100)/13
			self._updateProgress(progress)

	def getMaskHeights(self,parameterized=False):
		mask_heights={}
		mask_heights_parameterized={}
		mask_heights[1]=(0.0004064, 0.0004064)
		mask_heights_parameterized[1]=("(mask_cond_Zmin) - (0)", "(mask_cond_Zmax) - (0)")
		mask_heights[5]=(0.0004064, 0.0008128)
		mask_heights_parameterized[5]=("(mask_hole_Zmin) - (0)", "(mask_hole_Zmax) - (0)")
		mask_heights[2]=(0.0008128, 0.0008128)
		mask_heights_parameterized[2]=("(mask_cond2_Zmin) - (0)", "(mask_cond2_Zmax) - (0)")
		if(parameterized):
			return mask_heights_parameterized
		else:
			return mask_heights

	def getMaskHeightsParameterized(self):
		return self.getMaskHeights(parameterized=True)

	def create_ports( self, topAssembly, includeInvalidPorts=True, symbPinData=None):
		self.setPortWarnings(includeInvalidPorts)
		V=empro.geometry.Vector3d
		L=empro.geometry.Line
		SPAresabs=empro.activeProject.newPartModelingUnit.toReferenceUnits(1e-6)
		if topAssembly != None:
			bbox_geom = topAssembly.boundingBox()
		else:
			bbox_geom = empro.activeProject.geometry.boundingBox()
		xLowerBoundary = float(bbox_geom.lower.x)
		xUpperBoundary = float(bbox_geom.upper.x)
		yLowerBoundary = float(bbox_geom.lower.y)
		yUpperBoundary = float(bbox_geom.upper.y)
		zLowerBoundary = float(bbox_geom.lower.z)
		zUpperBoundary = float(bbox_geom.upper.z)
		internalPortOnXLowerBoundary = False
		internalPortOnXUpperBoundary = False
		internalPortOnYLowerBoundary = False
		internalPortOnYUpperBoundary = False
		internalPortOnZLowerBoundary = False
		internalPortOnZUpperBoundary = False
		ports=[]
		waveguides={}
		portShortcutGroups=[]
		assembly=empro.geometry.Assembly()
		waveform=empro.waveform.Waveform("Broadband Pulse")
		waveform.shape=empro.waveform.MaximumFrequencyWaveformShape()
		self.waveforms["Broadband Pulse"]=waveform
		if getSessionVersion(self.session) >= 7:
			self.session.appendUniqueWaveforms(self.waveforms)
		else:
			for name,waveform in self.waveforms.items():
				empro.activeProject.waveforms.append(waveform)
				self.waveforms[name] = empro.activeProject.waveforms[len(empro.activeProject.waveforms)-1]
		feed=empro.components.Feed()
		feed.name="50 ohm Voltage Source"
		feed.impedance.resistance=50
		feed.waveform=self.waveforms["Broadband Pulse"]
		self.circuitComponentDefinitions[feed.name]=feed
		if getSessionVersion(self.session) >= 7:
			self.session.appendUniqueCircuitComponentDefinitions(self.circuitComponentDefinitions)
		else:
			for name,compDef in self.circuitComponentDefinitions.items():
				empro.activeProject.circuitComponentDefinitions.append(compDef)
				self.circuitComponentDefinitions[name] = empro.activeProject.circuitComponentDefinitions[len(empro.activeProject.circuitComponentDefinitions)-1]
		head=V("(0.00018) - (0)","(0.0016) - (0)","(((mask_cond_Zmax) + (mask_cond_Zmin)) / (2)) - (0)")
		tail=V("(0.00018) - (0)","(0.0016) - (0)","(stack_substrate1_layer_1_Z) - (0)")
		extent=empro.components.CylindricalExtent("0.000128114590420782","0.000128114590420782")
		port = self._create_internal_port("P1","50 ohm Voltage Source",head,tail,extent)
		portShortcutGroups.append((3,port))
		ports.append(port)
		self._set_extra_port_info(port, "inputOutput", 1, "P1", "Direct")
		headsAndTails = (head if isinstance(head, list) else [head]) + (tail if isinstance(tail, list) else [tail])
		for headOrTail in headsAndTails:
			if abs(float(headOrTail.x) - xLowerBoundary) < SPAresabs: internalPortOnXLowerBoundary = True
			if abs(float(headOrTail.x) - xUpperBoundary) < SPAresabs: internalPortOnXUpperBoundary = True
			if abs(float(headOrTail.y) - yLowerBoundary) < SPAresabs: internalPortOnYLowerBoundary = True
			if abs(float(headOrTail.y) - yUpperBoundary) < SPAresabs: internalPortOnYUpperBoundary = True
			if abs(float(headOrTail.z) - zLowerBoundary) < SPAresabs: internalPortOnZLowerBoundary = True
			if abs(float(headOrTail.z) - zUpperBoundary) < SPAresabs: internalPortOnZUpperBoundary = True
		head=V("(-0.00142) - (0)","(0.0012) - (0)","(((mask_cond_Zmax) + (mask_cond_Zmin)) / (2)) - (0)")
		tail=V("(-0.00142) - (0)","(0.0012) - (0)","(stack_substrate1_layer_1_Z) - (0)")
		extent=empro.components.CylindricalExtent("8.21513421899522e-05","8.21513421899522e-05")
		port = self._create_internal_port("P2","50 ohm Voltage Source",head,tail,extent)
		portShortcutGroups.append((6,port))
		ports.append(port)
		self._set_extra_port_info(port, "inputOutput", 2, "P2", "Direct")
		headsAndTails = (head if isinstance(head, list) else [head]) + (tail if isinstance(tail, list) else [tail])
		for headOrTail in headsAndTails:
			if abs(float(headOrTail.x) - xLowerBoundary) < SPAresabs: internalPortOnXLowerBoundary = True
			if abs(float(headOrTail.x) - xUpperBoundary) < SPAresabs: internalPortOnXUpperBoundary = True
			if abs(float(headOrTail.y) - yLowerBoundary) < SPAresabs: internalPortOnYLowerBoundary = True
			if abs(float(headOrTail.y) - yUpperBoundary) < SPAresabs: internalPortOnYUpperBoundary = True
			if abs(float(headOrTail.z) - zLowerBoundary) < SPAresabs: internalPortOnZLowerBoundary = True
			if abs(float(headOrTail.z) - zUpperBoundary) < SPAresabs: internalPortOnZUpperBoundary = True
		head=V("(0.0036) - (0)","(0.0009) - (0)","(((mask_cond_Zmax) + (mask_cond_Zmin)) / (2)) - (0)")
		tail=V("(0.0036) - (0)","(0.0009) - (0)","(stack_substrate1_layer_1_Z) - (0)")
		extent=empro.components.CylindricalExtent("9.9e-05","9.9e-05")
		port = self._create_internal_port("P3","50 ohm Voltage Source",head,tail,extent)
		portShortcutGroups.append((3,port))
		ports.append(port)
		self._set_extra_port_info(port, "inputOutput", 3, "P3", "Direct")
		headsAndTails = (head if isinstance(head, list) else [head]) + (tail if isinstance(tail, list) else [tail])
		for headOrTail in headsAndTails:
			if abs(float(headOrTail.x) - xLowerBoundary) < SPAresabs: internalPortOnXLowerBoundary = True
			if abs(float(headOrTail.x) - xUpperBoundary) < SPAresabs: internalPortOnXUpperBoundary = True
			if abs(float(headOrTail.y) - yLowerBoundary) < SPAresabs: internalPortOnYLowerBoundary = True
			if abs(float(headOrTail.y) - yUpperBoundary) < SPAresabs: internalPortOnYUpperBoundary = True
			if abs(float(headOrTail.z) - zLowerBoundary) < SPAresabs: internalPortOnZLowerBoundary = True
			if abs(float(headOrTail.z) - zUpperBoundary) < SPAresabs: internalPortOnZUpperBoundary = True
		head=V("(0.0036) - (0)","(-0.00035) - (0)","(((mask_cond_Zmax) + (mask_cond_Zmin)) / (2)) - (0)")
		tail=V("(0.0036) - (0)","(-0.00035) - (0)","(stack_substrate1_layer_1_Z) - (0)")
		extent=empro.components.CylindricalExtent("9.9e-05","9.9e-05")
		port = self._create_internal_port("P4","50 ohm Voltage Source",head,tail,extent)
		portShortcutGroups.append((6,port))
		ports.append(port)
		self._set_extra_port_info(port, "inputOutput", 4, "P4", "Direct")
		headsAndTails = (head if isinstance(head, list) else [head]) + (tail if isinstance(tail, list) else [tail])
		for headOrTail in headsAndTails:
			if abs(float(headOrTail.x) - xLowerBoundary) < SPAresabs: internalPortOnXLowerBoundary = True
			if abs(float(headOrTail.x) - xUpperBoundary) < SPAresabs: internalPortOnXUpperBoundary = True
			if abs(float(headOrTail.y) - yLowerBoundary) < SPAresabs: internalPortOnYLowerBoundary = True
			if abs(float(headOrTail.y) - yUpperBoundary) < SPAresabs: internalPortOnYUpperBoundary = True
			if abs(float(headOrTail.z) - zLowerBoundary) < SPAresabs: internalPortOnZLowerBoundary = True
			if abs(float(headOrTail.z) - zUpperBoundary) < SPAresabs: internalPortOnZUpperBoundary = True
		setPortNbToNameMappingInitialized()
		try:
			if getSessionVersion(self.session) >= 5:
				self.session.appendPortList(ports,None,portShortcutGroups)
			else:
				self.session.appendPortList(ports,self.groupList,portShortcutGroups)
		except AttributeError:
			empro.activeProject.circuitComponents().appendList(ports)
			for group,port in portShortcutGroups:
				self.addShortcut(group,port)
		for i in waveguides.keys():
			empro.activeProject.waveGuides.append(waveguides[i])
		assembly.name="waveguide_planes"
		self.session.hide_part(assembly)

	def create_grid_regions(self):
		gG = empro.activeProject.gridGenerator

	def create_parameters(self):
		self._create_parameter("stack_substrate1_layer_1_Z", "0 mm", "Z of topology level (level 1 of stack substrate1)",True,fixGridAxis='Z')
		self._create_parameter("stack_substrate1_layer_3_Z", "0.4064 mm", "Z of topology level (level 3 of stack substrate1)",True,fixGridAxis='Z')
		self._create_parameter("stack_substrate1_layer_5_Z", "0.8128 mm", "Z of topology level (level 5 of stack substrate1)",True,fixGridAxis='Z')
		self._create_parameter("lateralExtension","3.125 mm","Substrate LATERAL extension", True)
		self._create_parameter("verticalExtension","5 mm","Substrate VERTICAL extension", True)
		self._create_parameter("xLowerExtension", "lateralExtension", "Lower X extension", True)
		self._create_parameter("xUpperExtension", "lateralExtension", "Upper X extension", True)
		self._create_parameter("yLowerExtension", "lateralExtension", "Lower Y extension", True)
		self._create_parameter("yUpperExtension", "lateralExtension", "Upper Y extension", True)
		self._create_parameter("zLowerExtension", "verticalExtension", "Lower Z extension", True)
		self._create_parameter("zUpperExtension", "verticalExtension", "Upper Z extension", True)
		if get_ads_import_version() >= 11 :
			self._create_parameter("toggleExtensionToBoundingBox", 0, "toggle extension of gnd/substrate layers to bounding box of geometry", True)
			self._create_parameter("xLowerBoundingBox", 0.0, "lower X coordinate of bounding box of geometry (for extension of covers)", True)
			self._create_parameter("yLowerBoundingBox", 0.0, "lower Y coordinate of bounding box of geometry (for extension of covers)", True)
			self._create_parameter("zLowerBoundingBox", 0.0, "lower Z coordinate of bounding box of geometry (for extension of covers)", True)
			self._create_parameter("xUpperBoundingBox", 0.0, "upper X coordinate of bounding box of geometry (for extension of covers)", True)
			self._create_parameter("yUpperBoundingBox", 0.0, "upper Y coordinate of bounding box of geometry (for extension of covers)", True)
			self._create_parameter("zUpperBoundingBox", 0.0, "upper Z coordinate of bounding box of geometry (for extension of covers)", True)
		self._create_parameter("mask_cond_Zmin",str("0.4064 mm"),"Zmin of mask cond",True,fixGridAxis='Z')
		self._create_parameter("mask_cond_Zmax","mask_cond_Zmin","Zmax of mask cond",True)
		self._create_parameter("mask_hole_Zmin",str("0.4064 mm"),"Zmin of mask hole",True,fixGridAxis='Z')
		self._create_parameter("mask_hole_Zmax",str("0.8128 mm"),"Zmax of mask hole",True,fixGridAxis='Z')
		self._create_parameter("mask_cond2_Zmin",str("0.8128 mm"),"Zmin of mask cond2",True,fixGridAxis='Z')
		self._create_parameter("mask_cond2_Zmax","mask_cond2_Zmin","Zmax of mask cond2",True)

def maxNbThreadsADS():
	maxNbThreads=0
	return maxNbThreads


g_portNbToName={}
g_portNbToNameInitialized=False

def portNbToName():
	if g_portNbToNameInitialized == True:
		return g_portNbToName
	raise RuntimeError("portNbToName used uninitialized")

def setPortNbToNameMappingInitialized( state = True ):
	global g_portNbToNameInitialized
	g_portNbToNameInitialized = True

def radiationPossible():
	return True

def main():
	try:
		demoMode=empro.toolkit.ads_import.useDemoMode()
	except AttributeError:
		demoMode=False
	try:
		ads_import(demoMode=demoMode)
	except Exception:
		empro.toolkit.ads_import.notify_failure()
		raise

if __name__=="__main__":
	main()
	del ads_import
