from os import path

import autogalaxy.plot as aplt
import pytest


@pytest.fixture(name="plot_path")
def make_hyper_plotter_setup():
    return path.join(
        "{}".format(path.dirname(path.realpath(__file__))),
        "files",
        "plots",
        "hyper_galaxies",
    )


def test__plot_hyper_images_of_galaxies(
    hyper_galaxy_image_path_dict_7x7, mask_7x7, include_all, plot_path, plot_patch
):

    aplt.hyper.subplot_hyper_images_of_galaxies(
        hyper_galaxy_image_path_dict=hyper_galaxy_image_path_dict_7x7,
        mask=mask_7x7,
        include=include_all,
        sub_plotter=aplt.SubPlotter(output=aplt.Output(plot_path, format="png")),
    )

    assert (
        path.join(plot_path, "subplot_hyper_images_of_galaxies.png") in plot_patch.paths
    )


def test__plot_contribution_maps_of_galaxies(
    contribution_map_7x7, mask_7x7, include_all, plot_path, plot_patch
):

    aplt.hyper.subplot_contribution_maps_of_galaxies(
        contribution_maps_of_galaxies=[
            contribution_map_7x7,
            contribution_map_7x7,
            None,
        ],
        mask=mask_7x7,
        include=include_all,
        sub_plotter=aplt.SubPlotter(output=aplt.Output(plot_path, format="png")),
    )

    assert (
        path.join(plot_path, "subplot_contribution_maps_of_galaxies.png")
        in plot_patch.paths
    )


def test__plot_individual_images(
    hyper_galaxy_image_0_7x7, contribution_map_7x7, include_all, plot_path, plot_patch
):

    aplt.hyper.hyper_galaxy_image(
        galaxy_image=hyper_galaxy_image_0_7x7,
        include=include_all,
        plotter=aplt.Plotter(output=aplt.Output(plot_path, format="png")),
    )

    assert path.join(plot_path, "hyper_galaxy_image.png") in plot_patch.paths

    aplt.hyper.contribution_map(
        contribution_map_in=contribution_map_7x7,
        include=include_all,
        plotter=aplt.Plotter(output=aplt.Output(plot_path, format="png")),
    )

    assert path.join(plot_path, "contribution_map.png") in plot_patch.paths
