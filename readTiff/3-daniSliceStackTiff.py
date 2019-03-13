# Examples of using widgets to interact / measure data in VTK views

# A central feature among most widgets is the conversion of 2D coordinates to 3D
# coordinates and vice versa.

# We use vtkImageActorPointPlacer to map between 2D image plane coordinates to
# 3D world coordinates

import os
import vtk

reader = vtk.vtkTIFFReader()
reader.SetFileName('mriBrain.tif') #prefix doesn't work
reader.Update()
#img = reader.GetOutput()


im = vtk.vtkImageResliceMapper()
im.SetInputConnection(reader.GetOutputPort())
im.SliceFacesCameraOn()
im.SliceAtFocalPointOn()

ip = vtk.vtkImageProperty()
ip.SetColorWindow(1000)
ip.SetColorLevel(50)
ip.SetAmbient(0.0)
ip.SetDiffuse(1.0)
ip.SetOpacity(1.0)
ip.SetInterpolationTypeToLinear()

ia = vtk.vtkImageSlice()
ia.SetMapper(im)
ia.SetProperty(ip)

# Create the RenderWindow, Renderer
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.SetSize(800, 800)
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren1.AddViewProp(ia)
ren1.SetBackground(0.1, 0.2, 0.4)

iren = vtk.vtkRenderWindowInteractor()
style = vtk.vtkInteractorStyleImage()
style.SetInteractionModeToImage3D()
iren.SetInteractorStyle(style)
renWin.SetInteractor(iren)

# render the image
renWin.Render()
cam1 = ren1.GetActiveCamera()
cam1.ParallelProjectionOn()
ren1.ResetCameraClippingRange()
renWin.Render()

# Set up widget
im.SliceFacesCameraOff()
im.SliceAtFocalPointOff()

sliderRep = vtk.vtkSliderRepresentation2D()
sliceMin = 0
sliceMax = reader.GetOutput().GetDimensions()[2] - 1
sliderRep.SetMinimumValue(sliceMin)
sliderRep.SetMaximumValue(sliceMax)
sliderRep.SetValue((sliceMin + sliceMax) / 2)
sliderRep.SetTitleText("Slice")
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(0.3, 0.1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(0.7, 0.1)
sliderRep.SetSliderLength(0.02)
sliderRep.SetSliderWidth(0.03)
sliderRep.SetEndCapLength(0.01)
sliderRep.SetEndCapWidth(0.03)
sliderRep.SetTubeWidth(0.005)
sliderRep.SetLabelFormat("%3.0lf")
sliderRep.SetTitleHeight(0.05)
sliderRep.SetLabelHeight(0.05)

sliderWidget = vtk.vtkSliderWidget()
sliderWidget.SetInteractor(iren)
sliderWidget.SetRepresentation(sliderRep)
sliderWidget.SetKeyPressActivation(0)
sliderWidget.SetAnimationModeToAnimate()
sliderWidget.SetEnabled(1)

def sliderCallback(obj, ev):
    value = sliderRep.GetValue()
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, value)
    plane.SetNormal(0, 0, 1)
    im.SetSlicePlane(plane)
    renWin.Render()

sliderWidget.AddObserver(vtk.vtkCommand.InteractionEvent, sliderCallback)

ia = vtk.vtkImageActor()
ia.SetMapper(im)
ia.SetProperty(ip)

pointPlacer = vtk.vtkImageActorPointPlacer()
pointPlacer.SetImageActor(ia)

contourRep = vtk.vtkOrientedGlyphContourRepresentation()
contourRep.SetPointPlacer(pointPlacer)
contourRep.GetProperty().SetColor(0, 1, 0)

contourWidget = vtk.vtkContourWidget()
contourWidget.SetInteractor(iren)
contourWidget.SetFollowCursor(True)
contourWidget.SetEnabled(1)
contourWidget.ProcessEventsOn()

style.SetInteractionModeToImage2D()
iren.Start()
