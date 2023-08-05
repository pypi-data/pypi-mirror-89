import autofit as af
from autoarray.exc import PixelizationException, InversionException, GridException
from autofit.exc import FitException
from autogalaxy.fit import fit
from autogalaxy.pipeline import visualizer
from autogalaxy.pipeline.phase.dataset import analysis as analysis_dataset


class Analysis(analysis_dataset.Analysis):
    def __init__(self, masked_imaging, settings, cosmology, results=None):

        super(Analysis, self).__init__(
            masked_dataset=masked_imaging,
            settings=settings,
            cosmology=cosmology,
            results=results,
        )

        self.visualizer = visualizer.PhaseImagingVisualizer(
            masked_dataset=masked_imaging
        )

    @property
    def masked_imaging(self):
        return self.masked_dataset

    def log_likelihood_function(self, instance):
        """
        Determine the fit of a lens galaxy and source galaxy to the masked_imaging in this lens.

        Parameters
        ----------
        instance
            A model instance with attributes

        Returns
        -------
        fit : Fit
            A fractional value indicating how well this model fit and the model masked_imaging itself
        """

        self.associate_hyper_images(instance=instance)
        plane = self.plane_for_instance(instance=instance)

        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)

        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        try:
            fit = self.masked_imaging_fit_for_plane(
                plane=plane,
                hyper_image_sky=hyper_image_sky,
                hyper_background_noise=hyper_background_noise,
            )

            return fit.figure_of_merit
        except (PixelizationException, InversionException, GridException) as e:
            raise FitException from e

    def masked_imaging_fit_for_plane(
        self, plane, hyper_image_sky, hyper_background_noise, use_hyper_scalings=True
    ):

        return fit.FitImaging(
            masked_imaging=self.masked_dataset,
            plane=plane,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
            use_hyper_scalings=use_hyper_scalings,
            settings_pixelization=self.settings.settings_pixelization,
            settings_inversion=self.settings.settings_inversion,
        )

    def visualize(self, paths: af.Paths, instance, during_analysis):

        self.visualizer.visualize_imaging(paths=paths)

        instance = self.associate_hyper_images(instance=instance)
        plane = self.plane_for_instance(instance=instance)
        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)
        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        fit = self.masked_imaging_fit_for_plane(
            plane=plane,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
        )

        if plane.has_mass_profile:

            visualizer = self.visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
                preloaded_critical_curves=plane.critical_curves,
                preloaded_caustics=plane.caustics,
            )

        else:

            visualizer = self.visualizer

        #   visualizer.visualize_plane(plane=fit.plane, during_analysis=during_analysis)
        visualizer.visualize_fit(paths=paths, fit=fit, during_analysis=during_analysis)

        self.visualizer.visualize_hyper_images(
            paths=paths,
            hyper_galaxy_image_path_dict=self.hyper_galaxy_image_path_dict,
            hyper_model_image=self.hyper_model_image,
            contribution_maps_of_galaxies=plane.contribution_maps_of_galaxies,
        )

        if self.visualizer.plot_fit_no_hyper:

            fit = self.masked_imaging_fit_for_plane(
                plane=plane,
                hyper_image_sky=None,
                hyper_background_noise=None,
                use_hyper_scalings=False,
            )

            visualizer.visualize_fit(
                paths=paths,
                fit=fit,
                during_analysis=during_analysis,
                subfolders="fit_no_hyper",
            )

    def make_attributes(self):
        return Attributes(
            cosmology=self.cosmology,
            hyper_model_image=self.hyper_model_image,
            hyper_galaxy_image_path_dict=self.hyper_galaxy_image_path_dict,
        )


class Attributes:
    def __init__(self, cosmology, hyper_model_image, hyper_galaxy_image_path_dict):
        self.cosmology = cosmology
        self.hyper_model_image = hyper_model_image
        self.hyper_galaxy_image_path_dict = hyper_galaxy_image_path_dict
