from vtk import *

# You'll need a render window to show it in
renwin = vtkRenderWindow()

# You'll need a renderer in the render window
renderer = vtkRenderer()

# Put in renderer in the render window
renwin.AddRenderer(renderer)

# You'll need an interactor for interaction
interactor = vtkRenderWindowInteractor()

# Set interactor on the render window
renwin.SetInteractor(interactor)

style = vtkInteractorStyleImage()
interactor.SetInteractorStyle(style)






reader = vtkTIFFReader()
reader.SetFileName('mriBrain.tif')
reader.Update()
img = reader.GetOutput()


# You'll need an image actor for display
actor = vtkImageActor()

# Connect the reader to the image actor
actor.SetInputData(img)

# Put the image actor in the renderer
renderer.AddActor(actor)

# Render and start interactor
renwin.Render()

interactor.Start()
