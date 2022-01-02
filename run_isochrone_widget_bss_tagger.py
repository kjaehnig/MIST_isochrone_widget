import pandas as pd
#from GaiaOCprojectCode.isochrones_.iso_gen import MIST_isochrone_class
from MIST_isochrone_class import MIST_isochrone_class
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from matplotlib.gridspec import GridSpec
import numpy as np

from matplotlib import rcParams

rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['axes.titleweight'] = 'bold'


RepoDIR = "~/Repositories/MIST_isochrone_widget/"


def make_and_plot_isochrone_slider(clst_data=None, iso_cls=None):

    # if clst_data is None:
    #     clst_data = pd.read_csv(RepoDIR+"sample_clusters/berkeley_39_gaia_dr2_data.csv")


    # usually iso_cls will be None unless running this function in ipython.
    if iso_cls is None:
        iso_cls = MIST_isochrone_class()
        iso_cls.generate_mass(2000)
        iso_cls.get_tracks()


    print("Initializing isochrone class object (takes a second...)")
    iso_data = iso_cls.generate_photometry()
    print("Initialization done")
    iso_data = iso_data.loc[iso_data.eep <= 1000].sort_values("eep")

    fig = plt.figure(figsize=(10,6), constrained_layout=False)
    ax_grid = GridSpec(nrows=20,ncols=100)
    ax_age = fig.add_subplot(ax_grid[:,0:5])
    ax_av = fig.add_subplot(ax_grid[:,10:15])
    ax_dist = fig.add_subplot(ax_grid[:,20:25])
    ax_feh = fig.add_subplot(ax_grid[:,30:35])
    cmd = fig.add_subplot(ax_grid[0:15,45:])


    # Set some isochrone class values to help reload other clusters
    iso_cls.currently_loaded_cluster = 'None'
    iso_cls.current_gmag = [0.0]  ##clst_data.phot_g_mean_mag.values
    iso_cls.current_bprp = [0.0]  ##clst_data.bp_rp.values
    iso_cls.age = 7.0
    iso_cls.av = 1.0
    iso_cls.dist = 1.0
    iso_cls.feh = 0.0
    iso_cls.IS_BIG_CAT_LOADED = False


    # initial scatter plot for cluster color-magnitude
    cmd_plot, = cmd.plot([],[],
                ls='None',marker='o', 
                mec='red',mfc='None', rasterized=True)
    cmd_plot.axes.set_ylim(19,12)
    cmd_plot.axes.set_xlim(-1,3)
    cmd.set_ylabel("g - mag")
    cmd.set_xlabel("bp - rp")
    cmd.set_title(iso_cls.currently_loaded_cluster)


    # initial line plot for the isochrone
    line, = cmd.plot(iso_data.BP_RP,iso_data.G_mag
                    ,lw=2,ls='--',color='black',
                rasterized=True)

    ## single point for the TAMS of the isochrone

    tams, = cmd.plot(-50,-50,ls='None',marker='x',rasterized=True, color='lightblue')
    bss_vline, = cmd.plot([-50,-50],[-50,-40], color='lightblue', ls='--', rasterized=True)
    bss_hline, = cmd.plot([-50,-40],[-50,-50], color='lightblue', ls='--', rasterized=True)

    tag_bss, = cmd.plot([],[], marker='o',mec='blue',mfc='blue',lw=2,ls='None',rasterized=True)

    axcolor = 'palegreen'

    age_slider=Slider(
        ax=ax_age,
        label=r'$Age$',
        valmin=5.1,
        valmax=12.5,
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
        valmax=12.6,
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
    def load_big_catalog(event):
        try:
            print("loading CG2020 clsts/membs tables")
            file = open("/Users/kjaehnig/Repositories/jA_A_640_A1_clst","rb")
            clst = pd.read_pickle(file)
            file.close()
            file = open("/Users/kjaehnig/Repositories/jA_A_640_A1_membs","rb")
            memb = pd.read_pickle(file)
            file.close()

            iso_cls.clst = clst
            iso_cls.memb = memb
            iso_cls.IS_BIG_CAT_LOADED = True
        except:
            print("Files not found. Downloading...J/A+A/640/A1")
            try:
                from astroquery.vizier import Vizier
            except:
                raise Exception("ASTROQUERY NOT INSTALLED!")

            viz = Vizier()
            viz.ROW_LIMITS = -1
            viz.columns=['all']
            res = viz.get_catalogs('J/A+A/640/A1')
            clst = res[0].to_pandas()
            memb = res[1].to_pandas()

            iso_cls.clst = clst
            iso_cls.memb = memb 
            ido_cld.IS_BIG_CAT_LOADED = True
        print('Finished loading big catalog')

        # iso_cls.current_gmag = data.phot_g_mean_mag.values
        # iso_cls.current_bprp = data.bp_rp.values
        
        # cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

        # cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
        #                         min(data.phot_g_mean_mag)-0.5)
        # cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
        #                         max(data.bp_rp)+0.5)

        # iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
        # cmd.set_title(iso_cls.currently_loaded_cluster)
        # print(f'Loaded {iso_cls.currently_loaded_cluster}')
    bigcat_ax = fig.add_subplot(ax_grid[18:19,40:55])
    bigcat_button = Button(bigcat_ax,"Load BigCat", color='pink', hovercolor='red')
    bigcat_button.label.set_fontsize(8)
    bigcat_button.on_clicked(load_big_catalog)



    def load_cluster_from_searchbar(clstname):
        if iso_cls.IS_BIG_CAT_LOADED is False:
            cmd.set_title("BIG CATALOG IS NOT LOADED", color='red')
        clstname = clstname.replace(' ','_').replace('-','_').upper()

        if clstname in iso_cls.clst['Cluster'].str.upper().values:
            data = iso_cls.memb.loc[iso_cls.memb['Cluster'].str.upper().values == clstname]
            iso_cls.current_gmag = data['Gmag'].values
            iso_cls.current_bprp = data['BP-RP'].values
            
            cmd_plot.set_data(iso_cls.current_bprp, iso_cls.current_gmag)

            cmd_plot.axes.set_ylim(max(iso_cls.current_gmag)+0.5,
                                    min(iso_cls.current_gmag)-0.5)
            cmd_plot.axes.set_xlim(min(iso_cls.current_bprp)-.5,
                                    max(iso_cls.current_bprp)+0.5)

            iso_cls.currently_loaded_cluster = clstname
            cmd.set_title(iso_cls.currently_loaded_cluster,color='black')
            print(f'Loaded {iso_cls.currently_loaded_cluster}')
            fig.canvas.draw_idle()
        else:
            cmd_plot.set_data([0.0],[0.0])
            cmd.set_title(f'{clstname} not present!',color='red')
            fig.canvas.draw_idle()
    search_bar = fig.add_subplot(ax_grid[18:19,55:85])
    search_box = TextBox(search_bar, initial='type cluster name',label=None)
    search_box.on_submit(load_cluster_from_searchbar)



    # # set up button to load NGC-2632
    # def load_n2632(event):
    #     data = pd.read_csv(RepoDIR+"sample_clusters/ngc_2632_gaia_dr2_data.csv")
    #     iso_cls.current_gmag = data.phot_g_mean_mag.values
    #     iso_cls.current_bprp = data.bp_rp.values
        
    #     cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

    #     cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
    #                             min(data.phot_g_mean_mag)-0.5)
    #     cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
    #                             max(data.bp_rp)+0.5)

    #     iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
    #     cmd.set_title(iso_cls.currently_loaded_cluster)
    #     print(f'Loaded {iso_cls.currently_loaded_cluster}')
    # n2632_ax = fig.add_subplot(ax_grid[18:19,85:100])
    # n2632_button = Button(n2632_ax,"Beehive", color=axcolor, hovercolor='0.975')
    # n2632_button.label.set_fontsize(8)
    # n2632_button.on_clicked(load_n2632)


    # # set up button to load IC-4651
    # def load_ic4651(event):
    #     data = pd.read_csv(RepoDIR+"sample_clusters/ic4651_gaia_dr2_data.csv")
    #     iso_cls.current_gmag = data.phot_g_mean_mag.values
    #     iso_cls.current_bprp = data.bp_rp.values
        
    #     cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

    #     cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
    #                             min(data.phot_g_mean_mag)-0.5)
    #     cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
    #                             max(data.bp_rp)+0.5)

    #     iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
    #     cmd.set_title(iso_cls.currently_loaded_cluster)
    #     print(f'Loaded {iso_cls.currently_loaded_cluster}')
    # i4651_ax = fig.add_subplot(ax_grid[19:20,55:70])
    # i4651_button = Button(i4651_ax,"IC-4651", color=axcolor, hovercolor='0.975')
    # i4651_button.label.set_fontsize(8)
    # i4651_button.on_clicked(load_ic4651)


    # # set up button to load IC-4756
    # def load_ic4756(event):
    #     data = pd.read_csv(RepoDIR+"sample_clusters/ic4756_gaia_dr2_data.csv")
    #     iso_cls.current_gmag = data.phot_g_mean_mag.values
    #     iso_cls.current_bprp = data.bp_rp.values
        
    #     cmd_plot.set_data(data.bp_rp, data.phot_g_mean_mag)

    #     cmd_plot.axes.set_ylim(max(data.phot_g_mean_mag)+0.5,
    #                             min(data.phot_g_mean_mag)-0.5)
    #     cmd_plot.axes.set_xlim(min(data.bp_rp)-.5,
    #                             max(data.bp_rp)+0.5)

    #     iso_cls.currently_loaded_cluster = data.Cluster.iloc[0]
    #     cmd.set_title(iso_cls.currently_loaded_cluster)
    #     print(f'Loaded {iso_cls.currently_loaded_cluster}')
    # i4756_ax = fig.add_subplot(ax_grid[19:20,70:85])
    # i4756_button = Button(i4756_ax,"IC-4756", color=axcolor, hovercolor='0.975')
    # i4756_button.label.set_fontsize(8)
    # i4756_button.on_clicked(load_ic4756)



    # set up button to load the best isochrone for 
    # the currently loaded cluster
    def load_best_iso(event):
        best_iso = iso_cls.clst.loc[iso_cls.clst['Cluster'].str.upper() ==
                                iso_cls.currently_loaded_cluster.upper()]

        str_age = str(np.round(best_iso.AgeNN.values,2))
        str_av = str(np.round(best_iso.AVNN.values,2))
        str_dist = str(np.round(best_iso.DistPc.values,3))
        str_feh = str(np.round(0.000,3))
        clst_str = 'Age: '+str_age+'\nAv: '+str_av+'\nDist[kpc]: '+str_dist+'\nFeH: '+str_feh

        new_iso_vals = iso_cls.generate_photometry(age=best_iso.AgeNN,
                                                   feh=0.0,
                                                   dist=best_iso.DistPc,
                                                   av=best_iso.AVNN).sort_values('eep')
        line.set_xdata(new_iso_vals.BP_RP)
        line.set_ydata(new_iso_vals.G_mag)
        
        age_slider.valinit = best_iso.AgeNN.squeeze()
        av_slider.valinit = best_iso.AVNN.squeeze()
        dist_slider.valinit = best_iso.DistPc.squeeze()/1000.
        feh_slider.valinit = 0.0

        age_slider.reset()
        av_slider.reset()
        dist_slider.reset()
        feh_slider.reset()

        update_tams_location(new_iso_vals)

        fig.canvas.draw_idle()

    load_best_iso_ax = fig.add_subplot(ax_grid[18:19,85:100])
    load_best_iso_button = Button(load_best_iso_ax,'Get best iso', 
                    color='springgreen', hovercolor='palegreen')
    load_best_iso_button.label.set_fontsize(8)
    load_best_iso_button.on_clicked(load_best_iso)


    def locate_and_highlight_bss(cmd_ax, isophot):
        brighter_ = cmd_ax.get_ydata() < isophot.G_mag.min()
        bluer_ = cmd_ax.get_xdata() < isophot.BP_RP.min()

        bss_bprp = cmd_ax.get_xdata()[brighter_ & bluer_]
        bss_gmag = cmd_ax.get_ydata()[brighter_ & bluer_]

        tag_bss.set_xdata(bss_bprp)
        tag_bss.set_ydata(bss_gmag)


    def update_tams_location(isophot):

        isophot = isophot.loc[isophot['eep'] <= 605]
        isophot = isophot.iloc[np.argmin(isophot['BP_RP'])]

        locate_and_highlight_bss(cmd_plot, isophot)

        tams.set_xdata(isophot['BP_RP'])
        tams.set_ydata(isophot['G_mag'])

        bss_vline.set_xdata([isophot['BP_RP'], isophot['BP_RP']])
        bss_vline.set_ydata([isophot['G_mag'], isophot['G_mag']-10])

        bss_hline.set_xdata([isophot['BP_RP'], isophot['BP_RP']-10])
        bss_hline.set_ydata([isophot['G_mag'], isophot['G_mag']])

        fig.canvas.draw_idle()


    # set up to generate new isochrones with sliders
    def generate_new_iso(val):
        new_iso_vals = iso_cls.generate_photometry(age=age_slider.val,
                                                   feh=feh_slider.val,
                                                   dist=dist_slider.val*1000,
                                                   av=av_slider.val)
        new_iso_vals = new_iso_vals.sort_values("eep")
        line.set_xdata(new_iso_vals.BP_RP)
        line.set_ydata(new_iso_vals.G_mag)

        update_tams_location(new_iso_vals)
        fig.canvas.draw_idle()


    age_slider.on_changed(generate_new_iso)
    feh_slider.on_changed(generate_new_iso)
    dist_slider.on_changed(generate_new_iso)
    av_slider.on_changed(generate_new_iso)


    plt.show()



make_and_plot_isochrone_slider()

