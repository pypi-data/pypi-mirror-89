import os
import shutil
from os import path

import pytest

import autofit as af
import autogalaxy as ag
from autoconf import conf
from autogalaxy.pipeline import visualizer as vis
from autogalaxy.plot import Include

directory = path.dirname(path.realpath(__file__))


@pytest.fixture(name="plot_path")
def make_visualizer_plotter_setup():
    return path.join(
        "{}".format(path.dirname(path.realpath(__file__))),
        "files",
        "plot",
        "visualizer",
    )


@pytest.fixture(autouse=True)
def default_config(plot_path):
    conf.instance.push(path.join(directory, "config"), output_path=plot_path)


@pytest.fixture(name="include_all")
def make_include_all(default_config):
    return Include(
        origin=True,
        mask=True,
        grid=True,
        border=True,
        positions=True,
        light_profile_centres=True,
        mass_profile_centres=True,
        critical_curves=True,
        caustics=True,
        multiple_images=True,
        inversion_pixelization_grid=True,
        inversion_grid=True,
        inversion_border=True,
        inversion_image_pixelization_grid=True,
        preloaded_critical_curves=ag.GridIrregularGrouped([(1.0, 1.0), (2.0, 2.0)]),
        preload_caustics=ag.GridIrregularGrouped([(1.0, 1.0), (2.0, 2.0)]),
    )


class TestAbstractPhaseVisualizer:
    def test__visualizer_with_preloaded_critical_curves_and_caustics_is_setup(
        self, masked_imaging_7x7, include_all, plot_path, plot_patch
    ):
        visualizer = vis.PhaseDatasetVisualizer(masked_dataset=masked_imaging_7x7)

        assert visualizer.include.preloaded_critical_curves == None
        assert visualizer.include.preloaded_caustics == None

        visualizer = visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
            preloaded_critical_curves=1, preloaded_caustics=2
        )

        assert visualizer.include.preloaded_critical_curves == 1
        assert visualizer.include.preloaded_caustics == 2

        visualizer.include.critical_curves = False
        visualizer.include.caustics = False


class TestPhaseImagingVisualizer:
    def test__visualizes_imaging_using_configs(
        self, masked_imaging_7x7, include_all, plot_path, plot_patch
    ):

        if path.exists(plot_path):
            shutil.rmtree(plot_path)

        visualizer = vis.PhaseImagingVisualizer(masked_dataset=masked_imaging_7x7)

        visualizer = visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
            preloaded_critical_curves=include_all.preloaded_critical_curves,
            preloaded_caustics=include_all.preloaded_caustics,
        )

        visualizer.visualize_imaging(paths=af.Paths())

        assert (
            path.join(plot_path, "image", "imaging", "subplot_imaging.png")
            in plot_patch.paths
        )
        assert path.join(plot_path, "image", "imaging", "image.png") in plot_patch.paths
        assert (
            path.join(plot_path, "image", "imaging", "noise_map.png")
            not in plot_patch.paths
        )
        assert path.join(plot_path, "image", "imaging", "psf.png") in plot_patch.paths
        assert (
            path.join(plot_path, "image", "imaging", "inverse_noise_map.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "imaging", "signal_to_noise_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "imaging", "absolute_signal_to_noise_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "imaging", "potential_chi_squared_map.png")
            in plot_patch.paths
        )

    def test__source_and_galaxy__visualizes_fit_and_inversion_using_configs(
        self,
        masked_imaging_7x7,
        masked_imaging_fit_x2_galaxy_inversion_7x7,
        include_all,
        plot_path,
        plot_patch,
    ):

        if path.exists(plot_path):
            shutil.rmtree(plot_path)

        visualizer = vis.PhaseImagingVisualizer(masked_dataset=masked_imaging_7x7)

        visualizer = visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
            preloaded_critical_curves=include_all.preloaded_critical_curves,
            preloaded_caustics=include_all.preloaded_caustics,
        )

        visualizer.visualize_fit(
            paths=af.Paths(),
            fit=masked_imaging_fit_x2_galaxy_inversion_7x7,
            during_analysis=False,
        )

        assert (
            path.join(plot_path, "image", "fit_imaging", "subplot_fit_imaging.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "image.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "noise_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "signal_to_noise_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "model_image.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "residual_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "normalized_residual_map.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "chi_squared_map.png")
            in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "fit_imaging", "subtracted_image_of_galaxy_0.png"
            )
            in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "fit_imaging", "subtracted_image_of_galaxy_1.png"
            )
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "model_image_of_galaxy_0.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_imaging", "model_image_of_galaxy_1.png")
            not in plot_patch.paths
        )

        assert (
            path.join(plot_path, "image", "inversion", "subplot_inversion.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "reconstructed_image.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "reconstruction.png")
            in plot_patch.paths
        )
        # assert path.join(plot_path, "image","inversion","errors.png") not in plot_patch.paths
        assert (
            path.join(plot_path, "image", "inversion", "residual_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "normalized_residual_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "chi_squared_map.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "regularization_weight_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "inversion", "interpolated_reconstruction.png"
            )
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "interpolated_errors.png")
            in plot_patch.paths
        )

        image = ag.util.array.numpy_array_2d_from_fits(
            file_path=path.join(
                plot_path, "image", "fit_imaging", "fits", "image.fits"
            ),
            hdu=0,
        )

        assert image.shape == (5, 5)

        image = ag.util.array.numpy_array_2d_from_fits(
            file_path=path.join(
                plot_path,
                "image",
                "inversion",
                "fits",
                "interpolated_reconstruction.fits",
            ),
            hdu=0,
        )

        assert image.shape == (7, 7)

    def test__visualizes_hyper_images_using_config(
        self,
        masked_imaging_7x7,
        hyper_model_image_7x7,
        include_all,
        hyper_galaxy_image_path_dict_7x7,
        masked_imaging_fit_x2_galaxy_inversion_7x7,
        plot_path,
        plot_patch,
    ):

        visualizer = vis.PhaseImagingVisualizer(masked_dataset=masked_imaging_7x7)

        visualizer = visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
            preloaded_critical_curves=include_all.preloaded_critical_curves,
            preloaded_caustics=include_all.preloaded_caustics,
        )

        visualizer.visualize_hyper_images(
            paths=af.Paths(),
            hyper_galaxy_image_path_dict=hyper_galaxy_image_path_dict_7x7,
            hyper_model_image=hyper_model_image_7x7,
            contribution_maps_of_galaxies=masked_imaging_fit_x2_galaxy_inversion_7x7.plane.contribution_maps_of_galaxies,
        )

        assert (
            path.join(plot_path, "image", "hyper", "hyper_model_image.png")
            in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "hyper", "subplot_hyper_images_of_galaxies.png"
            )
            in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "hyper", "subplot_contribution_maps_of_galaxies.png"
            )
            not in plot_patch.paths
        )


