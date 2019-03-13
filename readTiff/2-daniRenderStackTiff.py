from vtk import *

# You'll need to read the file
reader = vtkXMLImageDataReader()

# You'll need a render window to show it in
renwin = vtkRenderWindow()

# You'll need a renderer in the render window
renderer = vtkRenderer()

# This is the file name.
#filename = "../data/head.vti"

# Set the file name on the reader to filename.c_str()
#reader.SetFileName(filename)

reader = vtkTIFFReader()
reader.SetFileName('mriBrain.tif')
reader.Update()
#img = reader.GetOutput()
###? how to set vtkImageDataXXXX.SetSpacing (186, 226, 216)




# Put in renderer in the render window
renwin.AddRenderer(renderer)

# Create the interactor
interactor = vtkRenderWindowInteractor()

# Set the interactor on the render window
renwin.SetInteractor(interactor)

# Create a vtkContourFilter to do the isocontouring
# Set the input to the output of the reader
# Set the value to 135
contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetValue(0,135)

# This is the vtkPolyDataMapper
contourMapper = vtkPolyDataMapper()

# Connect the mapper to the contour filter
# Remember to turn ScalarVisibilityOff()
contourMapper.SetInputConnection(contour.GetOutputPort())
contourMapper.ScalarVisibilityOff()

# This is the vtkActor
contourActor = vtkActor()

# Set the mapper
contourActor.SetMapper(contourMapper)

# Add the actor
#renderer.AddActor(contourActor)

# Create an opacity transfer function to map
# scalar value to opacity
opacityFun = vtkPiecewiseFunction()

# Set a mapping going from 0.0 opacity at 90, up to 0.2 at 100,
# and back down to 0.0 at 120.
opacityFun.AddPoint(0.0, 0.0)
opacityFun.AddPoint(85.0, 0.0)
opacityFun.AddPoint(100.0, 0.2)
opacityFun.AddPoint(115.0, 0.0)
opacityFun.AddPoint(135.0, 0.0)
opacityFun.AddPoint(150.0, 0.9)
opacityFun.AddPoint(165.0, 0.0)

# Create a color transfer function for the mapping of scalar
# value into color
colorFun = vtkColorTransferFunction()

# Set the color to a constant value, you might
# want to try (0.8, 0.4, 0.2)
colorFun.AddRGBPoint(90.0, 0.8, 0.4, 0.2)
colorFun.AddRGBPoint(150.0, 1, 1, 1)

# Create a volume property
# Set the opacity and color. Change interpolation
# to linear for a more pleasing image
property = vtkVolumeProperty()
property.SetScalarOpacity(opacityFun)
property.SetColor(colorFun)
property.SetInterpolationTypeToLinear()

# Create the GPU volume ray cast mapper
mapper = vtkGPUVolumeRayCastMapper()

# Set the input to the output of the reader
mapper.SetInputConnection(reader.GetOutputPort())

# Create the volume
volume = vtkVolume()

# Set the property and the mapper
volume.SetProperty(property)
volume.SetMapper(mapper)

# Add the volume to the renderer
renderer.AddVolume(volume)

# Render and start the interactor
renwin.Render()
interactor.Start()
