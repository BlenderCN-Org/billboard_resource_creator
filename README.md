Billboard Resource Creator
--------------------------

This is a Blender 2.79 Addon for building Speed Tree billboard assets for Unity.
It's 99% working. There are some bizarre workflow edge cases that still throw unhandled errors. 

There is currently a Gist of the the main function, which builds a Unity3D Asset.
https://gist.github.com/dval/cb093527d0d4e062b7acfb61247e0506
Images are also baked and tiled into an Atlas. 

The Blender Addon does not build a Unity3D Asset for you. 
The addon does:
1. publish the textures, dimensions, and UV Maps you need to build a BillboardAsset.
2. writes a C# component that provides a button. (pushing the button will build the billboard asset for you. )

So, once you publish from Blender, all you have to do is import into unity, and push a button.
Then, Unity will take those assets, and build the Billboard.


