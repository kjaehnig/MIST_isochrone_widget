

class MIST_isochrone_class():
    """Base class for generating isochrones
    """
    def __init__(self):
        self.num_stars = 1000
        self.IMF = None
        self.masses = None
        self.tracks = None
        self.has_masses = False
        self.has_tracks = False

    def generate_mass(self, N, IMF='chabrier'):
        if IMF is 'chabrier':
            from isochrones.priors import ChabrierPrior as iso_IMF
            self.IMF='chabrier'
        elif IMF is 'salpeter':
            from isochrones.priors import SalpeterPrior as iso_IMF
            self.IMF='salpetr'
        masses = iso_IMF().sample(N)
        self.masses = masses
        self.has_masses = True


    def get_tracks(self):
        from isochrones import get_ichrone
        tracks = get_ichrone('mist', tracks=False, basic=False)
        self.has_tracks = True
        self.tracks = tracks


    def generate_photometry(self, 
                            age=7.0, 
                            av=1.0, 
                            dist=10.0, 
                            feh=0.02):
        if self.has_masses is False:
            self.generate_mass
        if self.has_tracks is False:
            self.get_tracks

        iso_df = self.tracks.generate(self.masses,
                                    age,
                                    feh,
                                    distance=dist,
                                    AV=av)
        iso_df['BP_RP'] = iso_df.BP_mag.values - iso_df.RP_mag.values
        iso_df = iso_df.dropna()

        return iso_df