class TestPhaseInterferometerVisualizer:
    def test__visualizes_interferometer_using_configs(
        self, masked_interferometer_7, include_all, plot_path, plot_patch
    ):
        visualizer = vis.PhaseInterferometerVisualizer(
            masked_dataset=masked_interferometer_7
        )

        visualizer = visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
            preloaded_critical_curves=include_all.preloaded_critical_curves,
            preloaded_caustics=include_all.preloaded_caustics,
        )

        visualizer.visualize_interferometer(paths=af.Paths())

        assert (
            path.join(
                plot_path, "image", "interferometer", "subplot_interferometer.png"
            )
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "interferometer", "visibilities.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "interferometer", "u_wavelengths.png")
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "interferometer", "v_wavelengths.png")
            not in plot_patch.paths
        )

    def test__x2_galaxies_in_fit__visualizes_fit_using_configs(
        self,
        masked_interferometer_7,
        masked_interferometer_fit_x2_galaxy_inversion_7x7,
        include_all,
        plot_path,
        plot_patch,
    ):
        visualizer = vis.PhaseInterferometerVisualizer(
            masked_dataset=masked_interferometer_7
        )

        visualizer = visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
            preloaded_critical_curves=include_all.preloaded_critical_curves,
            preloaded_caustics=include_all.preloaded_caustics,
        )

        visualizer.visualize_fit(
            paths=af.Paths(),
            fit=masked_interferometer_fit_x2_galaxy_inversion_7x7,
            during_analysis=True,
        )

        assert (
            path.join(
                plot_path,
                "image",
                "fit_interferometer",
                "subplot_fit_interferometer_real.png",
            )
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_interferometer", "visibilities.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "fit_interferometer", "noise_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "fit_interferometer", "signal_to_noise_map.png"
            )
            not in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "fit_interferometer", "model_visibilities.png"
            )
            in plot_patch.paths
        )
        assert (
            path.join(
                plot_path,
                "image",
                "fit_interferometer",
                "residual_map_vs_uv_distances_real.png",
            )
            not in plot_patch.paths
        )
        assert (
            path.join(
                plot_path,
                "image",
                "fit_interferometer",
                "normalized_residual_map_vs_uv_distances_real.png",
            )
            in plot_patch.paths
        )
        assert (
            path.join(
                plot_path,
                "image",
                "fit_interferometer",
                "chi_squared_map_vs_uv_distances_real.png",
            )
            in plot_patch.paths
        )

        #    assert path.join(plot_path, "image","inversion","subplot_inversion.png") in plot_patch.paths
        assert (
            path.join(plot_path, "image", "inversion", "reconstructed_image.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "reconstruction.png")
            in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "errors.png")
            not in plot_patch.paths
        )
        #  assert path.join(plot_path, "image","inversion","residual_map.png") not in plot_patch.paths
        #  assert path.join(plot_path, "image","inversion","normalized_residual_map.png") not in plot_patch.paths
        #  assert path.join(plot_path, "image","inversion","chi_squared_map.png") in plot_patch.paths
        assert (
            path.join(plot_path, "image", "inversion", "regularization_weight_map.png")
            not in plot_patch.paths
        )
        assert (
            path.join(
                plot_path, "image", "inversion", "interpolated_reconstruction.png"
            )
            not in plot_patch.paths
        )
        assert (
            path.join(plot_path, "image", "inversion", "interpolated_errors.png")
            in plot_patch.paths
        )
