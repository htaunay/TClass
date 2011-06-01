#encoding: utf8
"""
Module containing pca class

@author: Henrique d'Escragnolle-Taunay
@contact: htaunay@gmail.com
"""

# global dependencies
import sys, traceback

# local dependecies
from tclass.corpus import Corpus
from tclass.util import exception

#external dependencies
import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

class PCA:
	"""
	Class for pca.
	"""
	
#>------------------------------------------------------------------------------
#> Special Methods    

	def __init__(self, corpus=None, verbose=True):
		"""
		Constructor

		@param corpus: Corpus to analized
		
		@param verbose: Defines if the classes operations should be
						explicitly presented on the prompt window.

		@ivar __numDimensions: 	Quantity of different tokens in the given corpus. 
								Each word (or it's respective stem) represents a
								attribute of the given data.
		
		@ivar __numSamples: 	Quantity of different documents in the given
								corpus. Each document, independent of class,
								represents a samples of the given data.
								
		@ivar __numClasses: 	Quantity of different classes in the given corpus.
								If the corpus does not present any specific 
								classes, the default is one generic class.
		
		@ivar __data:			A numpy matrix, representing the whole word
								frequency distribution in the given corpus.
								Each row represents a document/sample. Each 
								column represents a attribute/word.
		
		@ivar __centralizedData:	A numpy matrix variation of __data, only
									here all of the values have been centralized
									(every value is subtracted by the average of
									it's respective column, therefore, leaving
									each column with a #TODO )
		
		@ivar __classMap:		Two-column matrix, where the first column
								represents a document number, and the second
								column represents the frist columns text class
								number.
		
		@ivar __verbose:		Defines if the classes operations should be
								explicitly presented on the prompt window. 
		
		@ivar __colorMap:		Vector with several options of colors. These
								colors are used to separate visually diferent
								classes while plotting a graph.
		
		@ivar __markerMap:		Vector with several options of markers. These
								markers are used to separate visually diferent
								classes while plotting a graph.
		
		"""

		self.__numDimensions 	= -1
		self.__numSamples		= -1
		self.__numClasses		= -1
		self.__data				= None
		self.__centralizedData	= None
		self.__classMap			= None
		self.__verbose			= verbose
		
		self.__colorMap = [ 'b', #blue
							'r', #red
							'g', #green
							'c', #cyan
							'm', #magenta
							'y', #yellow
							'w', #white
							'k' ] #black
							
		self.__markerMap = ['o', #circle
							'^', #triangle
							's', #square
							'+', #plus
							'd', #diamond
							'x', #cross
							's', #square
							'v' ] #triangle down
		
		# if a corpus was given in the constructor, call data setup
		if corpus != None:
			self.__setData( corpus )
		
