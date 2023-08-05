import autofit as af
import autogalaxy as ag
from test_autogalaxy.integration.tests.interferometer import runner

test_type = "galaxy_x1"
test_name = "galaxy_x2__sersics__hyper"
data_name = "galaxy_x2__sersics"
instrument = "sma"


def make_pipeline(name, path_prefix, real_space_mask, search=af.DynestyStatic()):

    bulge_0 = af.PriorModel(ag.lp.EllipticalSersic)
    bulge_1 = af.PriorModel(ag.lp.EllipticalSersic)

    bulge_0.centre_0 = -1.0
    bulge_0.centre_1 = -1.0
    bulge_1.centre_0 = 1.0
    bulge_1.centre_1 = 1.0

    phase1 = ag.PhaseInterferometer(
        name="phase_1",
        path_prefix=path_prefix,
        galaxies=dict(
            galaxy_0=ag.GalaxyModel(redshift=0.5, bulge=bulge_0),
            galaxy_1=ag.GalaxyModel(redshift=0.5, bulge=bulge_1),
        ),
        real_space_mask=real_space_mask,
        search=search,
    )

    phase1.search.const_efficiency_mode = True
    phase1.search.n_live_points = 40
    phase1.search.facc = 0.8

    phase1 = phase1.extend_with_hyper_phase(hyper_galaxies_search=True)

    phase2 = ag.PhaseInterferometer(
        name="phase_2",
        path_prefix=path_prefix,
        galaxies=dict(
            galaxy_0=ag.GalaxyModel(
                redshift=0.5,
                bulge=phase1.result.model.galaxies.galaxy_0.bulge,
                hyper_galaxy=phase1.result.hyper.instance.galaxies.galaxy_0.hyper_galaxy,
            ),
            galaxy_1=ag.GalaxyModel(
                redshift=0.5,
                bulge=phase1.result.model.galaxies.galaxy_1.bulge,
                hyper_galaxy=phase1.result.hyper.instance.galaxies.galaxy_1.hyper_galaxy,
            ),
        ),
        real_space_mask=real_space_mask,
        search=search,
    )

    phase2.search.const_efficiency_mode = True
    phase2.search.n_live_points = 40
    phase2.search.facc = 0.8

    return ag.PipelineDataset(name, phase1, phase2)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])
