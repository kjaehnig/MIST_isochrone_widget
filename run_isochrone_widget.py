import pandas as pd
from GaiaOCprojectCode.isochrones_.iso_gen import MIST_isochrone_class
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.gridspec import GridSpec
import numpy as np


from matplotlib import rcParams

rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.titleweight'] = 'bold'





def make_and_plot_isochrone_slider(clst_data=None, iso_cls=None):

    if clst_data is None:
        clst_data = pd.read_csv("berkeley_39_gaia_dr2_data.csv")


    # usually iso_cls will be None unless running this function in ipython.
    if iso_cls is None:
        iso_cls = MIST_isochrone_class()
        iso_cls.generate_mass(2000)
        iso_cls.get_tracks()

    best_iso_params = pd.read_csv('cluster_best_iso_params.csv')



    print("Initializing isochrone class object (takes a second...)")
    iso_data = iso_cls.generate_photometry()
    print("Initialization done")
    iso_data = iso_data.loc[iso_data.eep <= 1000].sort_values("eep")

    fig = plt.figure(figsize=(8,4), constrained_layout=False)
    ax_grid = GridSpec(nrows=20,ncols=100)
    ax_age = fig.add_subplot(ax_grid[:,0:5])
    ax_av = fig.add_subplot(ax_grid[:,10:15])
    ax_dist = fig.add_subplot(ax_grid[:,20:25])
    ax_feh = fig.add_subplot(ax_grid[:,30:35])
    cmd = fig.add_subplot(ax_grid[0:15,45:])


    # Set some isochrone class values to help reload other clusters
    iso_cls.currently_loaded_cluster = clst_data.Cluster.iloc[0]
    iso_cls.current_gmag = clst_data.phot_g_mean_mag.values
    iso_cls.current_bprp = clst_data.bp_rp.values
    iso_cls.age = 7.0
    iso_cls.av = 1.0
    iso_cls.dist = 1.0
    iso_cls.feh = 0.0


    # initial scatter plot for cluster color-magnitude
    cmd_plot, = cmd.plot(clst_data.bp_rp, clst_data.phot_g_mean_mag,
                ls='None',marker='o', 
                mec='red',mfc='None', rasterized=True)
    cmd_plot.axes.set_ylim(max(clst_data.phot_g_mean_mag)+0.5,
                            min(clst_data.phot_g_mean_mag)-0.5)
    cmd_plot.axes.set_xlim(min(clst_data.bp_rp)-.5,
                            max(clst_data.bp_rp)+0.5)
    cmd.set_ylabel("g - mag")
    cmd.set_xlabel("bp - rp")
    cmd.set_title(iso_cls.currently_loaded_cluster)


    # initial line plot for the isochrone
    line, = cmd.plot(iso_data.BP_RP,iso_data.G_mag
                    ,lw=2,ls='--',color='black',
                rasterized=True)


    axcolor='lightgoldenrodyellow'

    age_slider=Slider(
        ax=ax_age,
        label=r'$Age$',
        valmin=5.1,
        valmax=10.1,
        valinit=7,
        orientation='vertical')
    av_slider = Slider(
        ax=ax_av,
        label=r'$A_{v}$',
        valmin=0.0,
        valmax=5.0,
        valinit=1.0,
        orientation='vertical')
    dist_slider=Slider(
        ax=ax_dist,
        label=r'$Dist(kpc)$',
        valmin=0.01,
        valmax=5,
        valinit=1.0,
        orientation='vertical')
    feh_slider=Slider(
        ax=ax_feh,
        label=r'$FeH$',
        valmin=-4,
        valmax=.49,
        valinit=0.00,
        orientation='vertical')




    # set up button to load Berkeley-39
    def load_b39(event):
        data = pd.read_csv("berkeley_39_gaia_dr2_data.csv")
        iso_cls.current_gmag = data.phot_g_mean_mag.values
        iso_cls.current_bprp = data.bp_rp.values
        
        cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
                                min(data.phot_g_mean_mag)-0.5)
        cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
                                max(data.bp_rp)+0.5)

        iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        cmd.set_title(iso_cls.currently_loaded_cluster)
        print(f'Loaded {iso_cls.currently_loaded_cluster}')
    b39_ax = fig.add_subplot(ax_grid[18:19,40:55])
    b39_button = Button(b39_ax,"Berkeley-39", color=axcolor, hovercolor='0.975')
    b39_button.label.set_fontsize(8)
    b39_button.on_clicked(load_b39)


    # set up button to load Melotte-22
    def load_m22(event):
        data = pd.read_csv("melotte_22_gaia_dr2_data.csv")
        iso_cls.current_gmag = data.phot_g_mean_mag.values
        iso_cls.current_bprp = data.bp_rp.values
        
        cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
                                min(data.phot_g_mean_mag)-0.5)
        cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
                                max(data.bp_rp)+0.5)

        iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        cmd.set_title(iso_cls.currently_loaded_cluster)
        print(f'Loaded {iso_cls.currently_loaded_cluster}')
    m22_ax = fig.add_subplot(ax_grid[18:19,55:70])
    m22_button = Button(m22_ax,"Pleiades", color=axcolor, hovercolor='0.975')
    m22_button.label.set_fontsize(8)
    m22_button.on_clicked(load_m22)


    # set up button to load Melotte-20
    def load_m20(event):
        data = pd.read_csv("melotte_20_gaia_dr2_data.csv")
        iso_cls.current_gmag = data.phot_g_mean_mag.values
        iso_cls.current_bprp = data.bp_rp.values
        
        cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
                                min(data.phot_g_mean_mag)-0.5)
        cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
                                max(data.bp_rp)+0.5)

        iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        cmd.set_title(iso_cls.currently_loaded_cluster)
        print(f'Loaded {iso_cls.currently_loaded_cluster}')
    m20_ax = fig.add_subplot(ax_grid[18:19,70:85])
    m20_button = Button(m20_ax,"Alpha-Per", color=axcolor, hovercolor='0.975')
    m20_button.label.set_fontsize(8)
    m20_button.on_clicked(load_m20)


    # set up button to load NGC-2632
    def load_n2632(event):
        data = pd.read_csv("ngc_2632_gaia_dr2_data.csv")
        iso_cls.current_gmag = data.phot_g_mean_mag.values
        iso_cls.current_bprp = data.bp_rp.values
        
        cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
                                min(data.phot_g_mean_mag)-0.5)
        cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
                                max(data.bp_rp)+0.5)

        iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        cmd.set_title(iso_cls.currently_loaded_cluster)
        print(f'Loaded {iso_cls.currently_loaded_cluster}')
    n2632_ax = fig.add_subplot(ax_grid[18:19,85:100])
    n2632_button = Button(n2632_ax,"Beehive", color=axcolor, hovercolor='0.975')
    n2632_button.label.set_fontsize(8)
    n2632_button.on_clicked(load_n2632)


    # set up button to load IC-4651
    def load_ic4651(event):
        data = pd.read_csv("ic4651_gaia_dr2_data.csv")
        iso_cls.current_gmag = data.phot_g_mean_mag.values
        iso_cls.current_bprp = data.bp_rp.values
        
        cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
                                min(data.phot_g_mean_mag)-0.5)
        cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
                                max(data.bp_rp)+0.5)

        iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        cmd.set_title(iso_cls.currently_loaded_cluster)
        print(f'Loaded {iso_cls.currently_loaded_cluster}')
    i4651_ax = fig.add_subplot(ax_grid[19:20,55:70])
    i4651_button = Button(i4651_ax,"IC-4651", color=axcolor, hovercolor='0.975')
    i4651_button.label.set_fontsize(8)
    i4651_button.on_clicked(load_ic4651)


    # set up button to load IC-4756
    def load_ic4756(event):
        data = pd.read_csv("ic4756_gaia_dr2_data.csv")
        iso_cls.current_gmag = data.phot_g_mean_mag.values
        iso_cls.current_bprp = data.bp_rp.values
        
        cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
                                min(data.phot_g_mean_mag)-0.5)
        cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
                                max(data.bp_rp)+0.5)

        iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        cmd.set_title(iso_cls.currently_loaded_cluster)
        print(f'Loaded {iso_cls.currently_loaded_cluster}')
    i4756_ax = fig.add_subplot(ax_grid[19:20,70:85])
    i4756_button = Button(i4756_ax,"IC-4756", color=axcolor, hovercolor='0.975')
    i4756_button.label.set_fontsize(8)
    i4756_button.on_clicked(load_ic4756)



    # set up button to load the best isochrone for 
    # the currently loaded cluster
    def load_best_iso(event):
        best_iso = best_iso_params.loc[
                    best_iso_params.Cluster==iso_cls.currently_loaded_cluster]

        str_age = str(np.round(best_iso.age.values,2))
        str_av = str(np.round(best_iso.av.values,2))
        str_dist = str(np.round(best_iso.dist.values,3))
        str_feh = str(np.round(best_iso.feh.values,3))
        clst_str = 'Age: '+str_age+'\nAv: '+str_av+'\nDist[kpc]: '+str_dist+'\nFeH: '+str_feh

        new_iso_vals = iso_cls.generate_photometry(age=best_iso.age,
                                                   feh=best_iso.feh,
                                                   dist=best_iso.dist*1000,
                                                   av=best_iso.av).sort_values('eep')
        line.set_xdata(new_iso_vals.BP_RP)
        line.set_ydata(new_iso_vals.G_mag)
        
        age_slider.valinit = best_iso.age.squeeze()
        av_slider.valinit = best_iso.av.squeeze()
        dist_slider.valinit = best_iso.dist.squeeze()
        feh_slider.valinit = best_iso.feh.squeeze()

        age_slider.reset()
        av_slider.reset()
        dist_slider.reset()
        feh_slider.reset()

        fig.canvas.draw_idle()

    load_best_iso_ax = fig.add_subplot(ax_grid[19:20,85:100])
    load_best_iso_button = Button(load_best_iso_ax,'Get best iso', 
                    color='springgreen', hovercolor='palegreen')
    load_best_iso_button.label.set_fontsize(8)
    load_best_iso_button.on_clicked(load_best_iso)


    # set up to generate new isochrones with sliders
    def generate_new_iso(val):
        new_iso_vals = iso_cls.generate_photometry(age=age_slider.val,
                                                   feh=feh_slider.val,
                                                   dist=dist_slider.val*1000,
                                                   av=av_slider.val)
        new_iso_vals = new_iso_vals.sort_values("eep")
        line.set_xdata(new_iso_vals.BP_RP)
        line.set_ydata(new_iso_vals.G_mag)
        fig.canvas.draw_idle()


    age_slider.on_changed(generate_new_iso)
    feh_slider.on_changed(generate_new_iso)
    dist_slider.on_changed(generate_new_iso)
    av_slider.on_changed(generate_new_iso)


    plt.show()



make_and_plot_isochrone_slider()

