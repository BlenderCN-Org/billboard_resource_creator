Billboard Resource Creator
--------------------------

This is a Blender Addon for building Speed Tree billboard assets for Unity. (and in the future, Unreal)

There is currently a Gist of the the main function, which builds a Unity3D Asset.
https://gist.github.com/dval/cb093527d0d4e062b7acfb61247e0506
Images are also baked and tiled into an Atlas. 

The Blender Addon does not build a Unity3D Asset for you. 
The addon publishes the textures, dimensions, and UV Maps you need to build an 8 sided billboard.
It also writes a C# component that, provides you with a button to push. 

So, once you publish from Blender, all you have to do is import into unity, and push a button.
Then, Unity will take those assets, and build the Billboard.