#>------------------------------------------------------------------------------
#> Public methods

	def loadCorpus(self, corpus):
		"""
		Loads corpus, add sets up it's data, so it can be treated by the PCA class.
		Eliminates all old data, in case it exists.

		@param corpus: corpus class to be analized
		"""
        
        #clean up
		self.__numDimensions 	= -1
		self.__numSamples		= -1
		self.__numClasses		= -1
		self.__data				= None
		self.__centralizedData	= None
		self.__classMap			= None
	
		self.__setData( corpus )
		
	def show2D(self, colorClasses=True, markerClasses=True):
		"""
		Displays on the X and Y axis the two principal components present
		on the corpus being treated. The proportional variance visible
		in such components is shown on the windows title.
		
		@param colorClasses: Draw each class with a different color
		
		@param markerClasses: Draw each class with a different marker
		"""
		
		#TODO checkvalidity
		pcas = self.__getPrincipalComponents( 2 )
		pcaVariances, pcaSumVariances = self.__updateVariances( pcas )

		# Calculate percentage of visible variance
		percNumber = ( pcaSumVariances[1]/self.__getVariance() ) * 100
		percString = "Principal Component Analysis - ~%(perc).2f of variance visible" % {"perc": percNumber}
		
		# Create a plot figure object set visible variance at title
		fig = plot.figure()
		fig.canvas.set_window_title(percString)
		
		canvas = fig.add_subplot( 111 )
		canvas.set_xlabel( 'X - First Component' )
		canvas.set_ylabel( 'Y - Second Component' )
		
		for i in range(self.__numSamples):
		
			marker, color = self.__getMarkerAndColor(i)
			
			if markerClasses == True:
				classMarker = self.__markerMap[marker]
			else:
				classMarker = self.__markerMap[0]
				
			if colorClasses == True:
				classColor = self.__colorMap[color]
			else:
				classColor = self.__colorMap[0]
				
			#plot the already calculated and configured point
			canvas.plot( pcas[0][i], pcas[1][i], color=classColor, marker=classMarker )

		plot.show()
		
	def show3D(self, colorClasses=True, markerClasses=True):
		"""
		Displays on the X,Y and Z axis the three principal components present
		on the corpus being treated. The proportional variance visible
		in such components is shown on the windows title.
		
		@param colorClasses: Draw each class with a different color
		
		@param markerClasses: Draw each class with a different marker
		"""
		
		#TODO checkvalidity
		pcas = self.__getPrincipalComponents( 3 )
		pcaVariances, pcaSumVariances = self.__updateVariances( pcas )

		# Calculate percentage of visible variance
		percNumber = ( pcaSumVariances[2]/self.__getVariance() ) * 100
		percString = "Principal Component Analysis - ~%(perc).2f of variance visible" % {"perc": percNumber}
		
		# Create a plot figure object set visible variance at title
		fig = plot.figure()
		fig.canvas.set_window_title(percString)
		
		canvas = Axes3D(fig)
		canvas.set_xlabel( 'X - First Component' )
		canvas.set_ylabel( 'Y - Second Component' )
		canvas.set_zlabel( 'Z - Third Component' )
		
		for i in range( self.__numSamples ):
		
			marker, color = self.__getMarkerAndColor(i)
			
			if markerClasses == True:
				classMarker = self.__markerMap[marker]
			else:
				classMarker = self.__markerMap[0]
				
			if colorClasses == True:
				classColor = self.__colorMap[color]
			else:
				classColor = self.__colorMap[0]
				
			#plot the already calculated and configured point
			canvas.scatter( pcas[0][i], pcas[1][i], pcas[2][i], color=classColor, marker=classMarker )
			
		plot.show()
		
	def show4D(self, colorClasses=True, markerClasses=True):
		"""
		Displays the four principal components present on the corpus being 
		treated. The first three are shown on the X,Y and Z axis, and the fourth
		is shown in alpha-scale on each point in the graph. The proportional 
		variance visible in such components is shown on the windows title.
		
		@param colorClasses: Draw each class with a different color
		
		@param markerClasses: Draw each class with a different marker
		"""
		
		#TODO checkvalidity
		pcas = self.__getPrincipalComponents( 4 )
		pcaVariances, pcaSumVariances = self.__updateVariances( pcas )

		# Calculate percentage of visible variance
		percNumber = ( pcaSumVariances[3]/self.__getVariance() ) * 100
		percString = "Principal Component Analysis - ~%(perc).2f of variance visible" % {"perc": percNumber}
		
		# Find minimum value and range, between of all samples of the fourth PC
		min4rth = min( pcas[3] )
		length4rth = max( pcas[3] ) - min4rth
		
		# Create a plot figure object set visible variance at title
		fig = plot.figure()
		fig.canvas.set_window_title(percString)
		
		canvas = Axes3D(fig)
		canvas.set_xlabel( 'X - First Component' )
		canvas.set_ylabel( 'Y - Second Component' )
		canvas.set_zlabel( 'Z - Third Component' )
		
		for i in range( self.__numSamples ):
		
			# Set alpha scale based on fouth components min and range
			# Minimum alpha scale is set to 20%, to avoid invisible points
			alphaScale = ( (pcas[3][i] - min4rth)/length4rth ) * 0.8
			alphaScale = alphaScale.item() + 0.2
			
			marker, color = self.__getMarkerAndColor(i)
			
			if markerClasses == True:
				classMarker = self.__markerMap[marker]
			else:
				classMarker = self.__markerMap[0]
				
			if colorClasses == True:
				classColor = self.__colorMap[color]
			else:
				classColor = self.__colorMap[0]
			
			#plot the already calculated and configured point
			canvas.scatter( pcas[0][i], pcas[1][i], pcas[2][i], \
					color=classColor, marker=classMarker, alpha=alphaScale )
			
		plot.show()
		
	def showScreeplot(self,numComponents=0):
		"""
		Displays the screeplot of the principal components calculated. The
		lower line represents the proportional variance of each component, and
		the upper line represents the sum of all the variances of the previous
		components.
		
		@param numComponents: 	How many components to be calculated and 
								displayed on the screeplot. If no number is
								specified, by default the method will calculate
								all available dimensions.
		"""
		
		#TODO checkvalidity
		if numComponents == 0:
			numComponents = self.__numDimensions
			
		pcas = self.__getPrincipalComponents( numComponents )
		pcaVariances, pcaSumVariances = self.__updateVariances( pcas )
		totalVariance = self.__getVariance()

		# Calculate percentage of visible variance
		percNumber = ( pcaSumVariances[numComponents-1]/totalVariance ) * 100
		percString = "ScreePlot - ~%(perc).2f of variance visible" % {"perc": percNumber}
		
		# Create a plot figure object set visible variance at title
		fig = plot.figure()
		fig.canvas.set_window_title(percString)
		
		#plot the already calculated sequence os variances
		canvas = fig.add_subplot( 111 )
		canvas.plot( pcaVariances/totalVariance )
		canvas.plot( pcaSumVariances/totalVariance )
		
		# Customizing the grid configuration
		canvas.set_xlabel( 'Principal Component' )
		canvas.set_ylabel( 'Proportion of Variance' )
		canvas.grid( True )
			
		plot.show()
			
