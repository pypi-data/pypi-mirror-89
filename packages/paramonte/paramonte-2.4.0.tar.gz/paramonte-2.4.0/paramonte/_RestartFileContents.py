####################################################################################################################################
####################################################################################################################################
####
####   MIT License
####
####   ParaMonte: plain powerful parallel Monte Carlo library.
####
####   Copyright (C) 2012-present, The Computational Data Science Lab
####
####   This file is part of the ParaMonte library.
####
####   Permission is hereby granted, free of charge, to any person obtaining a 
####   copy of this software and associated documentation files (the "Software"), 
####   to deal in the Software without restriction, including without limitation 
####   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
####   and/or sell copies of the Software, and to permit persons to whom the 
####   Software is furnished to do so, subject to the following conditions:
####
####   The above copyright notice and this permission notice shall be 
####   included in all copies or substantial portions of the Software.
####
####   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
####   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
####   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
####   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
####   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
####   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
####   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
####
####   ACKNOWLEDGMENT
####
####   ParaMonte is an honor-ware and its currency is acknowledgment and citations.
####   As per the ParaMonte library license agreement terms, if you use any parts of 
####   this library for any purposes, kindly acknowledge the use of ParaMonte in your 
####   work (education/research/industry/development/...) by citing the ParaMonte 
####   library as described on this page:
####
####       https://github.com/cdslaborg/paramonte/blob/master/ACKNOWLEDGMENT.md
####
####################################################################################################################################
####################################################################################################################################

import numpy as np
import _paramonte as pm
import _CorCovMat as ccm
from _OutputFileContents import OutputFileContents
from paramonte.vis.LineScatterPlot import LineScatterPlot
from paramonte.vis.EllipsoidPlot import EllipsoidPlot

Struct = pm.Struct
newline = pm.newline

# amazingly strange. If Struct is taken from outside this module,
# it will automatically add: isParaDRAM, isParaNest, isParaTemp attributes
# print("\nself.contents.isParaDRAM: {}\n".format(self.contents.isParaDRAM))
# issue resolved: self._method = pm.Struct in _ParaMonteSampler (without parentheses, it does not instantiate).
# class Struct: pass

####################################################################################################################################
#### RestartFileContents
####################################################################################################################################

