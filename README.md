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
    
The compressed directory can be downloaded from this [One-drive-link](https://tinyurl.com/mby99638)
The .isochrones directory will look like this once unzipped:
```bash
|── .isochrones
   ├── BC
   |   ├──mist
   |        ├── UBVRIplus and WISE passband files
   ├── mist
       ├──tracks
           ├──array_grid_v1.2_vvcrit0.4.npz
           ├──full_grid_v1.2_vvcrit0.4.npz
           ├──dt_deep_v1.2_vvcrit0.4.h5
           ├──mist_v1.2_vvcrit0.4.h5
```

**Please Note** It is important that the file be extracted into your username directory, such that the resulting pathway looks like " /Users/your_user_name/.isochrones ". This will ensure that the isochrones package seemlessly finds the preconstructed isochrone grids. Otherwise it will start the automatic downloading from the MIST servers and begin the grid construction on its own (**That big 15GB step**). 


## Using the isochrone widget for the first time
**DON'T FORGET TO SET THE BASE DIRECTORY FOR THE WIDGET**
This can be done by changing the following line in run_isochrone_widget.py (line #16):
    
    RepoDIR = "YOUR_REPOSITORY_DIRECTORY/MIST-isochrone-widget/"

To the directory into which you download this REPO.


The widget can be called from a terminal by typing: 
        " python run_isochrone_widget.py "
        
After which the following should appear in your terminal:
```bash
Holoviews not imported. Some visualizations will not be available.
PyMultiNest not imported.  MultiNest fits will not work.
Initializing isochrone class object (takes a second...)
Initialization done
```
Once that is completed the matplotlib figure should appear and you're ready to explore with the sliders and the pre-loaded cluster buttons.

**Unfortunately**, sometimes the matplotlib figure will 'freeze' when being called within the ipython terminal. I have not found that to be the case when calling the function with python, so that's the more reliable way to use this widget if using it to teach in a lecture or lab.
        
        


