from . import _proshade

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _proshade.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self):
        return _proshade.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _proshade.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _proshade.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _proshade.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _proshade.SwigPyIterator_equal(self, x)

    def copy(self):
        return _proshade.SwigPyIterator_copy(self)

    def next(self):
        return _proshade.SwigPyIterator_next(self)

    def __next__(self):
        return _proshade.SwigPyIterator___next__(self)

    def previous(self):
        return _proshade.SwigPyIterator_previous(self)

    def advance(self, n):
        return _proshade.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _proshade.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _proshade.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _proshade.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _proshade.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _proshade.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _proshade.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _proshade.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

SHARED_PTR_DISOWN = _proshade.SHARED_PTR_DISOWN
NA = _proshade.NA
Distances = _proshade.Distances
Symmetry = _proshade.Symmetry
OverlayMap = _proshade.OverlayMap
MapManip = _proshade.MapManip
class ProSHADE_settings(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ProSHADE_settings, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ProSHADE_settings, name)
    __repr__ = _swig_repr
    __swig_setmethods__["task"] = _proshade.ProSHADE_settings_task_set
    __swig_getmethods__["task"] = _proshade.ProSHADE_settings_task_get
    if _newclass:
        task = _swig_property(_proshade.ProSHADE_settings_task_get, _proshade.ProSHADE_settings_task_set)
    __swig_setmethods__["inputFiles"] = _proshade.ProSHADE_settings_inputFiles_set
    __swig_getmethods__["inputFiles"] = _proshade.ProSHADE_settings_inputFiles_get
    if _newclass:
        inputFiles = _swig_property(_proshade.ProSHADE_settings_inputFiles_get, _proshade.ProSHADE_settings_inputFiles_set)
    __swig_setmethods__["forceP1"] = _proshade.ProSHADE_settings_forceP1_set
    __swig_getmethods__["forceP1"] = _proshade.ProSHADE_settings_forceP1_get
    if _newclass:
        forceP1 = _swig_property(_proshade.ProSHADE_settings_forceP1_get, _proshade.ProSHADE_settings_forceP1_set)
    __swig_setmethods__["removeWaters"] = _proshade.ProSHADE_settings_removeWaters_set
    __swig_getmethods__["removeWaters"] = _proshade.ProSHADE_settings_removeWaters_get
    if _newclass:
        removeWaters = _swig_property(_proshade.ProSHADE_settings_removeWaters_get, _proshade.ProSHADE_settings_removeWaters_set)
    __swig_setmethods__["firstModelOnly"] = _proshade.ProSHADE_settings_firstModelOnly_set
    __swig_getmethods__["firstModelOnly"] = _proshade.ProSHADE_settings_firstModelOnly_get
    if _newclass:
        firstModelOnly = _swig_property(_proshade.ProSHADE_settings_firstModelOnly_get, _proshade.ProSHADE_settings_firstModelOnly_set)
    __swig_setmethods__["requestedResolution"] = _proshade.ProSHADE_settings_requestedResolution_set
    __swig_getmethods__["requestedResolution"] = _proshade.ProSHADE_settings_requestedResolution_get
    if _newclass:
        requestedResolution = _swig_property(_proshade.ProSHADE_settings_requestedResolution_get, _proshade.ProSHADE_settings_requestedResolution_set)
    __swig_setmethods__["changeMapResolution"] = _proshade.ProSHADE_settings_changeMapResolution_set
    __swig_getmethods__["changeMapResolution"] = _proshade.ProSHADE_settings_changeMapResolution_get
    if _newclass:
        changeMapResolution = _swig_property(_proshade.ProSHADE_settings_changeMapResolution_get, _proshade.ProSHADE_settings_changeMapResolution_set)
    __swig_setmethods__["changeMapResolutionTriLinear"] = _proshade.ProSHADE_settings_changeMapResolutionTriLinear_set
    __swig_getmethods__["changeMapResolutionTriLinear"] = _proshade.ProSHADE_settings_changeMapResolutionTriLinear_get
    if _newclass:
        changeMapResolutionTriLinear = _swig_property(_proshade.ProSHADE_settings_changeMapResolutionTriLinear_get, _proshade.ProSHADE_settings_changeMapResolutionTriLinear_set)
    __swig_setmethods__["pdbBFactorNewVal"] = _proshade.ProSHADE_settings_pdbBFactorNewVal_set
    __swig_getmethods__["pdbBFactorNewVal"] = _proshade.ProSHADE_settings_pdbBFactorNewVal_get
    if _newclass:
        pdbBFactorNewVal = _swig_property(_proshade.ProSHADE_settings_pdbBFactorNewVal_get, _proshade.ProSHADE_settings_pdbBFactorNewVal_set)
    __swig_setmethods__["maxBandwidth"] = _proshade.ProSHADE_settings_maxBandwidth_set
    __swig_getmethods__["maxBandwidth"] = _proshade.ProSHADE_settings_maxBandwidth_get
    if _newclass:
        maxBandwidth = _swig_property(_proshade.ProSHADE_settings_maxBandwidth_get, _proshade.ProSHADE_settings_maxBandwidth_set)
    __swig_setmethods__["rotationUncertainty"] = _proshade.ProSHADE_settings_rotationUncertainty_set
    __swig_getmethods__["rotationUncertainty"] = _proshade.ProSHADE_settings_rotationUncertainty_get
    if _newclass:
        rotationUncertainty = _swig_property(_proshade.ProSHADE_settings_rotationUncertainty_get, _proshade.ProSHADE_settings_rotationUncertainty_set)
    __swig_setmethods__["usePhase"] = _proshade.ProSHADE_settings_usePhase_set
    __swig_getmethods__["usePhase"] = _proshade.ProSHADE_settings_usePhase_get
    if _newclass:
        usePhase = _swig_property(_proshade.ProSHADE_settings_usePhase_get, _proshade.ProSHADE_settings_usePhase_set)
    __swig_setmethods__["maxSphereDists"] = _proshade.ProSHADE_settings_maxSphereDists_set
    __swig_getmethods__["maxSphereDists"] = _proshade.ProSHADE_settings_maxSphereDists_get
    if _newclass:
        maxSphereDists = _swig_property(_proshade.ProSHADE_settings_maxSphereDists_get, _proshade.ProSHADE_settings_maxSphereDists_set)
    __swig_setmethods__["integOrder"] = _proshade.ProSHADE_settings_integOrder_set
    __swig_getmethods__["integOrder"] = _proshade.ProSHADE_settings_integOrder_get
    if _newclass:
        integOrder = _swig_property(_proshade.ProSHADE_settings_integOrder_get, _proshade.ProSHADE_settings_integOrder_set)
    __swig_setmethods__["taylorSeriesCap"] = _proshade.ProSHADE_settings_taylorSeriesCap_set
    __swig_getmethods__["taylorSeriesCap"] = _proshade.ProSHADE_settings_taylorSeriesCap_get
    if _newclass:
        taylorSeriesCap = _swig_property(_proshade.ProSHADE_settings_taylorSeriesCap_get, _proshade.ProSHADE_settings_taylorSeriesCap_set)
    __swig_setmethods__["normaliseMap"] = _proshade.ProSHADE_settings_normaliseMap_set
    __swig_getmethods__["normaliseMap"] = _proshade.ProSHADE_settings_normaliseMap_get
    if _newclass:
        normaliseMap = _swig_property(_proshade.ProSHADE_settings_normaliseMap_get, _proshade.ProSHADE_settings_normaliseMap_set)
    __swig_setmethods__["invertMap"] = _proshade.ProSHADE_settings_invertMap_set
    __swig_getmethods__["invertMap"] = _proshade.ProSHADE_settings_invertMap_get
    if _newclass:
        invertMap = _swig_property(_proshade.ProSHADE_settings_invertMap_get, _proshade.ProSHADE_settings_invertMap_set)
    __swig_setmethods__["blurFactor"] = _proshade.ProSHADE_settings_blurFactor_set
    __swig_getmethods__["blurFactor"] = _proshade.ProSHADE_settings_blurFactor_get
    if _newclass:
        blurFactor = _swig_property(_proshade.ProSHADE_settings_blurFactor_get, _proshade.ProSHADE_settings_blurFactor_set)
    __swig_setmethods__["maskingThresholdIQRs"] = _proshade.ProSHADE_settings_maskingThresholdIQRs_set
    __swig_getmethods__["maskingThresholdIQRs"] = _proshade.ProSHADE_settings_maskingThresholdIQRs_get
    if _newclass:
        maskingThresholdIQRs = _swig_property(_proshade.ProSHADE_settings_maskingThresholdIQRs_get, _proshade.ProSHADE_settings_maskingThresholdIQRs_set)
    __swig_setmethods__["maskMap"] = _proshade.ProSHADE_settings_maskMap_set
    __swig_getmethods__["maskMap"] = _proshade.ProSHADE_settings_maskMap_get
    if _newclass:
        maskMap = _swig_property(_proshade.ProSHADE_settings_maskMap_get, _proshade.ProSHADE_settings_maskMap_set)
    __swig_setmethods__["useCorrelationMasking"] = _proshade.ProSHADE_settings_useCorrelationMasking_set
    __swig_getmethods__["useCorrelationMasking"] = _proshade.ProSHADE_settings_useCorrelationMasking_get
    if _newclass:
        useCorrelationMasking = _swig_property(_proshade.ProSHADE_settings_useCorrelationMasking_get, _proshade.ProSHADE_settings_useCorrelationMasking_set)
    __swig_setmethods__["halfMapKernel"] = _proshade.ProSHADE_settings_halfMapKernel_set
    __swig_getmethods__["halfMapKernel"] = _proshade.ProSHADE_settings_halfMapKernel_get
    if _newclass:
        halfMapKernel = _swig_property(_proshade.ProSHADE_settings_halfMapKernel_get, _proshade.ProSHADE_settings_halfMapKernel_set)
    __swig_setmethods__["correlationKernel"] = _proshade.ProSHADE_settings_correlationKernel_set
    __swig_getmethods__["correlationKernel"] = _proshade.ProSHADE_settings_correlationKernel_get
    if _newclass:
        correlationKernel = _swig_property(_proshade.ProSHADE_settings_correlationKernel_get, _proshade.ProSHADE_settings_correlationKernel_set)
    __swig_setmethods__["saveMask"] = _proshade.ProSHADE_settings_saveMask_set
    __swig_getmethods__["saveMask"] = _proshade.ProSHADE_settings_saveMask_get
    if _newclass:
        saveMask = _swig_property(_proshade.ProSHADE_settings_saveMask_get, _proshade.ProSHADE_settings_saveMask_set)
    __swig_setmethods__["maskFileName"] = _proshade.ProSHADE_settings_maskFileName_set
    __swig_getmethods__["maskFileName"] = _proshade.ProSHADE_settings_maskFileName_get
    if _newclass:
        maskFileName = _swig_property(_proshade.ProSHADE_settings_maskFileName_get, _proshade.ProSHADE_settings_maskFileName_set)
    __swig_setmethods__["reBoxMap"] = _proshade.ProSHADE_settings_reBoxMap_set
    __swig_getmethods__["reBoxMap"] = _proshade.ProSHADE_settings_reBoxMap_get
    if _newclass:
        reBoxMap = _swig_property(_proshade.ProSHADE_settings_reBoxMap_get, _proshade.ProSHADE_settings_reBoxMap_set)
    __swig_setmethods__["boundsExtraSpace"] = _proshade.ProSHADE_settings_boundsExtraSpace_set
    __swig_getmethods__["boundsExtraSpace"] = _proshade.ProSHADE_settings_boundsExtraSpace_get
    if _newclass:
        boundsExtraSpace = _swig_property(_proshade.ProSHADE_settings_boundsExtraSpace_get, _proshade.ProSHADE_settings_boundsExtraSpace_set)
    __swig_setmethods__["boundsSimilarityThreshold"] = _proshade.ProSHADE_settings_boundsSimilarityThreshold_set
    __swig_getmethods__["boundsSimilarityThreshold"] = _proshade.ProSHADE_settings_boundsSimilarityThreshold_get
    if _newclass:
        boundsSimilarityThreshold = _swig_property(_proshade.ProSHADE_settings_boundsSimilarityThreshold_get, _proshade.ProSHADE_settings_boundsSimilarityThreshold_set)
    __swig_setmethods__["useSameBounds"] = _proshade.ProSHADE_settings_useSameBounds_set
    __swig_getmethods__["useSameBounds"] = _proshade.ProSHADE_settings_useSameBounds_get
    if _newclass:
        useSameBounds = _swig_property(_proshade.ProSHADE_settings_useSameBounds_get, _proshade.ProSHADE_settings_useSameBounds_set)
    __swig_setmethods__["forceBounds"] = _proshade.ProSHADE_settings_forceBounds_set
    __swig_getmethods__["forceBounds"] = _proshade.ProSHADE_settings_forceBounds_get
    if _newclass:
        forceBounds = _swig_property(_proshade.ProSHADE_settings_forceBounds_get, _proshade.ProSHADE_settings_forceBounds_set)
    __swig_setmethods__["moveToCOM"] = _proshade.ProSHADE_settings_moveToCOM_set
    __swig_getmethods__["moveToCOM"] = _proshade.ProSHADE_settings_moveToCOM_get
    if _newclass:
        moveToCOM = _swig_property(_proshade.ProSHADE_settings_moveToCOM_get, _proshade.ProSHADE_settings_moveToCOM_set)
    __swig_setmethods__["addExtraSpace"] = _proshade.ProSHADE_settings_addExtraSpace_set
    __swig_getmethods__["addExtraSpace"] = _proshade.ProSHADE_settings_addExtraSpace_get
    if _newclass:
        addExtraSpace = _swig_property(_proshade.ProSHADE_settings_addExtraSpace_get, _proshade.ProSHADE_settings_addExtraSpace_set)
    __swig_setmethods__["progressiveSphereMapping"] = _proshade.ProSHADE_settings_progressiveSphereMapping_set
    __swig_getmethods__["progressiveSphereMapping"] = _proshade.ProSHADE_settings_progressiveSphereMapping_get
    if _newclass:
        progressiveSphereMapping = _swig_property(_proshade.ProSHADE_settings_progressiveSphereMapping_get, _proshade.ProSHADE_settings_progressiveSphereMapping_set)
    __swig_setmethods__["outName"] = _proshade.ProSHADE_settings_outName_set
    __swig_getmethods__["outName"] = _proshade.ProSHADE_settings_outName_get
    if _newclass:
        outName = _swig_property(_proshade.ProSHADE_settings_outName_get, _proshade.ProSHADE_settings_outName_set)
    __swig_setmethods__["computeEnergyLevelsDesc"] = _proshade.ProSHADE_settings_computeEnergyLevelsDesc_set
    __swig_getmethods__["computeEnergyLevelsDesc"] = _proshade.ProSHADE_settings_computeEnergyLevelsDesc_get
    if _newclass:
        computeEnergyLevelsDesc = _swig_property(_proshade.ProSHADE_settings_computeEnergyLevelsDesc_get, _proshade.ProSHADE_settings_computeEnergyLevelsDesc_set)
    __swig_setmethods__["enLevMatrixPowerWeight"] = _proshade.ProSHADE_settings_enLevMatrixPowerWeight_set
    __swig_getmethods__["enLevMatrixPowerWeight"] = _proshade.ProSHADE_settings_enLevMatrixPowerWeight_get
    if _newclass:
        enLevMatrixPowerWeight = _swig_property(_proshade.ProSHADE_settings_enLevMatrixPowerWeight_get, _proshade.ProSHADE_settings_enLevMatrixPowerWeight_set)
    __swig_setmethods__["computeTraceSigmaDesc"] = _proshade.ProSHADE_settings_computeTraceSigmaDesc_set
    __swig_getmethods__["computeTraceSigmaDesc"] = _proshade.ProSHADE_settings_computeTraceSigmaDesc_get
    if _newclass:
        computeTraceSigmaDesc = _swig_property(_proshade.ProSHADE_settings_computeTraceSigmaDesc_get, _proshade.ProSHADE_settings_computeTraceSigmaDesc_set)
    __swig_setmethods__["computeRotationFuncDesc"] = _proshade.ProSHADE_settings_computeRotationFuncDesc_set
    __swig_getmethods__["computeRotationFuncDesc"] = _proshade.ProSHADE_settings_computeRotationFuncDesc_get
    if _newclass:
        computeRotationFuncDesc = _swig_property(_proshade.ProSHADE_settings_computeRotationFuncDesc_get, _proshade.ProSHADE_settings_computeRotationFuncDesc_set)
    __swig_setmethods__["peakNeighbours"] = _proshade.ProSHADE_settings_peakNeighbours_set
    __swig_getmethods__["peakNeighbours"] = _proshade.ProSHADE_settings_peakNeighbours_get
    if _newclass:
        peakNeighbours = _swig_property(_proshade.ProSHADE_settings_peakNeighbours_get, _proshade.ProSHADE_settings_peakNeighbours_set)
    __swig_setmethods__["noIQRsFromMedianNaivePeak"] = _proshade.ProSHADE_settings_noIQRsFromMedianNaivePeak_set
    __swig_getmethods__["noIQRsFromMedianNaivePeak"] = _proshade.ProSHADE_settings_noIQRsFromMedianNaivePeak_get
    if _newclass:
        noIQRsFromMedianNaivePeak = _swig_property(_proshade.ProSHADE_settings_noIQRsFromMedianNaivePeak_get, _proshade.ProSHADE_settings_noIQRsFromMedianNaivePeak_set)
    __swig_setmethods__["smoothingFactor"] = _proshade.ProSHADE_settings_smoothingFactor_set
    __swig_getmethods__["smoothingFactor"] = _proshade.ProSHADE_settings_smoothingFactor_get
    if _newclass:
        smoothingFactor = _swig_property(_proshade.ProSHADE_settings_smoothingFactor_get, _proshade.ProSHADE_settings_smoothingFactor_set)
    __swig_setmethods__["symMissPeakThres"] = _proshade.ProSHADE_settings_symMissPeakThres_set
    __swig_getmethods__["symMissPeakThres"] = _proshade.ProSHADE_settings_symMissPeakThres_get
    if _newclass:
        symMissPeakThres = _swig_property(_proshade.ProSHADE_settings_symMissPeakThres_get, _proshade.ProSHADE_settings_symMissPeakThres_set)
    __swig_setmethods__["axisErrTolerance"] = _proshade.ProSHADE_settings_axisErrTolerance_set
    __swig_getmethods__["axisErrTolerance"] = _proshade.ProSHADE_settings_axisErrTolerance_get
    if _newclass:
        axisErrTolerance = _swig_property(_proshade.ProSHADE_settings_axisErrTolerance_get, _proshade.ProSHADE_settings_axisErrTolerance_set)
    __swig_setmethods__["axisErrToleranceDefault"] = _proshade.ProSHADE_settings_axisErrToleranceDefault_set
    __swig_getmethods__["axisErrToleranceDefault"] = _proshade.ProSHADE_settings_axisErrToleranceDefault_get
    if _newclass:
        axisErrToleranceDefault = _swig_property(_proshade.ProSHADE_settings_axisErrToleranceDefault_get, _proshade.ProSHADE_settings_axisErrToleranceDefault_set)
    __swig_setmethods__["minSymPeak"] = _proshade.ProSHADE_settings_minSymPeak_set
    __swig_getmethods__["minSymPeak"] = _proshade.ProSHADE_settings_minSymPeak_get
    if _newclass:
        minSymPeak = _swig_property(_proshade.ProSHADE_settings_minSymPeak_get, _proshade.ProSHADE_settings_minSymPeak_set)
    __swig_setmethods__["recommendedSymmetryType"] = _proshade.ProSHADE_settings_recommendedSymmetryType_set
    __swig_getmethods__["recommendedSymmetryType"] = _proshade.ProSHADE_settings_recommendedSymmetryType_get
    if _newclass:
        recommendedSymmetryType = _swig_property(_proshade.ProSHADE_settings_recommendedSymmetryType_get, _proshade.ProSHADE_settings_recommendedSymmetryType_set)
    __swig_setmethods__["recommendedSymmetryFold"] = _proshade.ProSHADE_settings_recommendedSymmetryFold_set
    __swig_getmethods__["recommendedSymmetryFold"] = _proshade.ProSHADE_settings_recommendedSymmetryFold_get
    if _newclass:
        recommendedSymmetryFold = _swig_property(_proshade.ProSHADE_settings_recommendedSymmetryFold_get, _proshade.ProSHADE_settings_recommendedSymmetryFold_set)
    __swig_setmethods__["requestedSymmetryType"] = _proshade.ProSHADE_settings_requestedSymmetryType_set
    __swig_getmethods__["requestedSymmetryType"] = _proshade.ProSHADE_settings_requestedSymmetryType_get
    if _newclass:
        requestedSymmetryType = _swig_property(_proshade.ProSHADE_settings_requestedSymmetryType_get, _proshade.ProSHADE_settings_requestedSymmetryType_set)
    __swig_setmethods__["requestedSymmetryFold"] = _proshade.ProSHADE_settings_requestedSymmetryFold_set
    __swig_getmethods__["requestedSymmetryFold"] = _proshade.ProSHADE_settings_requestedSymmetryFold_get
    if _newclass:
        requestedSymmetryFold = _swig_property(_proshade.ProSHADE_settings_requestedSymmetryFold_get, _proshade.ProSHADE_settings_requestedSymmetryFold_set)
    __swig_setmethods__["usePeakSearchInRotationFunctionSpace"] = _proshade.ProSHADE_settings_usePeakSearchInRotationFunctionSpace_set
    __swig_getmethods__["usePeakSearchInRotationFunctionSpace"] = _proshade.ProSHADE_settings_usePeakSearchInRotationFunctionSpace_get
    if _newclass:
        usePeakSearchInRotationFunctionSpace = _swig_property(_proshade.ProSHADE_settings_usePeakSearchInRotationFunctionSpace_get, _proshade.ProSHADE_settings_usePeakSearchInRotationFunctionSpace_set)
    __swig_setmethods__["useBiCubicInterpolationOnPeaks"] = _proshade.ProSHADE_settings_useBiCubicInterpolationOnPeaks_set
    __swig_getmethods__["useBiCubicInterpolationOnPeaks"] = _proshade.ProSHADE_settings_useBiCubicInterpolationOnPeaks_get
    if _newclass:
        useBiCubicInterpolationOnPeaks = _swig_property(_proshade.ProSHADE_settings_useBiCubicInterpolationOnPeaks_get, _proshade.ProSHADE_settings_useBiCubicInterpolationOnPeaks_set)
    __swig_setmethods__["maxSymmetryFold"] = _proshade.ProSHADE_settings_maxSymmetryFold_set
    __swig_getmethods__["maxSymmetryFold"] = _proshade.ProSHADE_settings_maxSymmetryFold_get
    if _newclass:
        maxSymmetryFold = _swig_property(_proshade.ProSHADE_settings_maxSymmetryFold_get, _proshade.ProSHADE_settings_maxSymmetryFold_set)
    __swig_setmethods__["overlayStructureName"] = _proshade.ProSHADE_settings_overlayStructureName_set
    __swig_getmethods__["overlayStructureName"] = _proshade.ProSHADE_settings_overlayStructureName_get
    if _newclass:
        overlayStructureName = _swig_property(_proshade.ProSHADE_settings_overlayStructureName_get, _proshade.ProSHADE_settings_overlayStructureName_set)
    __swig_setmethods__["rotTrsJSONFile"] = _proshade.ProSHADE_settings_rotTrsJSONFile_set
    __swig_getmethods__["rotTrsJSONFile"] = _proshade.ProSHADE_settings_rotTrsJSONFile_get
    if _newclass:
        rotTrsJSONFile = _swig_property(_proshade.ProSHADE_settings_rotTrsJSONFile_get, _proshade.ProSHADE_settings_rotTrsJSONFile_set)
    __swig_setmethods__["verbose"] = _proshade.ProSHADE_settings_verbose_set
    __swig_getmethods__["verbose"] = _proshade.ProSHADE_settings_verbose_get
    if _newclass:
        verbose = _swig_property(_proshade.ProSHADE_settings_verbose_get, _proshade.ProSHADE_settings_verbose_set)
    __swig_setmethods__["detectedSymmetry"] = _proshade.ProSHADE_settings_detectedSymmetry_set
    __swig_getmethods__["detectedSymmetry"] = _proshade.ProSHADE_settings_detectedSymmetry_get
    if _newclass:
        detectedSymmetry = _swig_property(_proshade.ProSHADE_settings_detectedSymmetry_get, _proshade.ProSHADE_settings_detectedSymmetry_set)
    __swig_setmethods__["allDetectedCAxes"] = _proshade.ProSHADE_settings_allDetectedCAxes_set
    __swig_getmethods__["allDetectedCAxes"] = _proshade.ProSHADE_settings_allDetectedCAxes_get
    if _newclass:
        allDetectedCAxes = _swig_property(_proshade.ProSHADE_settings_allDetectedCAxes_get, _proshade.ProSHADE_settings_allDetectedCAxes_set)
    __swig_setmethods__["allDetectedDAxes"] = _proshade.ProSHADE_settings_allDetectedDAxes_set
    __swig_getmethods__["allDetectedDAxes"] = _proshade.ProSHADE_settings_allDetectedDAxes_get
    if _newclass:
        allDetectedDAxes = _swig_property(_proshade.ProSHADE_settings_allDetectedDAxes_get, _proshade.ProSHADE_settings_allDetectedDAxes_set)
    __swig_setmethods__["allDetectedTAxes"] = _proshade.ProSHADE_settings_allDetectedTAxes_set
    __swig_getmethods__["allDetectedTAxes"] = _proshade.ProSHADE_settings_allDetectedTAxes_get
    if _newclass:
        allDetectedTAxes = _swig_property(_proshade.ProSHADE_settings_allDetectedTAxes_get, _proshade.ProSHADE_settings_allDetectedTAxes_set)
    __swig_setmethods__["allDetectedOAxes"] = _proshade.ProSHADE_settings_allDetectedOAxes_set
    __swig_getmethods__["allDetectedOAxes"] = _proshade.ProSHADE_settings_allDetectedOAxes_get
    if _newclass:
        allDetectedOAxes = _swig_property(_proshade.ProSHADE_settings_allDetectedOAxes_get, _proshade.ProSHADE_settings_allDetectedOAxes_set)
    __swig_setmethods__["allDetectedIAxes"] = _proshade.ProSHADE_settings_allDetectedIAxes_set
    __swig_getmethods__["allDetectedIAxes"] = _proshade.ProSHADE_settings_allDetectedIAxes_get
    if _newclass:
        allDetectedIAxes = _swig_property(_proshade.ProSHADE_settings_allDetectedIAxes_get, _proshade.ProSHADE_settings_allDetectedIAxes_set)

    def getListOfNonCSymmetryAxesIndicesLength(self):
        return _proshade.ProSHADE_settings_getListOfNonCSymmetryAxesIndicesLength(self)

    def getListOfNonCSymmetryAxesIndices(self, allOtherDetectedSymsIndices):
        return _proshade.ProSHADE_settings_getListOfNonCSymmetryAxesIndices(self, allOtherDetectedSymsIndices)

    def determineBandwidthFromAngle(self, uncertainty):
        return _proshade.ProSHADE_settings_determineBandwidthFromAngle(self, uncertainty)

    def determineBandwidth(self, circumference):
        return _proshade.ProSHADE_settings_determineBandwidth(self, circumference)

    def determineSphereDistances(self, maxMapRange):
        return _proshade.ProSHADE_settings_determineSphereDistances(self, maxMapRange)

    def determineIntegrationOrder(self, maxMapRange):
        return _proshade.ProSHADE_settings_determineIntegrationOrder(self, maxMapRange)

    def determineAllSHValues(self, xDim, yDim, zDim):
        return _proshade.ProSHADE_settings_determineAllSHValues(self, xDim, yDim, zDim)

    def setVariablesLeftOnAuto(self):
        return _proshade.ProSHADE_settings_setVariablesLeftOnAuto(self)

    def __init__(self, *args):
        this = _proshade.new_ProSHADE_settings(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _proshade.delete_ProSHADE_settings
    __del__ = lambda self: None

    def addStructure(self, structure):
        return _proshade.ProSHADE_settings_addStructure(self, structure)

    def setResolution(self, resolution):
        return _proshade.ProSHADE_settings_setResolution(self, resolution)

    def setPDBBFactor(self, newBF):
        return _proshade.ProSHADE_settings_setPDBBFactor(self, newBF)

    def setNormalisation(self, normalise):
        return _proshade.ProSHADE_settings_setNormalisation(self, normalise)

    def setMapInversion(self, mInv):
        return _proshade.ProSHADE_settings_setMapInversion(self, mInv)

    def setVerbosity(self, verbosity):
        return _proshade.ProSHADE_settings_setVerbosity(self, verbosity)

    def setMaskBlurFactor(self, blurFac):
        return _proshade.ProSHADE_settings_setMaskBlurFactor(self, blurFac)

    def setMaskIQR(self, noIQRs):
        return _proshade.ProSHADE_settings_setMaskIQR(self, noIQRs)

    def setMasking(self, mask):
        return _proshade.ProSHADE_settings_setMasking(self, mask)

    def setCorrelationMasking(self, corMask):
        return _proshade.ProSHADE_settings_setCorrelationMasking(self, corMask)

    def setTypicalNoiseSize(self, typNoi):
        return _proshade.ProSHADE_settings_setTypicalNoiseSize(self, typNoi)

    def setMinimumMaskSize(self, minMS):
        return _proshade.ProSHADE_settings_setMinimumMaskSize(self, minMS)

    def setMaskSaving(self, savMsk):
        return _proshade.ProSHADE_settings_setMaskSaving(self, savMsk)

    def setMaskFilename(self, mskFln):
        return _proshade.ProSHADE_settings_setMaskFilename(self, mskFln)

    def setMapReboxing(self, reBx):
        return _proshade.ProSHADE_settings_setMapReboxing(self, reBx)

    def setBoundsSpace(self, boundsExSp):
        return _proshade.ProSHADE_settings_setBoundsSpace(self, boundsExSp)

    def setBoundsThreshold(self, boundsThres):
        return _proshade.ProSHADE_settings_setBoundsThreshold(self, boundsThres)

    def setSameBoundaries(self, sameB):
        return _proshade.ProSHADE_settings_setSameBoundaries(self, sameB)

    def setOutputFilename(self, oFileName):
        return _proshade.ProSHADE_settings_setOutputFilename(self, oFileName)

    def setMapResolutionChange(self, mrChange):
        return _proshade.ProSHADE_settings_setMapResolutionChange(self, mrChange)

    def setMapResolutionChangeTriLinear(self, mrChange):
        return _proshade.ProSHADE_settings_setMapResolutionChangeTriLinear(self, mrChange)

    def setMapCentering(self, com):
        return _proshade.ProSHADE_settings_setMapCentering(self, com)

    def setExtraSpace(self, exSpace):
        return _proshade.ProSHADE_settings_setExtraSpace(self, exSpace)

    def setBandwidth(self, band):
        return _proshade.ProSHADE_settings_setBandwidth(self, band)

    def setSphereDistances(self, sphDist):
        return _proshade.ProSHADE_settings_setSphereDistances(self, sphDist)

    def setIntegrationOrder(self, intOrd):
        return _proshade.ProSHADE_settings_setIntegrationOrder(self, intOrd)

    def setTaylorSeriesCap(self, tayCap):
        return _proshade.ProSHADE_settings_setTaylorSeriesCap(self, tayCap)

    def setProgressiveSphereMapping(self, progSphMap):
        return _proshade.ProSHADE_settings_setProgressiveSphereMapping(self, progSphMap)

    def setEnergyLevelsComputation(self, enLevDesc):
        return _proshade.ProSHADE_settings_setEnergyLevelsComputation(self, enLevDesc)

    def setTraceSigmaComputation(self, trSigVal):
        return _proshade.ProSHADE_settings_setTraceSigmaComputation(self, trSigVal)

    def setRotationFunctionComputation(self, rotfVal):
        return _proshade.ProSHADE_settings_setRotationFunctionComputation(self, rotfVal)

    def setPeakNeighboursNumber(self, pkS):
        return _proshade.ProSHADE_settings_setPeakNeighboursNumber(self, pkS)

    def setPeakNaiveNoIQR(self, noIQRs):
        return _proshade.ProSHADE_settings_setPeakNaiveNoIQR(self, noIQRs)

    def setPhaseUsage(self, phaseUsage):
        return _proshade.ProSHADE_settings_setPhaseUsage(self, phaseUsage)

    def setEnLevShellWeight(self, mPower):
        return _proshade.ProSHADE_settings_setEnLevShellWeight(self, mPower)

    def setGroupingSmoothingFactor(self, smFact):
        return _proshade.ProSHADE_settings_setGroupingSmoothingFactor(self, smFact)

    def setMissingPeakThreshold(self, mpThres):
        return _proshade.ProSHADE_settings_setMissingPeakThreshold(self, mpThres)

    def setAxisComparisonThreshold(self, axThres):
        return _proshade.ProSHADE_settings_setAxisComparisonThreshold(self, axThres)

    def setAxisComparisonThresholdBehaviour(self, behav):
        return _proshade.ProSHADE_settings_setAxisComparisonThresholdBehaviour(self, behav)

    def setMinimumPeakForAxis(self, minSP):
        return _proshade.ProSHADE_settings_setMinimumPeakForAxis(self, minSP)

    def setRecommendedSymmetry(self, val):
        return _proshade.ProSHADE_settings_setRecommendedSymmetry(self, val)

    def setRecommendedFold(self, val):
        return _proshade.ProSHADE_settings_setRecommendedFold(self, val)

    def setRequestedSymmetry(self, val):
        return _proshade.ProSHADE_settings_setRequestedSymmetry(self, val)

    def setRequestedFold(self, val):
        return _proshade.ProSHADE_settings_setRequestedFold(self, val)

    def setDetectedSymmetry(self, sym):
        return _proshade.ProSHADE_settings_setDetectedSymmetry(self, sym)

    def setOverlaySaveFile(self, filename):
        return _proshade.ProSHADE_settings_setOverlaySaveFile(self, filename)

    def setOverlayJsonFile(self, filename):
        return _proshade.ProSHADE_settings_setOverlayJsonFile(self, filename)

    def setSymmetryRotFunPeaks(self, rotFunPeaks):
        return _proshade.ProSHADE_settings_setSymmetryRotFunPeaks(self, rotFunPeaks)

    def setBicubicInterpolationSearch(self, bicubPeaks):
        return _proshade.ProSHADE_settings_setBicubicInterpolationSearch(self, bicubPeaks)

    def setMaxSymmetryFold(self, maxFold):
        return _proshade.ProSHADE_settings_setMaxSymmetryFold(self, maxFold)

    def getCommandLineParams(self, argc, argv):
        return _proshade.ProSHADE_settings_getCommandLineParams(self, argc, argv)

    def printSettings(self):
        return _proshade.ProSHADE_settings_printSettings(self)
ProSHADE_settings_swigregister = _proshade.ProSHADE_settings_swigregister
ProSHADE_settings_swigregister(ProSHADE_settings)

UNKNOWN = _proshade.UNKNOWN
PDB = _proshade.PDB
MAP = _proshade.MAP

def figureDataType(fName):
    return _proshade.figureDataType(fName)
figureDataType = _proshade.figureDataType

def isFilePDB(fName):
    return _proshade.isFilePDB(fName)
isFilePDB = _proshade.isFilePDB

def isFileMAP(fName):
    return _proshade.isFileMAP(fName)
isFileMAP = _proshade.isFileMAP

def readInMapHeader(map, xDimInds, yDimInds, zDimInds, xDim, yDim, zDim, aAng, bAng, cAng, xFrom, yFrom, zFrom, xAxOrigin, yAxOrigin, zAxOrigin, xAxOrder, yAxOrder, zAxOrder, xGridInds, yGridInds, zGridInds):
    return _proshade.readInMapHeader(map, xDimInds, yDimInds, zDimInds, xDim, yDim, zDim, aAng, bAng, cAng, xFrom, yFrom, zFrom, xAxOrigin, yAxOrigin, zAxOrigin, xAxOrder, yAxOrder, zAxOrder, xGridInds, yGridInds, zGridInds)
readInMapHeader = _proshade.readInMapHeader

def readInMapData(gemmiMap, map, xDimInds, yDimInds, zDimInds, xAxOrder, yAxOrder, zAxOrder):
    return _proshade.readInMapData(gemmiMap, map, xDimInds, yDimInds, zDimInds, xAxOrder, yAxOrder, zAxOrder)
readInMapData = _proshade.readInMapData

def writeOutMapHeader(map, xDimInds, yDimInds, zDimInds, xDim, yDim, zDim, aAng, bAng, cAng, xFrom, yFrom, zFrom, xAxOrigin, yAxOrigin, zAxOrigin, xAxOrder, yAxOrder, zAxOrder, xGridInds, yGridInds, zGridInds, title, mode):
    return _proshade.writeOutMapHeader(map, xDimInds, yDimInds, zDimInds, xDim, yDim, zDim, aAng, bAng, cAng, xFrom, yFrom, zFrom, xAxOrigin, yAxOrigin, zAxOrigin, xAxOrder, yAxOrder, zAxOrder, xGridInds, yGridInds, zGridInds, title, mode)
writeOutMapHeader = _proshade.writeOutMapHeader

def writeRotationTranslationJSON(trsX1, trsY1, trsZ1, eulA, eulB, eulG, trsX2, trsY2, trsZ2, xMapCen, yMapCen, zMapCen, fileName):
    return _proshade.writeRotationTranslationJSON(trsX1, trsY1, trsZ1, eulA, eulB, eulG, trsX2, trsY2, trsZ2, xMapCen, yMapCen, zMapCen, fileName)
writeRotationTranslationJSON = _proshade.writeRotationTranslationJSON
class ProSHADE_data(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ProSHADE_data, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ProSHADE_data, name)
    __repr__ = _swig_repr
    __swig_setmethods__["fileName"] = _proshade.ProSHADE_data_fileName_set
    __swig_getmethods__["fileName"] = _proshade.ProSHADE_data_fileName_get
    if _newclass:
        fileName = _swig_property(_proshade.ProSHADE_data_fileName_get, _proshade.ProSHADE_data_fileName_set)
    __swig_setmethods__["fileType"] = _proshade.ProSHADE_data_fileType_set
    __swig_getmethods__["fileType"] = _proshade.ProSHADE_data_fileType_get
    if _newclass:
        fileType = _swig_property(_proshade.ProSHADE_data_fileType_get, _proshade.ProSHADE_data_fileType_set)
    __swig_setmethods__["internalMap"] = _proshade.ProSHADE_data_internalMap_set
    __swig_getmethods__["internalMap"] = _proshade.ProSHADE_data_internalMap_get
    if _newclass:
        internalMap = _swig_property(_proshade.ProSHADE_data_internalMap_get, _proshade.ProSHADE_data_internalMap_set)
    __swig_setmethods__["xDimSize"] = _proshade.ProSHADE_data_xDimSize_set
    __swig_getmethods__["xDimSize"] = _proshade.ProSHADE_data_xDimSize_get
    if _newclass:
        xDimSize = _swig_property(_proshade.ProSHADE_data_xDimSize_get, _proshade.ProSHADE_data_xDimSize_set)
    __swig_setmethods__["yDimSize"] = _proshade.ProSHADE_data_yDimSize_set
    __swig_getmethods__["yDimSize"] = _proshade.ProSHADE_data_yDimSize_get
    if _newclass:
        yDimSize = _swig_property(_proshade.ProSHADE_data_yDimSize_get, _proshade.ProSHADE_data_yDimSize_set)
    __swig_setmethods__["zDimSize"] = _proshade.ProSHADE_data_zDimSize_set
    __swig_getmethods__["zDimSize"] = _proshade.ProSHADE_data_zDimSize_get
    if _newclass:
        zDimSize = _swig_property(_proshade.ProSHADE_data_zDimSize_get, _proshade.ProSHADE_data_zDimSize_set)
    __swig_setmethods__["aAngle"] = _proshade.ProSHADE_data_aAngle_set
    __swig_getmethods__["aAngle"] = _proshade.ProSHADE_data_aAngle_get
    if _newclass:
        aAngle = _swig_property(_proshade.ProSHADE_data_aAngle_get, _proshade.ProSHADE_data_aAngle_set)
    __swig_setmethods__["bAngle"] = _proshade.ProSHADE_data_bAngle_set
    __swig_getmethods__["bAngle"] = _proshade.ProSHADE_data_bAngle_get
    if _newclass:
        bAngle = _swig_property(_proshade.ProSHADE_data_bAngle_get, _proshade.ProSHADE_data_bAngle_set)
    __swig_setmethods__["cAngle"] = _proshade.ProSHADE_data_cAngle_set
    __swig_getmethods__["cAngle"] = _proshade.ProSHADE_data_cAngle_get
    if _newclass:
        cAngle = _swig_property(_proshade.ProSHADE_data_cAngle_get, _proshade.ProSHADE_data_cAngle_set)
    __swig_setmethods__["xDimIndices"] = _proshade.ProSHADE_data_xDimIndices_set
    __swig_getmethods__["xDimIndices"] = _proshade.ProSHADE_data_xDimIndices_get
    if _newclass:
        xDimIndices = _swig_property(_proshade.ProSHADE_data_xDimIndices_get, _proshade.ProSHADE_data_xDimIndices_set)
    __swig_setmethods__["yDimIndices"] = _proshade.ProSHADE_data_yDimIndices_set
    __swig_getmethods__["yDimIndices"] = _proshade.ProSHADE_data_yDimIndices_get
    if _newclass:
        yDimIndices = _swig_property(_proshade.ProSHADE_data_yDimIndices_get, _proshade.ProSHADE_data_yDimIndices_set)
    __swig_setmethods__["zDimIndices"] = _proshade.ProSHADE_data_zDimIndices_set
    __swig_getmethods__["zDimIndices"] = _proshade.ProSHADE_data_zDimIndices_get
    if _newclass:
        zDimIndices = _swig_property(_proshade.ProSHADE_data_zDimIndices_get, _proshade.ProSHADE_data_zDimIndices_set)
    __swig_setmethods__["xGridIndices"] = _proshade.ProSHADE_data_xGridIndices_set
    __swig_getmethods__["xGridIndices"] = _proshade.ProSHADE_data_xGridIndices_get
    if _newclass:
        xGridIndices = _swig_property(_proshade.ProSHADE_data_xGridIndices_get, _proshade.ProSHADE_data_xGridIndices_set)
    __swig_setmethods__["yGridIndices"] = _proshade.ProSHADE_data_yGridIndices_set
    __swig_getmethods__["yGridIndices"] = _proshade.ProSHADE_data_yGridIndices_get
    if _newclass:
        yGridIndices = _swig_property(_proshade.ProSHADE_data_yGridIndices_get, _proshade.ProSHADE_data_yGridIndices_set)
    __swig_setmethods__["zGridIndices"] = _proshade.ProSHADE_data_zGridIndices_set
    __swig_getmethods__["zGridIndices"] = _proshade.ProSHADE_data_zGridIndices_get
    if _newclass:
        zGridIndices = _swig_property(_proshade.ProSHADE_data_zGridIndices_get, _proshade.ProSHADE_data_zGridIndices_set)
    __swig_setmethods__["xAxisOrder"] = _proshade.ProSHADE_data_xAxisOrder_set
    __swig_getmethods__["xAxisOrder"] = _proshade.ProSHADE_data_xAxisOrder_get
    if _newclass:
        xAxisOrder = _swig_property(_proshade.ProSHADE_data_xAxisOrder_get, _proshade.ProSHADE_data_xAxisOrder_set)
    __swig_setmethods__["yAxisOrder"] = _proshade.ProSHADE_data_yAxisOrder_set
    __swig_getmethods__["yAxisOrder"] = _proshade.ProSHADE_data_yAxisOrder_get
    if _newclass:
        yAxisOrder = _swig_property(_proshade.ProSHADE_data_yAxisOrder_get, _proshade.ProSHADE_data_yAxisOrder_set)
    __swig_setmethods__["zAxisOrder"] = _proshade.ProSHADE_data_zAxisOrder_set
    __swig_getmethods__["zAxisOrder"] = _proshade.ProSHADE_data_zAxisOrder_get
    if _newclass:
        zAxisOrder = _swig_property(_proshade.ProSHADE_data_zAxisOrder_get, _proshade.ProSHADE_data_zAxisOrder_set)
    __swig_setmethods__["xAxisOrigin"] = _proshade.ProSHADE_data_xAxisOrigin_set
    __swig_getmethods__["xAxisOrigin"] = _proshade.ProSHADE_data_xAxisOrigin_get
    if _newclass:
        xAxisOrigin = _swig_property(_proshade.ProSHADE_data_xAxisOrigin_get, _proshade.ProSHADE_data_xAxisOrigin_set)
    __swig_setmethods__["yAxisOrigin"] = _proshade.ProSHADE_data_yAxisOrigin_set
    __swig_getmethods__["yAxisOrigin"] = _proshade.ProSHADE_data_yAxisOrigin_get
    if _newclass:
        yAxisOrigin = _swig_property(_proshade.ProSHADE_data_yAxisOrigin_get, _proshade.ProSHADE_data_yAxisOrigin_set)
    __swig_setmethods__["zAxisOrigin"] = _proshade.ProSHADE_data_zAxisOrigin_set
    __swig_getmethods__["zAxisOrigin"] = _proshade.ProSHADE_data_zAxisOrigin_get
    if _newclass:
        zAxisOrigin = _swig_property(_proshade.ProSHADE_data_zAxisOrigin_get, _proshade.ProSHADE_data_zAxisOrigin_set)
    __swig_setmethods__["comMovX"] = _proshade.ProSHADE_data_comMovX_set
    __swig_getmethods__["comMovX"] = _proshade.ProSHADE_data_comMovX_get
    if _newclass:
        comMovX = _swig_property(_proshade.ProSHADE_data_comMovX_get, _proshade.ProSHADE_data_comMovX_set)
    __swig_setmethods__["comMovY"] = _proshade.ProSHADE_data_comMovY_set
    __swig_getmethods__["comMovY"] = _proshade.ProSHADE_data_comMovY_get
    if _newclass:
        comMovY = _swig_property(_proshade.ProSHADE_data_comMovY_get, _proshade.ProSHADE_data_comMovY_set)
    __swig_setmethods__["comMovZ"] = _proshade.ProSHADE_data_comMovZ_set
    __swig_getmethods__["comMovZ"] = _proshade.ProSHADE_data_comMovZ_get
    if _newclass:
        comMovZ = _swig_property(_proshade.ProSHADE_data_comMovZ_get, _proshade.ProSHADE_data_comMovZ_set)
    __swig_setmethods__["xCom"] = _proshade.ProSHADE_data_xCom_set
    __swig_getmethods__["xCom"] = _proshade.ProSHADE_data_xCom_get
    if _newclass:
        xCom = _swig_property(_proshade.ProSHADE_data_xCom_get, _proshade.ProSHADE_data_xCom_set)
    __swig_setmethods__["yCom"] = _proshade.ProSHADE_data_yCom_set
    __swig_getmethods__["yCom"] = _proshade.ProSHADE_data_yCom_get
    if _newclass:
        yCom = _swig_property(_proshade.ProSHADE_data_yCom_get, _proshade.ProSHADE_data_yCom_set)
    __swig_setmethods__["zCom"] = _proshade.ProSHADE_data_zCom_set
    __swig_getmethods__["zCom"] = _proshade.ProSHADE_data_zCom_get
    if _newclass:
        zCom = _swig_property(_proshade.ProSHADE_data_zCom_get, _proshade.ProSHADE_data_zCom_set)
    __swig_setmethods__["xDimSizeOriginal"] = _proshade.ProSHADE_data_xDimSizeOriginal_set
    __swig_getmethods__["xDimSizeOriginal"] = _proshade.ProSHADE_data_xDimSizeOriginal_get
    if _newclass:
        xDimSizeOriginal = _swig_property(_proshade.ProSHADE_data_xDimSizeOriginal_get, _proshade.ProSHADE_data_xDimSizeOriginal_set)
    __swig_setmethods__["yDimSizeOriginal"] = _proshade.ProSHADE_data_yDimSizeOriginal_set
    __swig_getmethods__["yDimSizeOriginal"] = _proshade.ProSHADE_data_yDimSizeOriginal_get
    if _newclass:
        yDimSizeOriginal = _swig_property(_proshade.ProSHADE_data_yDimSizeOriginal_get, _proshade.ProSHADE_data_yDimSizeOriginal_set)
    __swig_setmethods__["zDimSizeOriginal"] = _proshade.ProSHADE_data_zDimSizeOriginal_set
    __swig_getmethods__["zDimSizeOriginal"] = _proshade.ProSHADE_data_zDimSizeOriginal_get
    if _newclass:
        zDimSizeOriginal = _swig_property(_proshade.ProSHADE_data_zDimSizeOriginal_get, _proshade.ProSHADE_data_zDimSizeOriginal_set)
    __swig_setmethods__["xDimIndicesOriginal"] = _proshade.ProSHADE_data_xDimIndicesOriginal_set
    __swig_getmethods__["xDimIndicesOriginal"] = _proshade.ProSHADE_data_xDimIndicesOriginal_get
    if _newclass:
        xDimIndicesOriginal = _swig_property(_proshade.ProSHADE_data_xDimIndicesOriginal_get, _proshade.ProSHADE_data_xDimIndicesOriginal_set)
    __swig_setmethods__["yDimIndicesOriginal"] = _proshade.ProSHADE_data_yDimIndicesOriginal_set
    __swig_getmethods__["yDimIndicesOriginal"] = _proshade.ProSHADE_data_yDimIndicesOriginal_get
    if _newclass:
        yDimIndicesOriginal = _swig_property(_proshade.ProSHADE_data_yDimIndicesOriginal_get, _proshade.ProSHADE_data_yDimIndicesOriginal_set)
    __swig_setmethods__["zDimIndicesOriginal"] = _proshade.ProSHADE_data_zDimIndicesOriginal_set
    __swig_getmethods__["zDimIndicesOriginal"] = _proshade.ProSHADE_data_zDimIndicesOriginal_get
    if _newclass:
        zDimIndicesOriginal = _swig_property(_proshade.ProSHADE_data_zDimIndicesOriginal_get, _proshade.ProSHADE_data_zDimIndicesOriginal_set)
    __swig_setmethods__["xAxisOriginOriginal"] = _proshade.ProSHADE_data_xAxisOriginOriginal_set
    __swig_getmethods__["xAxisOriginOriginal"] = _proshade.ProSHADE_data_xAxisOriginOriginal_get
    if _newclass:
        xAxisOriginOriginal = _swig_property(_proshade.ProSHADE_data_xAxisOriginOriginal_get, _proshade.ProSHADE_data_xAxisOriginOriginal_set)
    __swig_setmethods__["yAxisOriginOriginal"] = _proshade.ProSHADE_data_yAxisOriginOriginal_set
    __swig_getmethods__["yAxisOriginOriginal"] = _proshade.ProSHADE_data_yAxisOriginOriginal_get
    if _newclass:
        yAxisOriginOriginal = _swig_property(_proshade.ProSHADE_data_yAxisOriginOriginal_get, _proshade.ProSHADE_data_yAxisOriginOriginal_set)
    __swig_setmethods__["zAxisOriginOriginal"] = _proshade.ProSHADE_data_zAxisOriginOriginal_set
    __swig_getmethods__["zAxisOriginOriginal"] = _proshade.ProSHADE_data_zAxisOriginOriginal_get
    if _newclass:
        zAxisOriginOriginal = _swig_property(_proshade.ProSHADE_data_zAxisOriginOriginal_get, _proshade.ProSHADE_data_zAxisOriginOriginal_set)
    __swig_setmethods__["originalMapXCom"] = _proshade.ProSHADE_data_originalMapXCom_set
    __swig_getmethods__["originalMapXCom"] = _proshade.ProSHADE_data_originalMapXCom_get
    if _newclass:
        originalMapXCom = _swig_property(_proshade.ProSHADE_data_originalMapXCom_get, _proshade.ProSHADE_data_originalMapXCom_set)
    __swig_setmethods__["originalMapYCom"] = _proshade.ProSHADE_data_originalMapYCom_set
    __swig_getmethods__["originalMapYCom"] = _proshade.ProSHADE_data_originalMapYCom_get
    if _newclass:
        originalMapYCom = _swig_property(_proshade.ProSHADE_data_originalMapYCom_get, _proshade.ProSHADE_data_originalMapYCom_set)
    __swig_setmethods__["originalMapZCom"] = _proshade.ProSHADE_data_originalMapZCom_set
    __swig_getmethods__["originalMapZCom"] = _proshade.ProSHADE_data_originalMapZCom_get
    if _newclass:
        originalMapZCom = _swig_property(_proshade.ProSHADE_data_originalMapZCom_get, _proshade.ProSHADE_data_originalMapZCom_set)
    __swig_setmethods__["mapPostRotXCom"] = _proshade.ProSHADE_data_mapPostRotXCom_set
    __swig_getmethods__["mapPostRotXCom"] = _proshade.ProSHADE_data_mapPostRotXCom_get
    if _newclass:
        mapPostRotXCom = _swig_property(_proshade.ProSHADE_data_mapPostRotXCom_get, _proshade.ProSHADE_data_mapPostRotXCom_set)
    __swig_setmethods__["mapPostRotYCom"] = _proshade.ProSHADE_data_mapPostRotYCom_set
    __swig_getmethods__["mapPostRotYCom"] = _proshade.ProSHADE_data_mapPostRotYCom_get
    if _newclass:
        mapPostRotYCom = _swig_property(_proshade.ProSHADE_data_mapPostRotYCom_get, _proshade.ProSHADE_data_mapPostRotYCom_set)
    __swig_setmethods__["mapPostRotZCom"] = _proshade.ProSHADE_data_mapPostRotZCom_set
    __swig_getmethods__["mapPostRotZCom"] = _proshade.ProSHADE_data_mapPostRotZCom_get
    if _newclass:
        mapPostRotZCom = _swig_property(_proshade.ProSHADE_data_mapPostRotZCom_get, _proshade.ProSHADE_data_mapPostRotZCom_set)
    __swig_setmethods__["originalPdbRotCenX"] = _proshade.ProSHADE_data_originalPdbRotCenX_set
    __swig_getmethods__["originalPdbRotCenX"] = _proshade.ProSHADE_data_originalPdbRotCenX_get
    if _newclass:
        originalPdbRotCenX = _swig_property(_proshade.ProSHADE_data_originalPdbRotCenX_get, _proshade.ProSHADE_data_originalPdbRotCenX_set)
    __swig_setmethods__["originalPdbRotCenY"] = _proshade.ProSHADE_data_originalPdbRotCenY_set
    __swig_getmethods__["originalPdbRotCenY"] = _proshade.ProSHADE_data_originalPdbRotCenY_get
    if _newclass:
        originalPdbRotCenY = _swig_property(_proshade.ProSHADE_data_originalPdbRotCenY_get, _proshade.ProSHADE_data_originalPdbRotCenY_set)
    __swig_setmethods__["originalPdbRotCenZ"] = _proshade.ProSHADE_data_originalPdbRotCenZ_set
    __swig_getmethods__["originalPdbRotCenZ"] = _proshade.ProSHADE_data_originalPdbRotCenZ_get
    if _newclass:
        originalPdbRotCenZ = _swig_property(_proshade.ProSHADE_data_originalPdbRotCenZ_get, _proshade.ProSHADE_data_originalPdbRotCenZ_set)
    __swig_setmethods__["originalPdbTransX"] = _proshade.ProSHADE_data_originalPdbTransX_set
    __swig_getmethods__["originalPdbTransX"] = _proshade.ProSHADE_data_originalPdbTransX_get
    if _newclass:
        originalPdbTransX = _swig_property(_proshade.ProSHADE_data_originalPdbTransX_get, _proshade.ProSHADE_data_originalPdbTransX_set)
    __swig_setmethods__["originalPdbTransY"] = _proshade.ProSHADE_data_originalPdbTransY_set
    __swig_getmethods__["originalPdbTransY"] = _proshade.ProSHADE_data_originalPdbTransY_get
    if _newclass:
        originalPdbTransY = _swig_property(_proshade.ProSHADE_data_originalPdbTransY_get, _proshade.ProSHADE_data_originalPdbTransY_set)
    __swig_setmethods__["originalPdbTransZ"] = _proshade.ProSHADE_data_originalPdbTransZ_set
    __swig_getmethods__["originalPdbTransZ"] = _proshade.ProSHADE_data_originalPdbTransZ_get
    if _newclass:
        originalPdbTransZ = _swig_property(_proshade.ProSHADE_data_originalPdbTransZ_get, _proshade.ProSHADE_data_originalPdbTransZ_set)
    __swig_setmethods__["xFrom"] = _proshade.ProSHADE_data_xFrom_set
    __swig_getmethods__["xFrom"] = _proshade.ProSHADE_data_xFrom_get
    if _newclass:
        xFrom = _swig_property(_proshade.ProSHADE_data_xFrom_get, _proshade.ProSHADE_data_xFrom_set)
    __swig_setmethods__["yFrom"] = _proshade.ProSHADE_data_yFrom_set
    __swig_getmethods__["yFrom"] = _proshade.ProSHADE_data_yFrom_get
    if _newclass:
        yFrom = _swig_property(_proshade.ProSHADE_data_yFrom_get, _proshade.ProSHADE_data_yFrom_set)
    __swig_setmethods__["zFrom"] = _proshade.ProSHADE_data_zFrom_set
    __swig_getmethods__["zFrom"] = _proshade.ProSHADE_data_zFrom_get
    if _newclass:
        zFrom = _swig_property(_proshade.ProSHADE_data_zFrom_get, _proshade.ProSHADE_data_zFrom_set)
    __swig_setmethods__["xTo"] = _proshade.ProSHADE_data_xTo_set
    __swig_getmethods__["xTo"] = _proshade.ProSHADE_data_xTo_get
    if _newclass:
        xTo = _swig_property(_proshade.ProSHADE_data_xTo_get, _proshade.ProSHADE_data_xTo_set)
    __swig_setmethods__["yTo"] = _proshade.ProSHADE_data_yTo_set
    __swig_getmethods__["yTo"] = _proshade.ProSHADE_data_yTo_get
    if _newclass:
        yTo = _swig_property(_proshade.ProSHADE_data_yTo_get, _proshade.ProSHADE_data_yTo_set)
    __swig_setmethods__["zTo"] = _proshade.ProSHADE_data_zTo_set
    __swig_getmethods__["zTo"] = _proshade.ProSHADE_data_zTo_get
    if _newclass:
        zTo = _swig_property(_proshade.ProSHADE_data_zTo_get, _proshade.ProSHADE_data_zTo_set)
    __swig_setmethods__["spherePos"] = _proshade.ProSHADE_data_spherePos_set
    __swig_getmethods__["spherePos"] = _proshade.ProSHADE_data_spherePos_get
    if _newclass:
        spherePos = _swig_property(_proshade.ProSHADE_data_spherePos_get, _proshade.ProSHADE_data_spherePos_set)
    __swig_setmethods__["noSpheres"] = _proshade.ProSHADE_data_noSpheres_set
    __swig_getmethods__["noSpheres"] = _proshade.ProSHADE_data_noSpheres_get
    if _newclass:
        noSpheres = _swig_property(_proshade.ProSHADE_data_noSpheres_get, _proshade.ProSHADE_data_noSpheres_set)
    __swig_setmethods__["spheres"] = _proshade.ProSHADE_data_spheres_set
    __swig_getmethods__["spheres"] = _proshade.ProSHADE_data_spheres_get
    if _newclass:
        spheres = _swig_property(_proshade.ProSHADE_data_spheres_get, _proshade.ProSHADE_data_spheres_set)
    __swig_setmethods__["sphericalHarmonics"] = _proshade.ProSHADE_data_sphericalHarmonics_set
    __swig_getmethods__["sphericalHarmonics"] = _proshade.ProSHADE_data_sphericalHarmonics_get
    if _newclass:
        sphericalHarmonics = _swig_property(_proshade.ProSHADE_data_sphericalHarmonics_get, _proshade.ProSHADE_data_sphericalHarmonics_set)
    __swig_setmethods__["rotSphericalHarmonics"] = _proshade.ProSHADE_data_rotSphericalHarmonics_set
    __swig_getmethods__["rotSphericalHarmonics"] = _proshade.ProSHADE_data_rotSphericalHarmonics_get
    if _newclass:
        rotSphericalHarmonics = _swig_property(_proshade.ProSHADE_data_rotSphericalHarmonics_get, _proshade.ProSHADE_data_rotSphericalHarmonics_set)
    __swig_setmethods__["maxShellBand"] = _proshade.ProSHADE_data_maxShellBand_set
    __swig_getmethods__["maxShellBand"] = _proshade.ProSHADE_data_maxShellBand_get
    if _newclass:
        maxShellBand = _swig_property(_proshade.ProSHADE_data_maxShellBand_get, _proshade.ProSHADE_data_maxShellBand_set)
    __swig_setmethods__["rrpMatrices"] = _proshade.ProSHADE_data_rrpMatrices_set
    __swig_getmethods__["rrpMatrices"] = _proshade.ProSHADE_data_rrpMatrices_get
    if _newclass:
        rrpMatrices = _swig_property(_proshade.ProSHADE_data_rrpMatrices_get, _proshade.ProSHADE_data_rrpMatrices_set)
    __swig_setmethods__["eMatrices"] = _proshade.ProSHADE_data_eMatrices_set
    __swig_getmethods__["eMatrices"] = _proshade.ProSHADE_data_eMatrices_get
    if _newclass:
        eMatrices = _swig_property(_proshade.ProSHADE_data_eMatrices_get, _proshade.ProSHADE_data_eMatrices_set)
    __swig_setmethods__["integrationWeight"] = _proshade.ProSHADE_data_integrationWeight_set
    __swig_getmethods__["integrationWeight"] = _proshade.ProSHADE_data_integrationWeight_get
    if _newclass:
        integrationWeight = _swig_property(_proshade.ProSHADE_data_integrationWeight_get, _proshade.ProSHADE_data_integrationWeight_set)
    __swig_setmethods__["so3Coeffs"] = _proshade.ProSHADE_data_so3Coeffs_set
    __swig_getmethods__["so3Coeffs"] = _proshade.ProSHADE_data_so3Coeffs_get
    if _newclass:
        so3Coeffs = _swig_property(_proshade.ProSHADE_data_so3Coeffs_get, _proshade.ProSHADE_data_so3Coeffs_set)
    __swig_setmethods__["so3CoeffsInverse"] = _proshade.ProSHADE_data_so3CoeffsInverse_set
    __swig_getmethods__["so3CoeffsInverse"] = _proshade.ProSHADE_data_so3CoeffsInverse_get
    if _newclass:
        so3CoeffsInverse = _swig_property(_proshade.ProSHADE_data_so3CoeffsInverse_get, _proshade.ProSHADE_data_so3CoeffsInverse_set)
    __swig_setmethods__["wignerMatrices"] = _proshade.ProSHADE_data_wignerMatrices_set
    __swig_getmethods__["wignerMatrices"] = _proshade.ProSHADE_data_wignerMatrices_get
    if _newclass:
        wignerMatrices = _swig_property(_proshade.ProSHADE_data_wignerMatrices_get, _proshade.ProSHADE_data_wignerMatrices_set)
    __swig_setmethods__["maxCompBand"] = _proshade.ProSHADE_data_maxCompBand_set
    __swig_getmethods__["maxCompBand"] = _proshade.ProSHADE_data_maxCompBand_get
    if _newclass:
        maxCompBand = _swig_property(_proshade.ProSHADE_data_maxCompBand_get, _proshade.ProSHADE_data_maxCompBand_set)
    __swig_setmethods__["translationMap"] = _proshade.ProSHADE_data_translationMap_set
    __swig_getmethods__["translationMap"] = _proshade.ProSHADE_data_translationMap_get
    if _newclass:
        translationMap = _swig_property(_proshade.ProSHADE_data_translationMap_get, _proshade.ProSHADE_data_translationMap_set)
    __swig_setmethods__["sphereMappedRotFun"] = _proshade.ProSHADE_data_sphereMappedRotFun_set
    __swig_getmethods__["sphereMappedRotFun"] = _proshade.ProSHADE_data_sphereMappedRotFun_get
    if _newclass:
        sphereMappedRotFun = _swig_property(_proshade.ProSHADE_data_sphereMappedRotFun_get, _proshade.ProSHADE_data_sphereMappedRotFun_set)
    __swig_setmethods__["isEmpty"] = _proshade.ProSHADE_data_isEmpty_set
    __swig_getmethods__["isEmpty"] = _proshade.ProSHADE_data_isEmpty_get
    if _newclass:
        isEmpty = _swig_property(_proshade.ProSHADE_data_isEmpty_get, _proshade.ProSHADE_data_isEmpty_set)
    __swig_setmethods__["inputOrder"] = _proshade.ProSHADE_data_inputOrder_set
    __swig_getmethods__["inputOrder"] = _proshade.ProSHADE_data_inputOrder_get
    if _newclass:
        inputOrder = _swig_property(_proshade.ProSHADE_data_inputOrder_get, _proshade.ProSHADE_data_inputOrder_set)

    def __init__(self, *args):
        this = _proshade.new_ProSHADE_data(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _proshade.delete_ProSHADE_data
    __del__ = lambda self: None

    def readInStructure(self, fName, inputO, settings):
        return _proshade.ProSHADE_data_readInStructure(self, fName, inputO, settings)

    def writeMap(self, *args):
        return _proshade.ProSHADE_data_writeMap(self, *args)

    def writePdb(self, fName, euA=0.0, euB=0.0, euG=0.0, transX=0.0, transY=0.0, transZ=0.0, firstModel=True):
        return _proshade.ProSHADE_data_writePdb(self, fName, euA, euB, euG, transX, transY, transZ, firstModel)

    def writeMask(self, fName, mask):
        return _proshade.ProSHADE_data_writeMask(self, fName, mask)

    def getMapArraySizePython(self):
        return _proshade.ProSHADE_data_getMapArraySizePython(self)

    def getMapPython(self, mapArrayPython):
        return _proshade.ProSHADE_data_getMapPython(self, mapArrayPython)

    def setMapPython(self, mapChangedInPython):
        return _proshade.ProSHADE_data_setMapPython(self, mapChangedInPython)

    def setNewMapPython(self, mapChangedInPython):
        return _proshade.ProSHADE_data_setNewMapPython(self, mapChangedInPython)

    def invertMirrorMap(self, settings):
        return _proshade.ProSHADE_data_invertMirrorMap(self, settings)

    def normaliseMap(self, settings):
        return _proshade.ProSHADE_data_normaliseMap(self, settings)

    def maskMap(self, settings):
        return _proshade.ProSHADE_data_maskMap(self, settings)

    def getReBoxBoundaries(self, settings, ret):
        return _proshade.ProSHADE_data_getReBoxBoundaries(self, settings, ret)

    def getReBoxBoundariesPy(self, settings, reBoxBounds):
        return _proshade.ProSHADE_data_getReBoxBoundariesPy(self, settings, reBoxBounds)

    def createNewMapFromBounds(self, settings, newStr, newBounds):
        return _proshade.ProSHADE_data_createNewMapFromBounds(self, settings, newStr, newBounds)

    def createNewMapFromBoundsPy(self, settings, newStr, newBounds):
        return _proshade.ProSHADE_data_createNewMapFromBoundsPy(self, settings, newStr, newBounds)

    def reSampleMap(self, settings):
        return _proshade.ProSHADE_data_reSampleMap(self, settings)

    def centreMapOnCOM(self, settings):
        return _proshade.ProSHADE_data_centreMapOnCOM(self, settings)

    def addExtraSpace(self, settings):
        return _proshade.ProSHADE_data_addExtraSpace(self, settings)

    def removePhaseInormation(self, settings):
        return _proshade.ProSHADE_data_removePhaseInormation(self, settings)

    def processInternalMap(self, settings):
        return _proshade.ProSHADE_data_processInternalMap(self, settings)

    def getSpherePositions(self, settings):
        return _proshade.ProSHADE_data_getSpherePositions(self, settings)

    def mapToSpheres(self, settings):
        return _proshade.ProSHADE_data_mapToSpheres(self, settings)

    def computeSphericalHarmonics(self, settings):
        return _proshade.ProSHADE_data_computeSphericalHarmonics(self, settings)

    def getRealSphericalHarmonicsForShell(self, shellNo, verbose, sphericalHarmsReal):
        return _proshade.ProSHADE_data_getRealSphericalHarmonicsForShell(self, shellNo, verbose, sphericalHarmsReal)

    def getImagSphericalHarmonicsForShell(self, shellNo, verbose, sphericalHarmsImag):
        return _proshade.ProSHADE_data_getImagSphericalHarmonicsForShell(self, shellNo, verbose, sphericalHarmsImag)

    def sphericalHarmonicsIndex(self, order, band, shell):
        return _proshade.ProSHADE_data_sphericalHarmonicsIndex(self, order, band, shell)

    def getSphericalHarmonicsLenForShell(self, shellNo, verbose):
        return _proshade.ProSHADE_data_getSphericalHarmonicsLenForShell(self, shellNo, verbose)

    def shellBandExists(self, shell, bandVal):
        return _proshade.ProSHADE_data_shellBandExists(self, shell, bandVal)

    def computeRRPMatrices(self, settings):
        return _proshade.ProSHADE_data_computeRRPMatrices(self, settings)

    def allocateEMatrices(self, settings, band):
        return _proshade.ProSHADE_data_allocateEMatrices(self, settings, band)

    def allocateSO3CoeffsSpace(self, band):
        return _proshade.ProSHADE_data_allocateSO3CoeffsSpace(self, band)

    def allocateWignerMatricesSpace(self, settings):
        return _proshade.ProSHADE_data_allocateWignerMatricesSpace(self, settings)

    def getRotationFunction(self, settings):
        return _proshade.ProSHADE_data_getRotationFunction(self, settings)

    def convertRotationFunction(self, settings):
        return _proshade.ProSHADE_data_convertRotationFunction(self, settings)

    def getRealEMatrixValuesForLM(self, band, order1, eMatsLMReal):
        return _proshade.ProSHADE_data_getRealEMatrixValuesForLM(self, band, order1, eMatsLMReal)

    def getImagEMatrixValuesForLM(self, band, order1, eMatsLMImag):
        return _proshade.ProSHADE_data_getImagEMatrixValuesForLM(self, band, order1, eMatsLMImag)

    def getRealSO3Coeffs(self, so3CoefsReal):
        return _proshade.ProSHADE_data_getRealSO3Coeffs(self, so3CoefsReal)

    def getImagSO3Coeffs(self, so3CoefsImag):
        return _proshade.ProSHADE_data_getImagSO3Coeffs(self, so3CoefsImag)

    def getRealRotFunction(self, rotFunReal):
        return _proshade.ProSHADE_data_getRealRotFunction(self, rotFunReal)

    def getImagRotFunction(self, rotFunImag):
        return _proshade.ProSHADE_data_getImagRotFunction(self, rotFunImag)

    def getRealTranslationFunction(self, trsFunReal):
        return _proshade.ProSHADE_data_getRealTranslationFunction(self, trsFunReal)

    def getImagTranslationFunction(self, trsFunImag):
        return _proshade.ProSHADE_data_getImagTranslationFunction(self, trsFunImag)

    def getRotMatrixFromRotFunInds(self, aI, bI, gI, rotMat):
        return _proshade.ProSHADE_data_getRotMatrixFromRotFunInds(self, aI, bI, gI, rotMat)

    def so3CoeffsArrayIndex(self, order1, order2, band):
        return _proshade.ProSHADE_data_so3CoeffsArrayIndex(self, order1, order2, band)

    def getCyclicSymmetriesList(self, settings):
        return _proshade.ProSHADE_data_getCyclicSymmetriesList(self, settings)

    def getDihedralSymmetriesList(self, settings, CSymList):
        return _proshade.ProSHADE_data_getDihedralSymmetriesList(self, settings, CSymList)

    def getTetrahedralSymmetriesList(self, settings, CSymList):
        return _proshade.ProSHADE_data_getTetrahedralSymmetriesList(self, settings, CSymList)

    def getOctahedralSymmetriesList(self, settings, CSymList):
        return _proshade.ProSHADE_data_getOctahedralSymmetriesList(self, settings, CSymList)

    def getIcosahedralSymmetriesList(self, settings, CSymList):
        return _proshade.ProSHADE_data_getIcosahedralSymmetriesList(self, settings, CSymList)

    def getPredictedIcosahedralSymmetriesList(self, settings, CSymList):
        return _proshade.ProSHADE_data_getPredictedIcosahedralSymmetriesList(self, settings, CSymList)

    def detectSymmetryInStructure(self, settings, axes, allCs):
        return _proshade.ProSHADE_data_detectSymmetryInStructure(self, settings, axes, allCs)

    def detectSymmetryInStructurePython(self, settings):
        return _proshade.ProSHADE_data_detectSymmetryInStructurePython(self, settings)

    def detectSymmetryFromAngleAxisSpace(self, settings, axes, allCs):
        return _proshade.ProSHADE_data_detectSymmetryFromAngleAxisSpace(self, settings, axes, allCs)

    def getCyclicSymmetriesListFromAngleAxis(self, settings):
        return _proshade.ProSHADE_data_getCyclicSymmetriesListFromAngleAxis(self, settings)

    def findRequestedCSymmetryFromAngleAxis(self, settings, fold, peakThres):
        return _proshade.ProSHADE_data_findRequestedCSymmetryFromAngleAxis(self, settings, fold, peakThres)

    def saveDetectedSymmetries(self, settings, CSyms, allCs):
        return _proshade.ProSHADE_data_saveDetectedSymmetries(self, settings, CSyms, allCs)

    def getRecommendedSymmetryType(self, settings):
        return _proshade.ProSHADE_data_getRecommendedSymmetryType(self, settings)

    def getRecommendedSymmetryFold(self, settings):
        return _proshade.ProSHADE_data_getRecommendedSymmetryFold(self, settings)

    def getNoRecommendedSymmetryAxes(self, settings):
        return _proshade.ProSHADE_data_getNoRecommendedSymmetryAxes(self, settings)

    def getAllSymsOneArrayLength(self, settings):
        return _proshade.ProSHADE_data_getAllSymsOneArrayLength(self, settings)

    def getSymmetryAxis(self, settings, axisNo):
        return _proshade.ProSHADE_data_getSymmetryAxis(self, settings, axisNo)

    def findBestCScore(self, CSym, symInd):
        return _proshade.ProSHADE_data_findBestCScore(self, CSym, symInd)

    def findBestDScore(self, DSym, symInd):
        return _proshade.ProSHADE_data_findBestDScore(self, DSym, symInd)

    def findTScore(self, TSym):
        return _proshade.ProSHADE_data_findTScore(self, TSym)

    def findOScore(self, OSym):
        return _proshade.ProSHADE_data_findOScore(self, OSym)

    def findIScore(self, ISym):
        return _proshade.ProSHADE_data_findIScore(self, ISym)

    def saveRecommendedSymmetry(self, settings, CSym, DSym, TSym, OSym, ISym, axes):
        return _proshade.ProSHADE_data_saveRecommendedSymmetry(self, settings, CSym, DSym, TSym, OSym, ISym, axes)

    def saveRequestedSymmetryC(self, settings, CSym, axes):
        return _proshade.ProSHADE_data_saveRequestedSymmetryC(self, settings, CSym, axes)

    def saveRequestedSymmetryD(self, settings, DSym, axes):
        return _proshade.ProSHADE_data_saveRequestedSymmetryD(self, settings, DSym, axes)

    def computeGroupElementsForGroup(self, *args):
        return _proshade.ProSHADE_data_computeGroupElementsForGroup(self, *args)

    def getAllGroupElements(self, *args):
        return _proshade.ProSHADE_data_getAllGroupElements(self, *args)

    def getAllGroupElementsLength(self, settings, grIndices, groupType):
        return _proshade.ProSHADE_data_getAllGroupElementsLength(self, settings, grIndices, groupType)

    def getAllGroupElementsPython(self, settings, grIndices, groupType, allGroupElement):
        return _proshade.ProSHADE_data_getAllGroupElementsPython(self, settings, grIndices, groupType, allGroupElement)

    def getCGroupElementsLength(self, settings, grPosition):
        return _proshade.ProSHADE_data_getCGroupElementsLength(self, settings, grPosition)

    def getCGroupElementsPython(self, settings, groupElements, grPosition):
        return _proshade.ProSHADE_data_getCGroupElementsPython(self, settings, groupElements, grPosition)

    def reportSymmetryResults(self, settings):
        return _proshade.ProSHADE_data_reportSymmetryResults(self, settings)

    def getOverlayRotationFunction(self, settings, obj2):
        return _proshade.ProSHADE_data_getOverlayRotationFunction(self, settings, obj2)

    def getBestRotationMapPeaksEulerAngles(self, settings):
        return _proshade.ProSHADE_data_getBestRotationMapPeaksEulerAngles(self, settings)

    def getBestTranslationMapPeaksAngstrom(self, staticStructure):
        return _proshade.ProSHADE_data_getBestTranslationMapPeaksAngstrom(self, staticStructure)

    def zeroPaddToDims(self, xDim, yDim, zDim):
        return _proshade.ProSHADE_data_zeroPaddToDims(self, xDim, yDim, zDim)

    def rotateMap(self, settings, eulerAlpha, eulerBeta, eulerGamma):
        return _proshade.ProSHADE_data_rotateMap(self, settings, eulerAlpha, eulerBeta, eulerGamma)

    def translateMap(self, settings, trsX, trsY, trsZ):
        return _proshade.ProSHADE_data_translateMap(self, settings, trsX, trsY, trsZ)

    def allocateRotatedSHMemory(self, settings):
        return _proshade.ProSHADE_data_allocateRotatedSHMemory(self, settings)

    def computeRotatedSH(self, settings):
        return _proshade.ProSHADE_data_computeRotatedSH(self, settings)

    def invertSHCoefficients(self):
        return _proshade.ProSHADE_data_invertSHCoefficients(self)

    def interpolateMapFromSpheres(self, settings, densityMapRotated):
        return _proshade.ProSHADE_data_interpolateMapFromSpheres(self, settings, densityMapRotated)

    def computeTranslationMap(self, obj1):
        return _proshade.ProSHADE_data_computeTranslationMap(self, obj1)

    def findMapCOM(self):
        return _proshade.ProSHADE_data_findMapCOM(self)

    def computeOverlayTranslations(self, rcX, rcY, rcZ, transX, transY, transZ):
        return _proshade.ProSHADE_data_computeOverlayTranslations(self, rcX, rcY, rcZ, transX, transY, transZ)

    def writeOutOverlayFiles(self, settings, trsX, trsY, trsZ, eulA, eulB, eulG, rotCentre, ultimateTranslation):
        return _proshade.ProSHADE_data_writeOutOverlayFiles(self, settings, trsX, trsY, trsZ, eulA, eulB, eulG, rotCentre, ultimateTranslation)

    def reportOverlayResults(self, settings, rotationCentre, mapBoxMovement, eulerAngles, finalTranslation):
        return _proshade.ProSHADE_data_reportOverlayResults(self, settings, rotationCentre, mapBoxMovement, eulerAngles, finalTranslation)

    def deepCopyMap(self, saveTo, verbose):
        return _proshade.ProSHADE_data_deepCopyMap(self, saveTo, verbose)

    def getMapValue(self, pos):
        return _proshade.ProSHADE_data_getMapValue(self, pos)

    def getMaxSpheres(self):
        return _proshade.ProSHADE_data_getMaxSpheres(self)

    def getMaxBand(self):
        return _proshade.ProSHADE_data_getMaxBand(self)

    def getRealSphHarmValue(self, band, order, shell):
        return _proshade.ProSHADE_data_getRealSphHarmValue(self, band, order, shell)

    def getImagSphHarmValue(self, band, order, shell):
        return _proshade.ProSHADE_data_getImagSphHarmValue(self, band, order, shell)

    def getRRPValue(self, band, sh1, sh2):
        return _proshade.ProSHADE_data_getRRPValue(self, band, sh1, sh2)

    def getAnySphereRadius(self, shell):
        return _proshade.ProSHADE_data_getAnySphereRadius(self, shell)

    def getIntegrationWeight(self):
        return _proshade.ProSHADE_data_getIntegrationWeight(self)

    def getShellBandwidth(self, shell):
        return _proshade.ProSHADE_data_getShellBandwidth(self, shell)

    def getSpherePosValue(self, shell):
        return _proshade.ProSHADE_data_getSpherePosValue(self, shell)

    def getEMatrixByBand(self, band):
        return _proshade.ProSHADE_data_getEMatrixByBand(self, band)

    def getEMatrixValue(self, band, order1, order2, valueReal, valueImag):
        return _proshade.ProSHADE_data_getEMatrixValue(self, band, order1, order2, valueReal, valueImag)

    def getInvSO3Coeffs(self):
        return _proshade.ProSHADE_data_getInvSO3Coeffs(self)

    def getSO3Coeffs(self):
        return _proshade.ProSHADE_data_getSO3Coeffs(self)

    def getComparisonBand(self):
        return _proshade.ProSHADE_data_getComparisonBand(self)

    def getWignerMatrixValue(self, band, order1, order2, valueReal, valueImag):
        return _proshade.ProSHADE_data_getWignerMatrixValue(self, band, order1, order2, valueReal, valueImag)

    def getXDimSize(self):
        return _proshade.ProSHADE_data_getXDimSize(self)

    def getYDimSize(self):
        return _proshade.ProSHADE_data_getYDimSize(self)

    def getZDimSize(self):
        return _proshade.ProSHADE_data_getZDimSize(self)

    def getXDim(self):
        return _proshade.ProSHADE_data_getXDim(self)

    def getYDim(self):
        return _proshade.ProSHADE_data_getYDim(self)

    def getZDim(self):
        return _proshade.ProSHADE_data_getZDim(self)

    def getXFromPtr(self):
        return _proshade.ProSHADE_data_getXFromPtr(self)

    def getYFromPtr(self):
        return _proshade.ProSHADE_data_getYFromPtr(self)

    def getZFromPtr(self):
        return _proshade.ProSHADE_data_getZFromPtr(self)

    def getXToPtr(self):
        return _proshade.ProSHADE_data_getXToPtr(self)

    def getYToPtr(self):
        return _proshade.ProSHADE_data_getYToPtr(self)

    def getZToPtr(self):
        return _proshade.ProSHADE_data_getZToPtr(self)

    def getXAxisOrigin(self):
        return _proshade.ProSHADE_data_getXAxisOrigin(self)

    def getYAxisOrigin(self):
        return _proshade.ProSHADE_data_getYAxisOrigin(self)

    def getZAxisOrigin(self):
        return _proshade.ProSHADE_data_getZAxisOrigin(self)

    def getInternalMap(self):
        return _proshade.ProSHADE_data_getInternalMap(self)

    def getTranslationFnPointer(self):
        return _proshade.ProSHADE_data_getTranslationFnPointer(self)

    def setIntegrationWeight(self, intW):
        return _proshade.ProSHADE_data_setIntegrationWeight(self, intW)

    def setIntegrationWeightCumul(self, intW):
        return _proshade.ProSHADE_data_setIntegrationWeightCumul(self, intW)

    def setEMatrixValue(self, band, order1, order2, val):
        return _proshade.ProSHADE_data_setEMatrixValue(self, band, order1, order2, val)

    def normaliseEMatrixValue(self, band, order1, order2, normF):
        return _proshade.ProSHADE_data_normaliseEMatrixValue(self, band, order1, order2, normF)

    def setSO3CoeffValue(self, position, val):
        return _proshade.ProSHADE_data_setSO3CoeffValue(self, position, val)

    def setWignerMatrixValue(self, val, band, order1, order2):
        return _proshade.ProSHADE_data_setWignerMatrixValue(self, val, band, order1, order2)
ProSHADE_data_swigregister = _proshade.ProSHADE_data_swigregister
ProSHADE_data_swigregister(ProSHADE_data)


def joinElementsFromDifferentGroups(first, second, combine):
    return _proshade.joinElementsFromDifferentGroups(first, second, combine)
joinElementsFromDifferentGroups = _proshade.joinElementsFromDifferentGroups

def computeEnergyLevelsDescriptor(obj1, obj2, settings):
    return _proshade.computeEnergyLevelsDescriptor(obj1, obj2, settings)
computeEnergyLevelsDescriptor = _proshade.computeEnergyLevelsDescriptor

def isBandWithinShell(bandInQuestion, shellInQuestion, spheres):
    return _proshade.isBandWithinShell(bandInQuestion, shellInQuestion, spheres)
isBandWithinShell = _proshade.isBandWithinShell

def computeRRPPearsonCoefficients(obj1, obj2, settings, minCommonBands, minCommonShells, bandDists):
    return _proshade.computeRRPPearsonCoefficients(obj1, obj2, settings, minCommonBands, minCommonShells, bandDists)
computeRRPPearsonCoefficients = _proshade.computeRRPPearsonCoefficients

def allocateTrSigmaWorkspace(minSpheres, intOrder, obj1Vals, obj2Vals, GLabscissas, glWeights, radiiVals):
    return _proshade.allocateTrSigmaWorkspace(minSpheres, intOrder, obj1Vals, obj2Vals, GLabscissas, glWeights, radiiVals)
allocateTrSigmaWorkspace = _proshade.allocateTrSigmaWorkspace

def computeSphericalHarmonicsMagnitude(obj, band, order, radius, result):
    return _proshade.computeSphericalHarmonicsMagnitude(obj, band, order, radius, result)
computeSphericalHarmonicsMagnitude = _proshade.computeSphericalHarmonicsMagnitude

def computeEMatricesForLM(obj1, obj2, bandIter, orderIter, radiiVals, integOrder, abscissas, weights, integRange, sphereDist):
    return _proshade.computeEMatricesForLM(obj1, obj2, bandIter, orderIter, radiiVals, integOrder, abscissas, weights, integRange, sphereDist)
computeEMatricesForLM = _proshade.computeEMatricesForLM

def computeWeightsForEMatricesForLM(obj1, obj2, bandIter, orderIter, obj1Vals, obj2Vals, integOrder, abscissas, weights, sphereDist):
    return _proshade.computeWeightsForEMatricesForLM(obj1, obj2, bandIter, orderIter, obj1Vals, obj2Vals, integOrder, abscissas, weights, sphereDist)
computeWeightsForEMatricesForLM = _proshade.computeWeightsForEMatricesForLM

def releaseTrSigmaWorkspace(obj1Vals, obj2Vals, GLabscissas, glWeights, radiiVals):
    return _proshade.releaseTrSigmaWorkspace(obj1Vals, obj2Vals, GLabscissas, glWeights, radiiVals)
releaseTrSigmaWorkspace = _proshade.releaseTrSigmaWorkspace

def computeEMatrices(obj1, obj2, settings):
    return _proshade.computeEMatrices(obj1, obj2, settings)
computeEMatrices = _proshade.computeEMatrices

def normaliseEMatrices(obj1, obj2, settings):
    return _proshade.normaliseEMatrices(obj1, obj2, settings)
normaliseEMatrices = _proshade.normaliseEMatrices

def computeTraceSigmaDescriptor(obj1, obj2, settings):
    return _proshade.computeTraceSigmaDescriptor(obj1, obj2, settings)
computeTraceSigmaDescriptor = _proshade.computeTraceSigmaDescriptor

def generateSO3CoeffsFromEMatrices(obj1, obj2, settings):
    return _proshade.generateSO3CoeffsFromEMatrices(obj1, obj2, settings)
generateSO3CoeffsFromEMatrices = _proshade.generateSO3CoeffsFromEMatrices

def allocateInvSOFTWorkspaces(work1, work2, work3, band):
    return _proshade.allocateInvSOFTWorkspaces(work1, work2, work3, band)
allocateInvSOFTWorkspaces = _proshade.allocateInvSOFTWorkspaces

def prepareInvSOFTPlan(inverseSO3, band, work1, invCoeffs):
    return _proshade.prepareInvSOFTPlan(inverseSO3, band, work1, invCoeffs)
prepareInvSOFTPlan = _proshade.prepareInvSOFTPlan

def releaseInvSOFTMemory(work1, work2, work3):
    return _proshade.releaseInvSOFTMemory(work1, work2, work3)
releaseInvSOFTMemory = _proshade.releaseInvSOFTMemory

def computeInverseSOFTTransform(obj1, obj2, settings):
    return _proshade.computeInverseSOFTTransform(obj1, obj2, settings)
computeInverseSOFTTransform = _proshade.computeInverseSOFTTransform

def computeRotationunctionDescriptor(obj1, obj2, settings):
    return _proshade.computeRotationunctionDescriptor(obj1, obj2, settings)
computeRotationunctionDescriptor = _proshade.computeRotationunctionDescriptor
class ProSHADE_run(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ProSHADE_run, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ProSHADE_run, name)
    __repr__ = _swig_repr

    def __init__(self, settings):
        this = _proshade.new_ProSHADE_run(settings)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _proshade.delete_ProSHADE_run
    __del__ = lambda self: None

    def getNoStructures(self):
        return _proshade.ProSHADE_run_getNoStructures(self)

    def getVerbose(self):
        return _proshade.ProSHADE_run_getVerbose(self)

    def getEnergyLevelsVectorValue(self, pos=0):
        return _proshade.ProSHADE_run_getEnergyLevelsVectorValue(self, pos)

    def getEnergyLevelsLength(self):
        return _proshade.ProSHADE_run_getEnergyLevelsLength(self)

    def getTraceSigmaVectorValue(self, pos=0):
        return _proshade.ProSHADE_run_getTraceSigmaVectorValue(self, pos)

    def getTraceSigmaLength(self):
        return _proshade.ProSHADE_run_getTraceSigmaLength(self)

    def getRotationFunctionVectorValue(self, pos=0):
        return _proshade.ProSHADE_run_getRotationFunctionVectorValue(self, pos)

    def getRotationFunctionLength(self):
        return _proshade.ProSHADE_run_getRotationFunctionLength(self)

    def getNoRecommendedSymmetryAxes(self):
        return _proshade.ProSHADE_run_getNoRecommendedSymmetryAxes(self)

    def getAllSymsOneArrayLength(self):
        return _proshade.ProSHADE_run_getAllSymsOneArrayLength(self)

    def getNoSymmetryAxes(self):
        return _proshade.ProSHADE_run_getNoSymmetryAxes(self)

    def getEnergyLevelsVector(self):
        return _proshade.ProSHADE_run_getEnergyLevelsVector(self)

    def getTraceSigmaVector(self):
        return _proshade.ProSHADE_run_getTraceSigmaVector(self)

    def getRotationFunctionVector(self):
        return _proshade.ProSHADE_run_getRotationFunctionVector(self)

    def getSymmetryType(self):
        return _proshade.ProSHADE_run_getSymmetryType(self)

    def getSymmetryFold(self):
        return _proshade.ProSHADE_run_getSymmetryFold(self)

    def getSymmetryAxis(self, axisNo):
        return _proshade.ProSHADE_run_getSymmetryAxis(self, axisNo)

    def getAllCSyms(self):
        return _proshade.ProSHADE_run_getAllCSyms(self)

    def getOriginalBounds(self, strNo):
        return _proshade.ProSHADE_run_getOriginalBounds(self, strNo)

    def getReBoxedBounds(self, strNo):
        return _proshade.ProSHADE_run_getReBoxedBounds(self, strNo)

    def getMapValue(self, strNo, mapIndex):
        return _proshade.ProSHADE_run_getMapValue(self, strNo, mapIndex)

    def getEulerAngles(self):
        return _proshade.ProSHADE_run_getEulerAngles(self)

    def getOptimalRotMat(self):
        return _proshade.ProSHADE_run_getOptimalRotMat(self)

    def getTranslationToOrigin(self):
        return _proshade.ProSHADE_run_getTranslationToOrigin(self)

    def getTranslationToMapCentre(self):
        return _proshade.ProSHADE_run_getTranslationToMapCentre(self)

    def getOriginToOverlayTranslation(self):
        return _proshade.ProSHADE_run_getOriginToOverlayTranslation(self)
ProSHADE_run_swigregister = _proshade.ProSHADE_run_swigregister
ProSHADE_run_swigregister(ProSHADE_run)


def getEnergyLevelsVectorNumpy(run, verbose, enLevVec):
    return _proshade.getEnergyLevelsVectorNumpy(run, verbose, enLevVec)
getEnergyLevelsVectorNumpy = _proshade.getEnergyLevelsVectorNumpy

def getTraceSigmaVectorNumpy(run, verbose, trSigVec):
    return _proshade.getTraceSigmaVectorNumpy(run, verbose, trSigVec)
getTraceSigmaVectorNumpy = _proshade.getTraceSigmaVectorNumpy

def getRotationFunctionVectorNumpy(run, verbose, rotFnVec):
    return _proshade.getRotationFunctionVectorNumpy(run, verbose, rotFnVec)
getRotationFunctionVectorNumpy = _proshade.getRotationFunctionVectorNumpy

def getOriginalBoundsVectorNumpy(run, strNo, boundsVec):
    return _proshade.getOriginalBoundsVectorNumpy(run, strNo, boundsVec)
getOriginalBoundsVectorNumpy = _proshade.getOriginalBoundsVectorNumpy

def getReBoxedBoundsVectorNumpy(run, strNo, reboxVec):
    return _proshade.getReBoxedBoundsVectorNumpy(run, strNo, reboxVec)
getReBoxedBoundsVectorNumpy = _proshade.getReBoxedBoundsVectorNumpy

def getReBoxedMap(run, strNo, reboxMap):
    return _proshade.getReBoxedMap(run, strNo, reboxMap)
getReBoxedMap = _proshade.getReBoxedMap

def getOptimalEulerAngles(run, eulerAngs):
    return _proshade.getOptimalEulerAngles(run, eulerAngs)
getOptimalEulerAngles = _proshade.getOptimalEulerAngles

def getToOriginTranslation(run, toOriginTranslation):
    return _proshade.getToOriginTranslation(run, toOriginTranslation)
getToOriginTranslation = _proshade.getToOriginTranslation

def getToMapCentreTranslation(run, toMapCentreTranslation):
    return _proshade.getToMapCentreTranslation(run, toMapCentreTranslation)
getToMapCentreTranslation = _proshade.getToMapCentreTranslation

def getOriginToOverlayTranslation(run, originToOverlayTranslation):
    return _proshade.getOriginToOverlayTranslation(run, originToOverlayTranslation)
getOriginToOverlayTranslation = _proshade.getOriginToOverlayTranslation

def getAllCSymmetriesOneArray(run, allCSymsArray):
    return _proshade.getAllCSymmetriesOneArray(run, allCSymsArray)
getAllCSymmetriesOneArray = _proshade.getAllCSymmetriesOneArray

def getAllCSymmetriesOneArrayAdvanced(settings, allCSymsArray):
    return _proshade.getAllCSymmetriesOneArrayAdvanced(settings, allCSymsArray)
getAllCSymmetriesOneArrayAdvanced = _proshade.getAllCSymmetriesOneArrayAdvanced
class _string_list(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _string_list, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _string_list, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _proshade._string_list_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _proshade._string_list___nonzero__(self)

    def __bool__(self):
        return _proshade._string_list___bool__(self)

    def __len__(self):
        return _proshade._string_list___len__(self)

    def __getslice__(self, i, j):
        return _proshade._string_list___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _proshade._string_list___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _proshade._string_list___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _proshade._string_list___delitem__(self, *args)

    def __getitem__(self, *args):
        return _proshade._string_list___getitem__(self, *args)

    def __setitem__(self, *args):
        return _proshade._string_list___setitem__(self, *args)

    def pop(self):
        return _proshade._string_list_pop(self)

    def append(self, x):
        return _proshade._string_list_append(self, x)

    def empty(self):
        return _proshade._string_list_empty(self)

    def size(self):
        return _proshade._string_list_size(self)

    def swap(self, v):
        return _proshade._string_list_swap(self, v)

    def begin(self):
        return _proshade._string_list_begin(self)

    def end(self):
        return _proshade._string_list_end(self)

    def rbegin(self):
        return _proshade._string_list_rbegin(self)

    def rend(self):
        return _proshade._string_list_rend(self)

    def clear(self):
        return _proshade._string_list_clear(self)

    def get_allocator(self):
        return _proshade._string_list_get_allocator(self)

    def pop_back(self):
        return _proshade._string_list_pop_back(self)

    def erase(self, *args):
        return _proshade._string_list_erase(self, *args)

    def __init__(self, *args):
        this = _proshade.new__string_list(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def push_back(self, x):
        return _proshade._string_list_push_back(self, x)

    def front(self):
        return _proshade._string_list_front(self)

    def back(self):
        return _proshade._string_list_back(self)

    def assign(self, n, x):
        return _proshade._string_list_assign(self, n, x)

    def resize(self, *args):
        return _proshade._string_list_resize(self, *args)

    def insert(self, *args):
        return _proshade._string_list_insert(self, *args)

    def reserve(self, n):
        return _proshade._string_list_reserve(self, n)

    def capacity(self):
        return _proshade._string_list_capacity(self)
    __swig_destroy__ = _proshade.delete__string_list
    __del__ = lambda self: None
_string_list_swigregister = _proshade._string_list_swigregister
_string_list_swigregister(_string_list)

class _float_list(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _float_list, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _float_list, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _proshade._float_list_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _proshade._float_list___nonzero__(self)

    def __bool__(self):
        return _proshade._float_list___bool__(self)

    def __len__(self):
        return _proshade._float_list___len__(self)

    def __getslice__(self, i, j):
        return _proshade._float_list___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _proshade._float_list___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _proshade._float_list___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _proshade._float_list___delitem__(self, *args)

    def __getitem__(self, *args):
        return _proshade._float_list___getitem__(self, *args)

    def __setitem__(self, *args):
        return _proshade._float_list___setitem__(self, *args)

    def pop(self):
        return _proshade._float_list_pop(self)

    def append(self, x):
        return _proshade._float_list_append(self, x)

    def empty(self):
        return _proshade._float_list_empty(self)

    def size(self):
        return _proshade._float_list_size(self)

    def swap(self, v):
        return _proshade._float_list_swap(self, v)

    def begin(self):
        return _proshade._float_list_begin(self)

    def end(self):
        return _proshade._float_list_end(self)

    def rbegin(self):
        return _proshade._float_list_rbegin(self)

    def rend(self):
        return _proshade._float_list_rend(self)

    def clear(self):
        return _proshade._float_list_clear(self)

    def get_allocator(self):
        return _proshade._float_list_get_allocator(self)

    def pop_back(self):
        return _proshade._float_list_pop_back(self)

    def erase(self, *args):
        return _proshade._float_list_erase(self, *args)

    def __init__(self, *args):
        this = _proshade.new__float_list(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def push_back(self, x):
        return _proshade._float_list_push_back(self, x)

    def front(self):
        return _proshade._float_list_front(self)

    def back(self):
        return _proshade._float_list_back(self)

    def assign(self, n, x):
        return _proshade._float_list_assign(self, n, x)

    def resize(self, *args):
        return _proshade._float_list_resize(self, *args)

    def insert(self, *args):
        return _proshade._float_list_insert(self, *args)

    def reserve(self, n):
        return _proshade._float_list_reserve(self, n)

    def capacity(self):
        return _proshade._float_list_capacity(self)
    __swig_destroy__ = _proshade.delete__float_list
    __del__ = lambda self: None
_float_list_swigregister = _proshade._float_list_swigregister
_float_list_swigregister(_float_list)

class _double_list(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _double_list, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _double_list, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _proshade._double_list_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _proshade._double_list___nonzero__(self)

    def __bool__(self):
        return _proshade._double_list___bool__(self)

    def __len__(self):
        return _proshade._double_list___len__(self)

    def __getslice__(self, i, j):
        return _proshade._double_list___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _proshade._double_list___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _proshade._double_list___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _proshade._double_list___delitem__(self, *args)

    def __getitem__(self, *args):
        return _proshade._double_list___getitem__(self, *args)

    def __setitem__(self, *args):
        return _proshade._double_list___setitem__(self, *args)

    def pop(self):
        return _proshade._double_list_pop(self)

    def append(self, x):
        return _proshade._double_list_append(self, x)

    def empty(self):
        return _proshade._double_list_empty(self)

    def size(self):
        return _proshade._double_list_size(self)

    def swap(self, v):
        return _proshade._double_list_swap(self, v)

    def begin(self):
        return _proshade._double_list_begin(self)

    def end(self):
        return _proshade._double_list_end(self)

    def rbegin(self):
        return _proshade._double_list_rbegin(self)

    def rend(self):
        return _proshade._double_list_rend(self)

    def clear(self):
        return _proshade._double_list_clear(self)

    def get_allocator(self):
        return _proshade._double_list_get_allocator(self)

    def pop_back(self):
        return _proshade._double_list_pop_back(self)

    def erase(self, *args):
        return _proshade._double_list_erase(self, *args)

    def __init__(self, *args):
        this = _proshade.new__double_list(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def push_back(self, x):
        return _proshade._double_list_push_back(self, x)

    def front(self):
        return _proshade._double_list_front(self)

    def back(self):
        return _proshade._double_list_back(self)

    def assign(self, n, x):
        return _proshade._double_list_assign(self, n, x)

    def resize(self, *args):
        return _proshade._double_list_resize(self, *args)

    def insert(self, *args):
        return _proshade._double_list_insert(self, *args)

    def reserve(self, n):
        return _proshade._double_list_reserve(self, n)

    def capacity(self):
        return _proshade._double_list_capacity(self)
    __swig_destroy__ = _proshade.delete__double_list
    __del__ = lambda self: None
_double_list_swigregister = _proshade._double_list_swigregister
_double_list_swigregister(_double_list)



def getEnergyLevelsDescrNumpy ( pRun ):
    return ( getEnergyLevelsVectorNumpy       ( pRun, pRun.getVerbose(), pRun.getNoStructures( ) - 1 ) )

def getTraceSigmaDescrNumpy ( pRun ):
    return ( getTraceSigmaVectorNumpy         ( pRun, pRun.getVerbose(), pRun.getNoStructures( ) - 1 ) )

def getRotationFunctionDescrNumpy ( pRun ):
    return ( getRotationFunctionVectorNumpy   ( pRun, pRun.getVerbose(), pRun.getNoStructures( ) - 1 ) )


def getDetectedSymmetryType ( pRun ):
    return                                    ( pRun.getSymmetryType ( ) )

def getDetectedSymmetryFold ( pRun ):
    return                                    ( pRun.getSymmetryFold ( ) )

def getDetectedSymmetryAxes ( pRun ):
    retArr                                    = []
    for iter in range( 0, pRun.getNoRecommendedSymmetryAxes ( ) ):
        hlpArr                                = pRun.getSymmetryAxis ( iter )
        hlpTlp                                = ( hlpArr[0], float ( hlpArr[1] ), float ( hlpArr[2] ), float ( hlpArr[3] ), float ( hlpArr[4] ), float ( hlpArr[5] ) )
        retArr.append                         ( hlpTlp )
    return                                    ( retArr )

def getAllDetectedSymmetryAxesSimple ( pRun ):
    import numpy
    valArr                                    = getAllCSymmetriesOneArray( pRun, pRun.getAllSymsOneArrayLength ( ) )
    retArr                                    = numpy.zeros ( [ int ( pRun.getAllSymsOneArrayLength ( ) / 6 ), 6 ] )
    for iter in range( 0, int ( pRun.getAllSymsOneArrayLength ( ) / 6 ) ):
        retArr[iter][0]                       = valArr[iter*6+0]
        retArr[iter][1]                       = valArr[iter*6+1]
        retArr[iter][2]                       = valArr[iter*6+2]
        retArr[iter][3]                       = valArr[iter*6+3]
        retArr[iter][4]                       = valArr[iter*6+4]
        retArr[iter][5]                       = valArr[iter*6+5]
    return                                    ( retArr )


def getAllDetectedSymmetryAxes ( pStruct, pSet ):
    import numpy
    valArr                                    = getAllCSymmetriesOneArrayAdvanced ( pSet, pStruct.getAllSymsOneArrayLength( pSet ) )
    retArr                                    = numpy.zeros ( [ int ( pStruct.getAllSymsOneArrayLength( pSet ) / 6 ), 6 ] )
    for iter in range( 0, int ( pStruct.getAllSymsOneArrayLength( pSet ) / 6 ) ):
        retArr[iter][0]                       = valArr[iter*6+0]
        retArr[iter][1]                       = valArr[iter*6+1]
        retArr[iter][2]                       = valArr[iter*6+2]
        retArr[iter][3]                       = valArr[iter*6+3]
        retArr[iter][4]                       = valArr[iter*6+4]
        retArr[iter][5]                       = valArr[iter*6+5]
    return                                    ( retArr )

def getCGroupElementsRotMat ( pStruct, pSet, grPos ):
    import numpy
    valArr                                    = pStruct.getCGroupElementsPython ( pSet, pStruct.getCGroupElementsLength( pSet, grPos ), grPos )
    ret                                       = []

    for iter in range ( 0, int ( pStruct.getCGroupElementsLength( pSet, grPos ) / 9 ) ):
        rotM                                  = numpy.zeros ( [ 3, 3 ], dtype="float32" )
        rotM[0][0]                            = valArr[iter*9+0]
        rotM[0][1]                            = valArr[iter*9+1]
        rotM[0][2]                            = valArr[iter*9+2]
        rotM[1][0]                            = valArr[iter*9+3]
        rotM[1][1]                            = valArr[iter*9+4]
        rotM[1][2]                            = valArr[iter*9+5]
        rotM[2][0]                            = valArr[iter*9+6]
        rotM[2][1]                            = valArr[iter*9+7]
        rotM[2][2]                            = valArr[iter*9+8]
        ret.append                            ( rotM )
    return                                    ( ret )

def getNonCSymmetryAxesIndices ( pSet ):
    vals                                      = pSet.getListOfNonCSymmetryAxesIndices ( pSet.getListOfNonCSymmetryAxesIndicesLength ( ) )
    ret                                       = {}

    hlpList                                   = []
    listSplits                                = []
    for val in vals:
        if val == -1:
            listSplits.append                 ( hlpList )
            hlpList                           = []
            continue
        else:
            hlpList.append                    ( int ( val ) )

    Ts                                        = listSplits[1]
    Os                                        = listSplits[2]
    Is                                        = listSplits[3]

    Ds                                        = []
    for val in listSplits[0]:
        if val == -2:
            Ds.append                         ( hlpList )
            hlpList                           = []
            continue
        else:
            hlpList.append                    ( int ( val ) )

    ret["D"]                                  = Ds
    ret["T"]                                  = Ts
    ret["O"]                                  = Os
    ret["I"]                                  = Is

    return                                    ( ret )

def getAllGroupElements ( pSet, pStruct, cIndices, grType ):
    import numpy
    arrLen                                    = pStruct.getAllGroupElementsLength ( pSet, cIndices, grType )
    allEls                                    = pStruct.getAllGroupElementsPython ( pSet, cIndices, grType, arrLen )

    ret                                       = []

    for iter in range ( 0, int ( arrLen / 9 ) ):
        rotM                                  = numpy.zeros ( [ 3, 3 ], dtype="float32" )
        rotM[0][0]                            = allEls[iter*9+0]
        rotM[0][1]                            = allEls[iter*9+1]
        rotM[0][2]                            = allEls[iter*9+2]
        rotM[1][0]                            = allEls[iter*9+3]
        rotM[1][1]                            = allEls[iter*9+4]
        rotM[1][2]                            = allEls[iter*9+5]
        rotM[2][0]                            = allEls[iter*9+6]
        rotM[2][1]                            = allEls[iter*9+7]
        rotM[2][2]                            = allEls[iter*9+8]
        ret.append                            ( rotM )
    return                                    ( ret )



def getOrigBounds ( pRun ):
    import numpy
    ret                                       = numpy.empty ( ( 0, 6 ) )
    for iter in range ( 0, pRun.getNoStructures ( ) ):
        ret                                   = numpy.append ( ret, [getOriginalBoundsVectorNumpy ( pRun, iter, 6 )], axis = 0 )
    return                                    ( ret )

def getReboxBounds ( pRun ):
    import numpy
    ret                                       = numpy.empty ( ( 0, 6 ) )
    for iter in range ( 0, pRun.getNoStructures ( ) ):
        ret                                   = numpy.append ( ret, [getReBoxedBoundsVectorNumpy ( pRun, iter, 6 )], axis = 0 )
    return                                    ( ret )

def getReboxMap ( pRun ):
    ret                                       = []
    reboxedBounds                             = getReboxBounds ( pRun )
    for iter in range ( 0, pRun.getNoStructures ( ) ):
        ret.append                            ( getReBoxedMap ( pRun, iter, int ( ( reboxedBounds[iter][1] - reboxedBounds[iter][0] + 1 ) *
                                                                                  ( reboxedBounds[iter][3] - reboxedBounds[iter][2] + 1 ) *
                                                                                  ( reboxedBounds[iter][5] - reboxedBounds[iter][4] + 1 ) ) ) )
    return                                    ( ret )


def getEulerAngles ( pRun ):
    return                                    ( getOptimalEulerAngles ( pRun, 3 ) )

def getRotationMat ( pRun ):
    import numpy
    eAngs                                     = getEulerAngles ( pRun )

    ret                                       = numpy.empty ( ( 3, 3 ) )

    ret[0][0]                                 =  numpy.cos ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.cos ( eAngs[2] ) - numpy.sin ( eAngs[0] ) * numpy.sin ( eAngs[2] );
    ret[1][0]                                 =  numpy.sin ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.cos ( eAngs[2] ) + numpy.cos ( eAngs[0] ) * numpy.sin ( eAngs[2] );
    ret[2][0]                                 = -numpy.sin ( eAngs[1] ) * numpy.cos ( eAngs[2] );

    ret[0][1]                                 = -numpy.cos ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.sin ( eAngs[2] ) - numpy.sin ( eAngs[0] ) * numpy.cos ( eAngs[2] );
    ret[1][1]                                 = -numpy.sin ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.sin ( eAngs[2] ) + numpy.cos ( eAngs[0] ) * numpy.cos ( eAngs[2] );
    ret[2][1]                                 =  numpy.sin ( eAngs[1] ) * numpy.sin ( eAngs[2] );

    ret[0][2]                                 =  numpy.cos ( eAngs[0] ) * numpy.sin ( eAngs[1]  );
    ret[1][2]                                 =  numpy.sin ( eAngs[0] ) * numpy.sin ( eAngs[1]  );
    ret[2][2]                                 =  numpy.cos ( eAngs[1] );

    return                                    ( ret )

def getNumpyTranslationToOrigin ( pRun ):
    import numpy
    return                                    ( numpy.array ( getToOriginTranslation ( pRun, 3 ) ) )

def getNumpyTranslationToMapCentre ( pRun ):
    import numpy
    return                                    ( numpy.array ( getToMapCentreTranslation ( pRun, 3 ) ) )

def getNumpyOriginToOverlayTranslation ( pRun ):
    import numpy
    return                                    ( numpy.array ( getOriginToOverlayTranslation ( pRun, 3 ) ) )

def computeOverlayTranslationsNumpy           ( pStruct, maxPeakVector ):
    import numpy
    if isFilePDB ( pStruct.fileName ):
        rotCen                                = numpy.empty ( 3 )
        rotCen[0]                             = pStruct.originalPdbRotCenX
        rotCen[1]                             = pStruct.originalPdbRotCenY
        rotCen[2]                             = pStruct.originalPdbRotCenZ

        toOverlay                             = numpy.empty ( 3 )
        toOverlay[0]                          = maxPeakVector[0] + pStruct.originalPdbRotCenX
        toOverlay[1]                          = maxPeakVector[0] + pStruct.originalPdbRotCenX
        toOverlay[2]                          = maxPeakVector[0] + pStruct.originalPdbRotCenX

        toMapCen                              = numpy.empty ( 3 )
        toMapCen[0]                           = pStruct.comMovX
        toMapCen[1]                           = pStruct.comMovY
        toMapCen[2]                           = pStruct.comMovZ

        return                                ( rotCen, toMapCen, toOverlay )
    else:
        xRotPos                               = ( ( ( pStruct.xDimIndicesOriginal / 2 ) - pStruct.xAxisOriginOriginal ) *
                                                  ( ( pStruct.xDimIndicesOriginal - 1 ) / pStruct.xDimSizeOriginal ) ) - ( pStruct.comMovX )
        yRotPos                               = ( ( ( pStruct.yDimIndicesOriginal / 2 ) - pStruct.yAxisOriginOriginal ) *
                                                  ( ( pStruct.yDimIndicesOriginal - 1 ) / pStruct.yDimSizeOriginal ) ) - ( pStruct.comMovY )
        zRotPos                               = ( ( ( pStruct.zDimIndicesOriginal / 2 ) - pStruct.zAxisOriginOriginal ) *
                                                  ( ( pStruct.zDimIndicesOriginal - 1 ) / pStruct.zDimSizeOriginal ) ) - ( pStruct.comMovZ )

        rotCen                                = numpy.empty ( 3 )
        rotCen[0]                             = xRotPos
        rotCen[1]                             = yRotPos
        rotCen[2]                             = zRotPos

        toOverlay                             = numpy.empty ( 3 )
        toOverlay[0]                          = maxPeakVector[0] + xRotPos
        toOverlay[1]                          = maxPeakVector[0] + yRotPos
        toOverlay[2]                          = maxPeakVector[0] + zRotPos

        toMapCen                              = numpy.empty ( 3 )
        toMapCen[0]                           = pStruct.comMovX
        toMapCen[1]                           = pStruct.comMovY
        toMapCen[2]                           = pStruct.comMovZ

        return                                ( rotCen, toMapCen, toOverlay )




def getSphericalHarmonics ( pStruct, verbose = -1 ):
    import numpy
    ret                                       = numpy.empty ( [ 0, pStruct.getSphericalHarmonicsLenForShell ( pStruct.noSpheres - 1, verbose ) ], dtype = complex )
    for sph in range ( 0, pStruct.noSpheres ):
        realSH                                = pStruct.getRealSphericalHarmonicsForShell ( sph, verbose, pStruct.getSphericalHarmonicsLenForShell ( sph, verbose ) )
        imagSH                                = pStruct.getImagSphericalHarmonicsForShell ( sph, verbose, pStruct.getSphericalHarmonicsLenForShell ( sph, verbose ) )

        if len( realSH ) < ret.shape[1]:
            for iter in range( len( realSH ), ret.shape[1] ):
                realSH                        = numpy.append ( realSH, [ 0.0 ] )

        if len( imagSH ) < ret.shape[1]:
            for iter in range( len( imagSH ), ret.shape[1] ):
                imagSH                        = numpy.append ( imagSH, [ 0.0 ] )

        ret                                   = numpy.append ( ret, [ realSH + 1j * imagSH ], axis = 0 )

    return                                    ( ret )


def getEMatrix ( pStruct ):
    import numpy
    ret                                       = numpy.empty ( [ pStruct.getMaxBand(),
                                                                len ( range( -pStruct.getMaxBand(), ( pStruct.getMaxBand() + 1 ) ) ),
                                                                len ( range( -pStruct.getMaxBand(), ( pStruct.getMaxBand() + 1 ) ) ) ], dtype = complex )
    for bnd in range ( 0, pStruct.getMaxBand() ):
        for ord1 in range ( -bnd, ( bnd + 1 ) ):
            realEVals                         = pStruct.getRealEMatrixValuesForLM ( bnd, ord1 + bnd, len( range( -bnd, ( bnd + 1 ) ) ) )
            imagEVals                         = pStruct.getImagEMatrixValuesForLM ( bnd, ord1 + bnd, len( range( -bnd, ( bnd + 1 ) ) ) )

            if len( realEVals ) < ret.shape[2]:
                for iter in range( len( realEVals ), ret.shape[2] ):
                    realEVals                 = numpy.append ( realEVals, [ 0.0 ] )

            if len( imagEVals ) < ret.shape[2]:
                for iter in range( len( imagEVals ), ret.shape[2] ):
                    imagEVals                 = numpy.append ( imagEVals, [ 0.0 ] )

            ret[bnd][ord1]                    = realEVals + 1j * imagEVals

    return                                    ( ret )


def getSO3Coeffs ( pStruct ):
    import numpy
    ret                                       = numpy.empty ( [ pStruct.getMaxBand(),
                                                                len ( range( -pStruct.getMaxBand(), ( pStruct.getMaxBand() + 1 ) ) ),
                                                                len ( range( -pStruct.getMaxBand(), ( pStruct.getMaxBand() + 1 ) ) ) ], dtype = complex )

    realSO3Coeffs                             = pStruct.getRealSO3Coeffs ( int ( ( 4 * numpy.power ( pStruct.getMaxBand(), 3 )  - pStruct.getMaxBand() ) / 3.0 ) )
    imagSO3Coeffs                             = pStruct.getImagSO3Coeffs ( int ( ( 4 * numpy.power ( pStruct.getMaxBand(), 3 )  - pStruct.getMaxBand() ) / 3.0 ) )

    for bnd in range ( 0, pStruct.getMaxBand() ):
        for ord1 in range ( -bnd, ( bnd + 1 ) ):
            for ord2 in range ( -bnd, ( bnd + 1 ) ):
                ret[bnd][ord1][ord2]          = realSO3Coeffs[pStruct.so3CoeffsArrayIndex ( ord1, ord2, bnd )] + 1j * imagSO3Coeffs[pStruct.so3CoeffsArrayIndex ( ord1, ord2, bnd )]

    return                                    ( ret )


def getRotationFunction1D ( pStruct ):
    import numpy

    realRotFun                                = pStruct.getRealRotFunction ( int ( numpy.power ( pStruct.getMaxBand() * 2.0, 3.0 ) ) )
    imagRotFun                                = pStruct.getImagRotFunction ( int ( numpy.power ( pStruct.getMaxBand() * 2.0, 3.0 ) ) )

    return                                    (  realRotFun + 1j * imagRotFun )

def getRotationFunction3D ( pStruct ):
    import numpy

    realRotFun                                = pStruct.getRealRotFunction ( int ( numpy.power ( pStruct.getMaxBand() * 2.0, 3.0 ) ) )
    imagRotFun                                = pStruct.getImagRotFunction ( int ( numpy.power ( pStruct.getMaxBand() * 2.0, 3.0 ) ) )
    ret                                       = numpy.empty ( [ int ( pStruct.getMaxBand() * 2.0 ), int ( pStruct.getMaxBand() * 2.0 ), int ( pStruct.getMaxBand() * 2.0 ) ], dtype = complex )

    for eA in range ( 0, int ( pStruct.getMaxBand() * 2.0 ) ):
       for eB in range ( 0, int ( pStruct.getMaxBand() * 2.0 ) ):
           for eG in range ( 0, int ( pStruct.getMaxBand() * 2.0 ) ):
               index                          = int ( eG + ( pStruct.getMaxBand() * 2.0 ) * ( eB + ( pStruct.getMaxBand() * 2.0 ) * eA ) )
               ret[eA][eB][eG]                = realRotFun[index] + 1j * imagRotFun[index]

    return                                    ( ret )

def getRotationMatrixFromRotFunIndices ( pStruct, first, second, third ):
    import numpy

    oneDMat                                   = pStruct.getRotMatrixFromRotFunInds ( first, second, third, 9  )
    ret                                       = numpy.empty ( [ 3, 3 ] )

    ret[0][0] = oneDMat[0]; ret[0][1] = oneDMat[1]; ret[0][2] = oneDMat[2];
    ret[1][0] = oneDMat[3]; ret[1][1] = oneDMat[4]; ret[1][2] = oneDMat[5];
    ret[2][0] = oneDMat[6]; ret[2][1] = oneDMat[7]; ret[2][2] = oneDMat[8];

    return                                    ( ret )


def getRecommendedSymmetryAxesPython ( pStruct, pSet ):
    retArr                                    = []
    for iter in range( 0, pStruct.getNoRecommendedSymmetryAxes ( pSet ) ):
        hlpArr                                = pStruct.getSymmetryAxis ( pSet, iter )
        hlpTlp                                = ( hlpArr[0], float ( hlpArr[1] ), float ( hlpArr[2] ), float ( hlpArr[3] ), float ( hlpArr[4] ), float ( hlpArr[5] ) )
        retArr.append                         ( hlpTlp )
    return                                    ( retArr )


def getRotationMatrixFromEulerZXZ ( eAngs ):
    import numpy

    ret                                       = numpy.empty ( ( 3, 3 ) )

    ret[0][0]                                 =  numpy.cos ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.cos ( eAngs[2] ) - numpy.sin ( eAngs[0] ) * numpy.sin ( eAngs[2] );
    ret[1][0]                                 =  numpy.sin ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.cos ( eAngs[2] ) + numpy.cos ( eAngs[0] ) * numpy.sin ( eAngs[2] );
    ret[2][0]                                 = -numpy.sin ( eAngs[1] ) * numpy.cos ( eAngs[2] );

    ret[0][1]                                 = -numpy.cos ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.sin ( eAngs[2] ) - numpy.sin ( eAngs[0] ) * numpy.cos ( eAngs[2] );
    ret[1][1]                                 = -numpy.sin ( eAngs[0] ) * numpy.cos ( eAngs[1]  ) * numpy.sin ( eAngs[2] ) + numpy.cos ( eAngs[0] ) * numpy.cos ( eAngs[2] );
    ret[2][1]                                 =  numpy.sin ( eAngs[1] ) * numpy.sin ( eAngs[2] );

    ret[0][2]                                 =  numpy.cos ( eAngs[0] ) * numpy.sin ( eAngs[1]  );
    ret[1][2]                                 =  numpy.sin ( eAngs[0] ) * numpy.sin ( eAngs[1]  );
    ret[2][2]                                 =  numpy.cos ( eAngs[1] );

    return                                    ( ret )


def getMapPython3D ( pStruct ):
    import numpy

    oneDMap                                   = pStruct.getMapPython ( pStruct.getMapArraySizePython() )
    ret                                       = numpy.empty ( [ int ( pStruct.getXDim() ), int ( pStruct.getYDim() ), int ( pStruct.getZDim() ) ] )
    arrPos                                    = 0

    for xIt in range ( 0, int ( pStruct.getXDim() ) ):
       for yIt in range ( 0, int ( pStruct.getYDim() ) ):
           for zIt in range ( 0, int ( pStruct.getZDim() ) ):
               arrPos                         = zIt + pStruct.getZDim() * ( yIt + pStruct.getYDim() * xIt )
               ret[xIt][yIt][zIt]             = oneDMap[arrPos]

    return                                    ( ret )

def getMapPython1D ( pStruct ):
    import numpy

    return                                    ( pStruct.getMapPython ( pStruct.getMapArraySizePython() ) )


def setMapPython1D ( pStruct, map ):
    pStruct.setMapPython                      ( map )

def setMapPython3D ( pStruct, map ):
    import numpy

    map1D                                     = numpy.empty ( int ( pStruct.getXDim() ) * int ( pStruct.getYDim() ) * int ( pStruct.getZDim() ) )
    arrPos                                    = 0

    for xIt in range ( 0, int ( pStruct.getXDim() ) ):
       for yIt in range ( 0, int ( pStruct.getYDim() ) ):
           for zIt in range ( 0, int ( pStruct.getZDim() ) ):
               arrPos                         = zIt + pStruct.getZDim() * ( yIt + pStruct.getYDim() * xIt )
               map1D[arrPos]                  = map[xIt][yIt][zIt]

    pStruct.setMapPython                      ( map1D )

def setNewMapPython1D ( pStruct, map ):
    pStruct.setNewMapPython                   ( map )

def setNewMapPython3D ( pStruct, map ):
    import numpy

    map1D                                     = numpy.empty ( int ( pStruct.getXDim() ) * int ( pStruct.getYDim() ) * int ( pStruct.getZDim() ) )
    arrPos                                    = 0

    for xIt in range ( 0, int ( pStruct.getXDim() ) ):
        for yIt in range ( 0, int ( pStruct.getYDim() ) ):
            for zIt in range ( 0, int ( pStruct.getZDim() ) ):
                arrPos                        = zIt + pStruct.getZDim() * ( yIt + pStruct.getYDim() * xIt )
                map1D[arrPos]                 = map[xIt][yIt][zIt]

    pStruct.setNewMapPython                   ( map1D )


def convert3Dto1DArray ( array3D ):
    import numpy
    assert                                    ( array3D.ndim == 3)

    array1D                                   = numpy.empty ( array3D.shape[0] * array3D.shape[1] * array3D.shape[2] )
    arrPos                                    = 0

    for xIt in range( 0, array3D.shape[0] ):
        for yIt in range( 0, array3D.shape[1] ):
            for zIt in range( 0, array3D.shape[2] ):
                arrPos                        = zIt + array3D.shape[2] * ( yIt + array3D.shape[1] * xIt )
                array1D[arrPos]               = array3D[xIt][yIt][zIt]  

    return                                    ( array1D )              


def getTranslationFunction1D ( pStruct ):
    import numpy

    realTrsFun                                = pStruct.getRealTranslationFunction ( pStruct.getXDim() * pStruct.getYDim() * pStruct.getZDim() )
    imagTrsFun                                = pStruct.getImagTranslationFunction ( pStruct.getXDim() * pStruct.getYDim() * pStruct.getZDim() )

    return                                    (  realTrsFun + 1j * imagTrsFun )

def getTranslationFunction3D ( pStruct ):
    import numpy

    realTrsFun                                = pStruct.getRealTranslationFunction ( pStruct.getXDim() * pStruct.getYDim() * pStruct.getZDim() )
    imagTrsFun                                = pStruct.getImagTranslationFunction ( pStruct.getXDim() * pStruct.getYDim() * pStruct.getZDim() )
    ret                                       = numpy.empty ( [ int ( pStruct.getXDim()), int ( pStruct.getYDim() ), int ( pStruct.getZDim() ) ], dtype = complex )

    for xIt in range ( 0, int ( pStruct.getXDim() ) ):
       for yIt in range ( 0, int ( pStruct.getYDim() ) ):
           for zIt in range ( 0, int ( pStruct.getZDim() ) ):
               index                          = int ( zIt + ( pStruct.getZDim() ) * ( yIt + ( pStruct.getYDim() ) * xIt ) )
               ret[xIt][yIt][zIt]             = realTrsFun[index] + 1j * imagTrsFun[index]

    return                                    ( ret )

# This file is compatible with both classic and new-style classes.


