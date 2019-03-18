#!/usr/bin/env python
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Image pipeline
#reader = vtk.vtkImageReader()
filename = "/Users/dani/Documents/data/fibers/newNatalie/recon_20141210_204424_127_1_InSituPyro_HC_97_0"
#reader = createReader.CreateImageReader2(filename)


reader = vtk.vtkImageReader2Factory()
reader.SetFilePrefix(filename)


#reader.SetFileName(filename)
# "beach.tif" image contains ORIENTATION tag which is
# ORIENTATION_TOPLEFT (row 0 top, col 0 lhs) type. The TIFF
# reader parses this tag and sets the internal TIFF image
# orientation accordingly.  To overwrite this orientation with a vtk
# convention of ORIENTATION_BOTLEFT (row 0 bottom, col 0 lhs ), invoke
# SetOrientationType method with parameter value of 4.
#reader.SetOrientationType(4)
viewer = vtk.vtkImageViewer()
viewer.SetInputConnection(reader.GetOutputPort())
viewer.SetColorWindow(256)
viewer.SetColorLevel(127.5)
#show Image window - thanks Cory
rwi = vtk.vtkRenderWindowInteractor()
viewer.SetupInteractor(rwi)
rwi.Initialize()
rwi.Start()
#make interface
viewer.Render()
reader.UnRegister(viewer) # not needed in python
# --- end of script --
