README - GUI:
=============
<ul>
  <li>This is a directory location where all BTS-3000 GUI assets are stored and located.</li>
  <li>Please do not remove any of these assets.</li>
  <li>Please do not modify any of these assets.</li>
  <li>If any GUI assets go missing, this will cause the BTS-3000 program to produce an error.</li>
  <li>If you notice any GUI assets missing, it is advised you replace them with copies or a substitute.</li>
</ul>

<ol>
  <li>To replace GUI assets, you must have a desired image and upload into this directory or folder.</li> 
  <li>Once the asset is with the rest, modify the source code in PyCharm IDE</li>
  <ul>
    <li>This replacement will usually be changing a file directory path reference in a PhotoImage or icon bit map GUI component</li>
    <ul>
      <li>A PhotoImage looks like the following in code: <code>img = PhotoImage(file=r"[your_saved_dir_here]\NexteerBannerBTS.png")</code></li>
      <li>Notice that an <code>r</code> is place in front of the String path so <code>\</code> can be registered. Also, the file must be PNG like above (JPG will NOT work).</li>
      <li>What's inside the "" is what you will change to replace GUI assets</li>
    </ul>
</ol>

<ul>
  <li>Note that an icon bit map is different and looks like this <code>rootFrame.iconbitmap(r"[your_saved_dir_here]\NexteerIcon.ico")</code></li>
  <li>An icon bit map requires a .ico file which can be obtained from opening a PNG file in MS Paint and then saving as a .ico in the file name with the image being 24 bits or less</li>
  <li>You will still need to first upload the image to this directory or folder and then change what's inside the "" to match the file you recently uploaded to replace</li>
</ul>
  
The files that should be in this folder are:
=============
<ol>
  <li>Loading_Circle (1).png</li>
  <li>NexteerBanner.PNG</li>
  <li>NexteerBanner2.jpg</li>
  <li>NexteerBanner3.jpg</li>
  <li>NexteerBanner4.jpg</li>
  <li>NexteerBannerBckgrnd.png</li>
  <li>NexteerBannerBTS.png</li>
  <li>NexteerIcon.ico</li>
</ol>
