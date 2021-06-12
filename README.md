# MIST-isochrone-widget
Simple python implementation with matplotlib to manually fit MIST isochrones to Gaia DR2 color-magnitude diagrams

This widget was primarily made to illustrate how cluster properties like **Age, Extinction(Av), distance, and FeH** can be derived by fitting an isochrone to the cluster's color-magnitude sequence.

The code here relies primarily on the isochrones package developed by Timothy Morton, which can be found here at [github link](https://github.com/timothydmorton/isochrones).

The isochrones package can be installed with 'pip install isochrones'
Installing the isochrones package will install most of the packages needed to run this widget. Nonetheless, you should have the following packages for this widget:

- Numpy
- Matplotlib
- Pandas

**WARNING** Upon running the MIST_isochrone_class for the first time, the isochrones package will initially produce an interpolation directory and table of isochrones that downloads from the MIST website server. All in all this interpolation/generation takes a few minutes and produces files/directories totalling 15Gb. 
Once these files are generated, you should be able generate isochrones on the relatively easily.

If you wish to avoid this interpolation step and want to jump right into creating isochrones, I am providing a link to a precompile directory of all necessary evolutionary tracks and their bolometric corrections to generate isochrones in Gaia DR2 [G, BP, RP] passbands. The files contains UBVRI passbands as well as WISE passbands. The directory is tar zipped and can be extracted with
    " tar -xvzf isochrones_precompiled_data.tar.gz " 
    
The compressed directory can be downloaded from this [One-drive-link](https://vanderbilt365-my.sharepoint.com/:u:/g/personal/karl_o_jaehnig_vanderbilt_edu/EXfkpHWiINpOkwIYICHNGEgBbqq4f09SIJoPXJpKubzY7w?e=oUC7TT)
**Please Note** It is important that the file be extracted into your username directory, such that the resulting pathway looks like " /Users/your_user_name/.isochrones ". This will ensure that the isochrones package seemlessly finds the preconstructed isochrone grids. Otherwise it will start the automatic downloading from the MIST servers and begin the grid construction on its own (**That big 15GB step**). 


After importing the MIST_isochrone_class object and initializing masses, and tracks, the first generation of an isochrone will take a few seconds. After which the generation of isochrones via the figure sliders should proceed quickly.