class RestartFileContents(OutputFileContents):
    """

    This is the **RestartFileContents** class for generating instances
    of the ParaMonte restart output contents. This class is NOT meant to
    be directly accessed by the ParaMonte library users. It is internally
    used by the ParaMonte library to parse the contents of the output restart
    files generated by the ParaMonte sampler routines. For example, the ParaDRAM
    sampler class makes calls to this class via its ``readRestart()`` method to
    return a list of objects of class ``RestartFileContents``.

        **Parameters**

            file

                The full path to the file containing the sample/chain.

            methodName

                A string representing the name of the ParaMonte sampler used
                to call the constructor of the ``RestartFileContents`` class.

            reportEnabled

                A logical input parameter indicating whether the ParaMonte
                automatic guidelines to the standard output should be provided 
                or not. The default value is ``True``.

        **Attributes**

            A dynamic set of attributes that are directly parsed from the file.

        **Returns**

            restartFileContents

                An object of class ``RestartFileContents``.

    ----------------------------------------------------------------------
    """

    ################################################################################################################################
    #### __init__
    ################################################################################################################################

    def __init__( self
                , file
                , methodName
                , reportEnabled
                ):

        super().__init__(file, methodName, reportEnabled)
        # superclass sets the following
        # self.file = file
        # self._methodName = methodName
        # self._reportEnabled = reportEnabled

        self.ndim = None
        self.count = None
        self.contents = None
        self._fileType = "restart"
        self._contents = []
        self._lineList = []
        self._lineListLen = []
        self.propNameList = []

        if self._methodName == pm.names.paradram:
            self._readRestartParaDRAM()
        else:
            pm.abort( msg = "Internal error occurred. Unrecognized methodName in the class \n"
                            "constructor of RestartFileContents: " + self.methodName
                    , marginTop = 1
                    , marginBot = 1
                    , methodName = "ParaMonte"
                    )

    ################################################################################################################################
    #### _readRestartParaDRAM
    ################################################################################################################################

    def _readRestartParaDRAM(self):

        # ParaDRAM field names

        self.propNameList = [ "meanAcceptanceRateSinceStart"
                            , "sampleSize"
                            , "logSqrtDeterminant"
                            , "adaptiveScaleFactorSquared"
                            , "meanVec"
                            , "covMat"
                            , "corMat"
                            ]

        ############################################################################################################################
        #### data
        ############################################################################################################################

        with open(self.file,"r") as fid: self._contents = fid.read().replace(pm.creturn,"")
        self._lineList = self._contents.split(pm.newline)
        self._lineListLen = len(self._lineList)

        # find count of updates

        self.count = self._contents.count(self.propNameList[0])

        # find ndim via meanVec entry: self.propNameList[4]

        rowOffset = 0;
        while self.propNameList[4] not in self._lineList[rowOffset]:
            rowOffset = rowOffset + 1
            if rowOffset > self._lineListLen: self._reportCorruptFile()
        rowOffset = rowOffset + 1 # the first numeric value of the meanVec

        self.ndim = 0
        while pm.utils.isNumericString( self._lineList[rowOffset+self.ndim] ): self.ndim += 1
        if self.ndim==0: self._reportCorruptFile()

        # parse the restart file contents

        fieldNamesDict =    { self.propNameList[0] : np.zeros(self.count)
                            , self.propNameList[1] : np.zeros(self.count)
                            , self.propNameList[2] : np.zeros(self.count)
                            , self.propNameList[3] : np.zeros(self.count)
                            , self.propNameList[4] : np.zeros((self.count,self.ndim))
                            , self.propNameList[5] : np.zeros((self.count,self.ndim,self.ndim))
                            , self.propNameList[6] : np.zeros((self.count,self.ndim,self.ndim))
                            }

        skip = 10 + (self.ndim * (self.ndim + 3)) // 2
        progressFraction = np.floor( self.count / 20 )
        for icount in range(self.count):

            if icount%progressFraction==0: self._progress.updateBar(icount/self.count-1)

            istart = icount * skip + 1

            rowOffset = 0
            fieldNamesDict[self.propNameList[0]][icount] = np.double( self._lineList[istart+rowOffset] )

            rowOffset = 2
            fieldNamesDict[self.propNameList[1]][icount] = np.double( self._lineList[istart+rowOffset] )

            rowOffset = 4
            fieldNamesDict[self.propNameList[2]][icount] = np.double( self._lineList[istart+rowOffset] )

            rowOffset = 6
            fieldNamesDict[self.propNameList[3]][icount] = np.double( self._lineList[istart+rowOffset] )

            rowOffset = 8
            iend = istart + rowOffset + self.ndim
            fieldNamesDict[self.propNameList[4]][icount,:] = np.double( self._lineList[istart+rowOffset:iend] )

            iend += 1 # the first numeric element of the covariance matrix
            for i in range(self.ndim): # covmat
                iPlusOne = i + 1
                istart = iend
                iend = istart + iPlusOne
                #print("\n{}".format(np.double( self._lineList[istart:iend]) ))
                fieldNamesDict[self.propNameList[5]][icount,i,0:iPlusOne] = np.double( self._lineList[istart:iend] )
                fieldNamesDict[self.propNameList[5]][icount,0:iPlusOne,i] = fieldNamesDict[self.propNameList[5]][icount,i,0:iPlusOne]

            fieldNamesDict[self.propNameList[6]][icount,:,:] = ccm.getCorFromCov( fieldNamesDict[self.propNameList[5]][icount,:,:] )

            #print("\n") # xxx
            #print(self.ndim) # xxx
            #print(self.count) # xxx
            #print(self.propNameList[0]+"\n"+str(fieldNamesDict[self.propNameList[0]][icount])) # xxx
            #print(self.propNameList[1]+"\n"+str(fieldNamesDict[self.propNameList[1]][icount])) # xxx
            #print(self.propNameList[2]+"\n"+str(fieldNamesDict[self.propNameList[2]][icount])) # xxx
            #print(self.propNameList[3]+"\n"+str(fieldNamesDict[self.propNameList[3]][icount])) # xxx
            #print(self.propNameList[4]+"\n"+str(fieldNamesDict[self.propNameList[4]][icount])) # xxx
            #print(self.propNameList[5]+"\n"+str(fieldNamesDict[self.propNameList[5]][icount,:,:])) # xxx
            #print(ccm.getCorFromCov( fieldNamesDict[self.propNameList[6]][icount,:,:] )) # xxx
            #break # xxx

        self._progress.updateBar(1)

        self.contents = Struct()
        for fieldName in self.propNameList: setattr(self.contents, fieldName, fieldNamesDict[fieldName])
        _ = fieldNamesDict.pop(self.propNameList[4])
        _ = fieldNamesDict.pop(self.propNameList[5])
        _ = fieldNamesDict.pop(self.propNameList[6]) # get rid of meanVec, covMat, corMat
        import pandas as pd
        self.df = pd.DataFrame.from_dict(fieldNamesDict)

        self._progress.note()

        ############################################################################################################################
        #### graphics
        ############################################################################################################################

        self._plotTypeList =    [ "line"
                                , "scatter"
                                , "lineScatter"
                                ]

        if self.ndim>1: self._plotTypeList +=   [ "covmat2"
                                                , "covmat3"
                                                , "cormat2"
                                                , "cormat3"
                                                ]

        self._progress.note( msg = "adding the graphics tools... ", end = newline, pre = True )
        self.plot = Struct()
        self._resetPlot(resetType="hard")
        self._progress.note()

        self.plot.reset = self._resetPlot

    ################################################################################################################################
    #### _reportCorruptFile
    ################################################################################################################################

    def _reportCorruptFile(self):
        pm.abort( msg = "The structure of the file: " + newline
                        + newline
                        + "    \"" + self.file + "\"" + newline
                        + newline
                        + "does not match a " + self._methodName + " " + self._fileType + " file." + newline
                        + "The contents of the file may have been compromised." + newline
                        + "Verify the integrity of the contents of this file before attempting to reread it."
                , marginTop = 2
                , marginBot = 1
                , methodName = self._methodName
                )

    ################################################################################################################################
    #### _resetPlot
    ################################################################################################################################

    def _resetPlot  ( self
                    , resetType = "soft"
                    , plotNames = "all"
                    ):
        """

        Reset the properties of the plot to the original default settings.
        Use this method when you change many attributes of the plot and
        you want to clean up and go back to the default settings.

            **Parameters**

                resetType (optional)

                    An optional string with possible value of ``"hard"``.
                    If provided, the plot object will be regenerated from scratch.
                    This includes reading the original data frame again and resetting
                    everything. If not provided, then only the plot settings will be
                    reset without reseting the dataFrame.

                plotNames (optional)

                    An optional string value or list of string values representing 
                    the names of plots to reset. If no value is provided, 
                    then all plots will be reset.

            **Returns**

                None

            **Example**

                .. code-block:: python

                    reset("hard")                       # regenerate all plots from scratch
                    reset("hard","covmat2")             # regenerate covmat2 plot from scratch
                    reset("hard",["covmat2","covmat3"]) # regenerate covmat2 & covmat3 plots

        """

        requestedPlotTypeList = []
        if isinstance(plotNames, str):
            plotTypeLower = plotNames.lower()
            if plotTypeLower=="all":
                requestedPlotTypeList = self._plotTypeList
            elif plotNames in self._plotTypeList:
                requestedPlotTypeList = [plotNames]
            else:
                self._reportWrongPlotName(plotNames)
        elif isinstance(plotNames, list):
            for plotName in plotNames:
                if plotName not in self._plotTypeList: self._reportWrongPlotName(plotName)
        else:
            self._reportWrongPlotName("a none-string none-list object.")

        resetTypeIsHard = None
        if isinstance(resetType, str):
            resetTypeIsHard = resetType.lower()=="hard"
        else:
            resetTypeIsHard = None
            pm.abort( msg   = "The input argument resetType must be a string representing" + newline
                            + "the type of the reset to be performed on the plots." + newline
                            + "A list of possible plots includes: \"hard\", \"soft\"" + newline
                            + "Here is the help for the ``reset()`` method: " + newline
                            + newline
                            + self._resetPlot.__doc__
                    , marginTop = 1
                    , marginBot = 1
                    , methodName = self._methodName
                    )

        ############################################################################################################################
        #### reset plots
        ############################################################################################################################

        for requestedPlotType in requestedPlotTypeList:

            plotObject = None
            requestedPlotTypeLower = requestedPlotType.lower()

           #is3d        = "3"           in requestedPlotTypeLower
            isLine      = "line"        in requestedPlotTypeLower
            isScatter   = "scatter"     in requestedPlotTypeLower
            isCovMat    = "covmat"      in requestedPlotTypeLower
            isCorMat    = "cormat"      in requestedPlotTypeLower

            if not resetTypeIsHard:
                plotComponent = getattr(self, "plot")
                plotObject = getattr(plotComponent, requestedPlotType)
                plotObject._reset()

            ########################################################################################################################
            #### reset line / scatter
            ########################################################################################################################

            if isLine or isScatter:

                if resetTypeIsHard:
                    plotObject = LineScatterPlot( plotType = requestedPlotType
                                                , dataFrame = self.df
                                                , methodName = self._methodName
                                                , reportEnabled = self._reportEnabled
                                                , resetPlot = self._resetPlot
                                                )

                if self._methodName == pm.names.paradram: plotObject.ycolumns = self.propNameList[0]
                plotObject.ccolumns = []
                plotObject.colorbar.kws.extend = "neither"
                plotObject.colorbar.kws.orientation = "vertical"
                plotObject.colorbar.kws.spacing = "uniform"

                if isLine:
                    if isScatter:
                        plotObject.lineCollection.enabled = False
                        plotObject.plot.enabled = True
                        plotObject.plot.kws.alpha = 0.2
                        plotObject.plot.kws.color = "grey"
                        plotObject.plot.kws.linewidth = 0.75
                    else:
                        plotObject.lineCollection.enabled = True
                        plotObject.plot.enabled = False

                setattr(self.plot, requestedPlotType, plotObject)

            ########################################################################################################################
            #### reset covmat / cormat
            ########################################################################################################################

            if isCovMat or isCorMat:

                if self._methodName == pm.names.paradram:

                    matrix = None
                    if isCovMat: matrix = self.contents.covMat
                    if isCorMat: matrix = self.contents.corMat

                    if resetTypeIsHard:
                        plotObject = EllipsoidPlot  ( matrix = matrix
                                                    , plotType = requestedPlotType
                                                    , methodName = self._methodName
                                                    , reportEnabled = self._reportEnabled
                                                    , resetPlot = self._resetPlot
                                                    )

                    plotObject.rows = plotObject.getLogLinSpace()
                    plotObject.center = self.contents.meanVec
                    plotObject.title.enabled = True
                    matrixType = "covariance" if isCovMat else "correlation"
                    plotObject.title.label = "Evolution of the " + matrixType + " matrices of the proposal distribution"

                    plotObject.colorbar.kws.extend = "neither"
                    plotObject.colorbar.kws.orientation = "vertical"
                    plotObject.colorbar.kws.spacing = "uniform"

                    setattr(self.plot, requestedPlotType, plotObject)

    ################################################################################################################################
