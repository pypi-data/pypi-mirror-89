from autoconf import conf
import autofit as af
from autoarray.inversion import pixelizations as pix
from autoarray.exc import PixelizationException, InversionException, GridException
from autofit.exc import FitException
from autogalaxy.pipeline.phase.dataset import analysis as ag_analysis
from autolens.fit import fit
from autolens.pipeline import visualizer
from autolens.pipeline.phase.dataset import analysis as analysis_dataset
from autogalaxy.pipeline.phase.imaging.analysis import Attributes as AgAttributes

import copy


class Analysis(ag_analysis.Analysis, analysis_dataset.Analysis):
    def __init__(self, masked_imaging, settings, cosmology, results=None):

        super().__init__(
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
        tracer = self.tracer_for_instance(instance=instance)

        self.settings.settings_lens.check_positions_trace_within_threshold_via_tracer(
            tracer=tracer, positions=self.masked_dataset.positions
        )

        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)

        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        try:
            fit = self.masked_imaging_fit_for_tracer(
                tracer=tracer,
                hyper_image_sky=hyper_image_sky,
                hyper_background_noise=hyper_background_noise,
            )
            return fit.figure_of_merit
        except (
            PixelizationException,
            InversionException,
            GridException,
            OverflowError,
        ) as e:
            raise FitException from e

    def masked_imaging_fit_for_tracer(
        self, tracer, hyper_image_sky, hyper_background_noise, use_hyper_scalings=True
    ):

        return fit.FitImaging(
            masked_imaging=self.masked_dataset,
            tracer=tracer,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
            use_hyper_scaling=use_hyper_scalings,
            settings_pixelization=self.settings.settings_pixelization,
            settings_inversion=self.settings.settings_inversion,
        )

    def stochastic_log_evidences_for_instance(self, instance):

        instance = self.associate_hyper_images(instance=instance)
        tracer = self.tracer_for_instance(instance=instance)

        if not tracer.has_pixelization:
            return

        if not isinstance(
            tracer.pixelizations_of_planes[-1], pix.VoronoiBrightnessImage
        ):
            return

        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)

        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        settings_pixelization = (
            self.settings.settings_pixelization.settings_with_is_stochastic_true()
        )

        log_evidences = []

        for i in range(self.settings.settings_lens.stochastic_samples):

            try:
                log_evidence = fit.FitImaging(
                    masked_imaging=self.masked_dataset,
                    tracer=tracer,
                    hyper_image_sky=hyper_image_sky,
                    hyper_background_noise=hyper_background_noise,
                    settings_pixelization=settings_pixelization,
                    settings_inversion=self.settings.settings_inversion,
                ).log_evidence
            except (
                PixelizationException,
                InversionException,
                GridException,
                OverflowError,
            ) as e:
                log_evidence = None

            if log_evidence is not None:
                log_evidences.append(log_evidence)

        return log_evidences

    def visualize(self, paths: af.Paths, instance, during_analysis):

        self.visualizer.visualize_imaging(paths=paths)

        instance = self.associate_hyper_images(instance=instance)
        tracer = self.tracer_for_instance(instance=instance)
        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)
        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        fit = self.masked_imaging_fit_for_tracer(
            tracer=tracer,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
        )

        if tracer.has_mass_profile:

            try:

                visualizer = self.visualizer.new_visualizer_with_preloaded_critical_curves_and_caustics(
                    preloaded_critical_curves=tracer.critical_curves,
                    preloaded_caustics=tracer.caustics,
                )

            except (Exception, IndexError, ValueError):

                visualizer = self.visualizer

        else:

            visualizer = self.visualizer

        try:
            visualizer.visualize_ray_tracing(
                paths=paths, tracer=fit.tracer, during_analysis=during_analysis
            )
        except Exception:
            pass

        try:
            visualizer.visualize_fit(
                paths=paths, fit=fit, during_analysis=during_analysis
            )
        except Exception:
            pass

        self.visualizer.visualize_hyper_images(
            paths=paths,
            hyper_galaxy_image_path_dict=self.hyper_galaxy_image_path_dict,
            hyper_model_image=self.hyper_model_image,
            contribution_maps_of_galaxies=tracer.contribution_maps_of_planes,
        )

        if self.visualizer.plot_fit_no_hyper:

            fit = self.masked_imaging_fit_for_tracer(
                tracer=tracer,
                hyper_image_sky=None,
                hyper_background_noise=None,
                use_hyper_scalings=False,
            )

            try:
                visualizer.visualize_fit(
                    paths=paths,
                    fit=fit,
                    during_analysis=during_analysis,
                    subfolders="fit_no_hyper",
                )
            except Exception:
                pass

    def make_attributes(self):
        return Attributes(
            cosmology=self.cosmology,
            positions=self.masked_dataset.positions,
            hyper_model_image=self.hyper_model_image,
            hyper_galaxy_image_path_dict=self.hyper_galaxy_image_path_dict,
        )

    def save_results_for_aggregator(
        self, paths: af.Paths, samples: af.OptimizerSamples
    ):

        if conf.instance["general"]["hyper"]["stochastic_outputs"]:
            self.save_stochastic_outputs(paths=paths, samples=samples)


class Attributes(AgAttributes):
    def __init__(
        self, cosmology, positions, hyper_model_image, hyper_galaxy_image_path_dict
    ):
        super().__init__(
            cosmology=cosmology,
            hyper_model_image=hyper_model_image,
            hyper_galaxy_image_path_dict=hyper_galaxy_image_path_dict,
        )

        self.positions = positions
