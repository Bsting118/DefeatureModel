README - GUI:
=============
-This is a directory location where all BTS-3000 GUI assets are stored and located.
-Please do not remove any of these assets.
-Please do not modify any of these assets.
-If any GUI assets go missing, this will cause the BTS-3000 program to produce an error.
-If you notice any GUI assets missing, it is advised you replace them with copies or a substitute.

-To replace GUI assets, you must have a desired image and upload into this directory or folder. 
-Once the asset is with the rest, modify the source code in PyCharm IDE
--This replacement will usually be changing a file directory path reference in a PhotoImage or icon bit map GUI component
---A PhotoImage looks like the following in code: 'img = PhotoImage(file=r"[your_saved_dir_here]\NexteerBannerBTS.png")'
---Notice that an r is place in front of the String path so \ can be registered. Also, the file must be PNG like above (JPG will NOT work).
---What's inside the "" is what you will change to replace GUI assets

---Note that an icon bit map is different and looks like this 'rootFrame.iconbitmap(r"[your_saved_dir_here]\NexteerIcon.ico")'
---An icon bit map requires a .ico file which can be obtained from opening a PNG file in MS Paint and then saving as a .ico in the file name with the image being 24 bits or less
---You will still need to first upload the image to this directory or folder and then change what's inside the "" to match the file you recently uploaded to replace

The files that should be in this folder are:
*Loading_Circle (1).png
*NexteerBanner.PNG
*NexteerBanner2.jpg
*NexteerBanner3.jpg
*NexteerBanner4.jpg
*NexteerBannerBckgrnd.png
*NexteerBannerBTS.png
*NexteerIcon.ico