#>------------------------------------------------------------------------------
#> Private methods

	def __verifyCorpus( self, corpus ):
		"""
		Verifies if the loaded corpus is valid, that meaning: is a Corpus
		object inherited directly from tclass; has documents; documents are not
		empty; and number of attributes isn't larger then a manually specified
		threashold(15k), set to limit memory consumption around 2GB.
		Is the given corpus passes all previous tests, this method initializes
		the class variables.
		
		@param corpus: Group of documents to be loaded into PCA class.
		"""
		
		#verify if the corpus variable is a valid Corpus object
		if isinstance( corpus, Corpus ) == False:
				raise exception.TClassException("PCA", "__verifyCorpus", 
							   "Given 'corpus' variable is not a Corpus object")
		
		# verify if the given corpus has any documents
		classes = len( corpus._documents )
		
		if classes < 1:
			raise exception.TClassException("PCA", "__verifyCorpus", 
								"Trying to load corpus with no documents")
		
		# verify if the given corpus documents are not empty
		dimensions = 0
		samples = 0
		for i in range( classes ):
			for doc in corpus._documents[i]:
				samples = samples + 1
				for i,j in doc.iteritems():
					if i > dimensions:
						dimensions = i
					
		if dimensions < 1:
			raise exception.TClassException("PCA", "__verifyCorpus", 
							"Trying to load corpus with empty documents")
							
		# verifiy if the number of dimensions is to big, leading to cause a 
		#probable perfomance issue, depending on the machine
		if dimensions > 15000: # 15k dimensions will use aproximately 2GB of ram
			raise exception.TClassException("PCA", "__verifyCorpus", 
							"Trying to load corpus with to many attributes")
						
		# if the given corpus documents are valid, set class variables
		self.__numDimensions 	= dimensions
		self.__numSamples		= samples
		self.__numClasses		= classes
		self.__data				= np.zeros( (samples,dimensions) )
		self.__centralizedData	= np.zeros( (samples,dimensions) )
		self.__classMap			= [None]*samples
		
	def __populateData( self, corpus ):
		"""
		Populate's the corpus data adequally to the class variables, in a 
		optimized manner for the PCA calculation.
		Specifically, the classmap and the data matrix(samples x attributes).
	
		@param corpus: Group of documents to be loaded into PCA class.
		"""	
		
		currentDoc = 0
		for c in range(self.__numClasses):
			for doc in corpus._documents[c]:
				self.__classMap[currentDoc] = c
				for i,j in doc.iteritems():
					self.__data[currentDoc, (i-1)] = j
				currentDoc = currentDoc + 1
			
	def __centralizeDataMatrix( self ):
		"""
		Centralizes all of the attributes presented in the classes main data
		matrix, by subtracting each value by the mean pf its respective
		column. This way, making all components results found, relative to
		the center of the attribute universe. 
		"""
	
		means = np.mean( self.__data, axis=0 )
		for i in range( self.__numSamples ):
			for j in range( self.__numDimensions ):
				self.__centralizedData[i,j] = self.__data[i,j] - means[j,]
		
	def __setData( self, corpus ):
		"""
		This method is the first step to visualizing a Corpus principal
		components. First it verifies the integrity of the given corpus. Then,
		it populates the corpus data adequally to the class variables, in a 
		optimized manner for the PCA calculation. And for last, it centralizes
		the values of the classes main data matrix.
		This procedure is called internally in the loadCorpus method, as well
		in the _init method, in the case of the corpus being passed in the
		classes constructor.
	
		@param corpus: Group of documents to be loaded into PCA class.
		"""
	
		try:
			self.__verifyCorpus( corpus )
			
		except Exception:
			print "Unnable to set corpus data to PCA class"
			traceback.print_exc(file=sys.stdout)
			return False
			
		self.__populateData( corpus )
		self.__centralizeDataMatrix()
		
		return True
		
	def __removeDirectionVariance( self, dataMatrix, direction ):
		"""
		Removes the variance of a given direction from the temporary data
		matrix. This is called after a principal component is calculated from
		the present data, so that the next component can be found. Otherwise,
		the same component would be calculated again.
	
		@param dataMatrix: Temporary instance of the classes main data matrix.
		
		@param direction: 	Direction on which the largest amount of variance is
							obtained from the current data matrix.
		"""
		
		#obtain matrix's height and width
		h,w = dataMatrix.shape
		#create an empty column
		u = np.zeros( [1,w] )
	
		for i in range(h):
		
			#copy line i to a column vector
			for j in range(w):
				u[0,j] = dataMatrix[i,j]
			
			# calculte the direction with a scale realtive to the current data
			scalar = np.dot( u, direction )
			relativeData = direction * scalar
			
			# remove re-scaled direction from temporary data matrix
			for j in range(w):
				dataMatrix[i,j] = dataMatrix[i,j] - relativeData[j,0]
			
		return dataMatrix
		
	def __extractOptimalDirection( self, dotMatrix ):
		"""
		Return which direction in the given attribute space maximizes the
		variance of such attributes. It is this direction that will determine
		which point of view of the original data offers a more relevant
		perspective.
	
		@param dotMatrix: Square matrix, obtained from the TM x M operation.
		"""

		h,w = dotMatrix.shape
		u = np.random.rand( h, 1 )
		u = self.__normalizeVector( u )
	
		length = 0
		diff = 99
		
		while abs(diff) > 0.01:
			u = np.dot( dotMatrix, u )
	
			if length != 0:
				newLength = self.__getVectorLength( u )
				diff = newLength - length
				length = newLength
		
			else:
				length = self.__getVectorLength( u )
	
			u = self.__normalizeVector( u )
			
			if self.__verbose:
				print "Random vector streched to length ->", length[0]
		
		return u
		
	def __getPrincipalComponents( self, numDimensions ):
		"""
		Calculates and returns a given number of principal componenets from
		the classes main data matrix.
	
		@param numDimensions: The number of principal components to be calculated.
		"""
		
		#limit max principal componenets
		if numDimensions > self.__numDimensions:
			numDimensions = self.__numDimensions
	
		# create empty pc vector
		principalComponents = [None]*numDimensions
		# copy temporary dataMatrix
		dataMatrix = np.copy( self.__centralizedData )
		
		for i in range(numDimensions):
		
			if self.__verbose:
				print "\n***** Calculating principal component ", i+1, " *****"
			
			#obtain square matrix
			tmatrix = np.transpose( dataMatrix )
			dotMatrix = np.dot( tmatrix, dataMatrix )
			
			# find optimal direction, obtain pc from it, and remove its
			# direction from temporary data matrix
			direction = self.__extractOptimalDirection( dotMatrix )
			principalComponents[i] = np.dot( dataMatrix, direction )
			dataMatrix = self.__removeDirectionVariance( dataMatrix, direction )

		# delete temporary data matrix
		del dataMatrix
		
		return principalComponents
		
	def __updateVariances( self, principalComponents ):
		"""
		Returns to vectors: one containg the variance of each of the principal
		components; the other containing the sum of the current component 
		variance with all previous component variances until given point. 
	
		@param principalComponents: Matrix, where each line represents a sample,
									and each column represents a component of
									given sample where its variance is maximized.
		"""

		numComponents = len(principalComponents)
		componentVariances = [None]*numComponents
		sumVariances = [None]*numComponents
	
		for i in range(numComponents):
			componentVariances[i] = principalComponents[i].var()
		
			if i == 0:
				sumVariances[i] = componentVariances[i]
			else:
				sumVariances[i] = componentVariances[i] + sumVariances[i-1]
		
		return componentVariances, sumVariances
		
	def __getMarkerAndColor(self, sample ):
		"""
		Returns a unique combination of marker and color, based on the class
		maps to the sample given. This operation is needed, since there are only
		a limited number of markers and colors, and there is the possibility
		that a larger number of classes may be plotted. 
	
		@param sample: Index of the sample to be plotted.
		"""
	
		# marker index simply loops over the available markers
		marker = self.__classMap[sample]
		if marker >= len(self.__markerMap):
			marker = marker - len(self.__markerMap)
			
		color = self.__classMap[sample]
		# if the number of default markers != than the number of default colors,
		# just simply loop the default colors, since they will naturally
		# not be sincronized
		if len(self.__markerMap) != len(self.__colorMap):
			if color >= len(self.__colorMap):
				color = color - len(self.__colorMap)
				
		# if the number of default colors and markers is the same, force both
		# indexes to always be unsincronized
		else:
			if color >= len(self.__colorMap):
				jumps = self.__classMap[sample]/len(self.__colorMap)
				color = color + jumps
				if color >= len(self.__colorMap):
					color = color - len(self.__colorMap)
					
		return marker, color

#>------------------------------------------------------------------------------
#> Auxiliary methods
	
	def __getVariance(self):
		"""
		Returns the total variance present in a two dimensional matrix.
		"""
		
		totalVar = 0
		variances = self.__data.var( axis = 0 )
		for i in range( self.__numDimensions ):
			totalVar = totalVar + variances[i,]
		
		return totalVar
		
	def __normalizeVector( self, vec ):
		"""
		Returns the given vector normalized, with its length equal to one.
	
		@param vec: One dimensional vector.
		"""
		
		vecSum = 0
		for i in range(len(vec)):
			vecSum = vecSum + np.power( vec[i], 2 )
	
		constVec = np.sqrt( vecSum )
		for i in range(len(vec)):
			vec[i] = vec[i] / constVec
		
		return vec
		
	def __getVectorLength( self, vec ):
		"""
		Returns the given vectors length/magnitude. 
	
		@param vec: One dimensional vector.
		"""
		
		vecSum = 0
		for i in range(len(vec)):
			vecSum = vecSum + np.power( vec[i], 2 )
	
		length = np.sqrt( vecSum )
		return length

