import autofit as af
import autogalaxy as ag
from test_autogalaxy.integration.tests.imaging import runner

test_type = "bulge"
test_name = "galaxy_x1__hyper"
data_name = "galaxy_x1__dev_vaucouleurs"
instrument = "vro"


def make_pipeline(name, path_prefix, search=af.DynestyStatic()):

    pipeline_name = "pipeline__hyper"

    path_prefix = f"{path_prefix}/{pipeline_name}/setup"

    phase1 = ag.PhaseImaging(
        name="phase_1",
        path_prefix=path_prefix,
        galaxies=dict(
            galaxy=ag.GalaxyModel(redshift=0.5, light=ag.lp.EllipticalSersic)
        ),
        settings=ag.SettingsPhaseImaging(grid_class=ag.Grid),
        search=search,
    )

    phase1 = phase1.extend_with_hyper_phase(
        hyper_galaxies_search=True,
        include_background_sky=True,
        include_background_noise=True,
    )

    return ag.PipelineDataset(name, phase1)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])
