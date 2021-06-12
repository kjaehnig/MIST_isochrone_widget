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

After importing the MIST_isochrone_class object and initializing masses, and tracks, the first generation of an isochrone will take a few seconds. After which the generation of isochrones via the figure sliders should proceed quickly.



