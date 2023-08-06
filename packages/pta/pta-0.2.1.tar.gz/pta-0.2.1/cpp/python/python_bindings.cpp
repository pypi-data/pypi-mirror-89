// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#include <chord_samplers/uniform_pdf_sampler.h>
#include <coordinate_hit_and_run_sampler.h>
#include <descriptors/polytope.h>
#include <hit_and_run_sampler.h>
#include <loggers/console_progress_logger.h>
#include <loggers/directions_logger.h>
#include <loggers/eigen_state_logger.h>
#include <loggers/multi_logger.h>
#include <pybind11/chrono.h>
#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <Eigen/Dense>

#include "python_helper.h"
#include "settings/free_energy_sampling_settings.h"
#include "settings/uniform_flux_sampling_settings.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

using namespace hyperflux;
using namespace samply;

typedef double Scalar;

//==============================================================================
//  Uniform sampling.
//==============================================================================

template <typename ChainState, typename DurationFormat>
using UniformLoggers =
    MultiLogger<ChainState, DurationFormat, EigenStateLogger, ConsoleProgressLogger>;
using UniformSampler =
    CoordinateHitAndRunSampler<Scalar, Polytope, UniformPdfSampler, UniformLoggers>;

py::array_t<double> sample_flux_space_uniform(
    const py::EigenDRef<Eigen::MatrixXd> G,
    const py::EigenDRef<Eigen::MatrixXd> h,
    const py::EigenDRef<Eigen::MatrixXd> from_Fd_T,
    const py::EigenDRef<Eigen::MatrixXd> initial_state,
    const UniformFluxSamplingSettings &settings)
{
    // Redirect stdout to the Python output.
    py::scoped_ostream_redirect stream(std::cout,
                                       py::module_::import("sys").attr("stdout"));

    AffineTransform<double> from_Fd(from_Fd_T, Vector<double>::Zero(G.cols()));

    Polytope<Scalar> descriptor(G, h, from_Fd);
    UniformPdfSampler<Scalar> chord_sampler(G.cols());

    const size_t preallocated_states =
        (settings.num_steps - settings.num_skipped_steps) / settings.steps_thinning;
    UniformSampler::LoggerType loggers(
        UniformSampler::LoggerType::Logger<0>(
            settings.worker_id, settings.steps_thinning, settings.num_skipped_steps,
            preallocated_states),
        UniformSampler::LoggerType::Logger<1>(settings.worker_id,
                                              settings.console_logging_interval_ms));

    UniformSampler sampler(descriptor, chord_sampler, loggers);
    sampler.set_state(initial_state);
    sampler.simulate(settings.num_steps);

    // Copy back resulting samples.
    return python_helper::vector_of_eigen_matrices_to_numpy_3d_array(
        sampler.get_logger().get<0>().get_states());
}

//==============================================================================
//  Thermodynamic space sampling.
//==============================================================================

template <typename ChainState, typename DurationFormat>
using TFSLoggers =
    MultiLogger<ChainState, DurationFormat, EigenStateLogger, DirectionsLogger>;
using TFSSampler = HitAndRunSampler<Scalar,
                                    SteadyStateFreeEnergiesDescriptor,
                                    MvnPdfSampler,
                                    TFSLoggers>;

struct TFSResult {
    py::array_t<double> chains;
    py::array_t<uint8_t> directions;
    py::array_t<uint32_t> direction_counts;
};

TFSResult sample_free_energies(
    const py::EigenDRef<Eigen::MatrixXd> E,
    const py::EigenDRef<Eigen::MatrixXd> f,
    const py::EigenDRef<Eigen::MatrixXd> S,
    const py::EigenDRef<Eigen::MatrixXd> lb,
    const py::EigenDRef<Eigen::MatrixXd> ub,
    const py::EigenDRef<Eigen::Matrix<uint32_t, -1, 1>> constrained_rxns_ids,
    const py::EigenDRef<Eigen::MatrixXd> initial_state,
    const FreeEnergySamplingSettings &settings,
    const py::EigenDRef<Eigen::MatrixXd> vars_to_drg_T,
    const py::EigenDRef<Eigen::MatrixXd> vars_to_drg_shift,
    const py::EigenDRef<Eigen::MatrixXd> direction_transform_T)
{
    AffineTransform<double> vars_to_drg(vars_to_drg_T, vars_to_drg_shift);
    AffineTransform<double> directions_transform(
        direction_transform_T, Vector<double>::Zero(direction_transform_T.rows()));

    Ellipsoid<Scalar> vars_constraints(E * settings.truncation_multiplier, f);
    FluxConstraints flux_constraints{S, lb, ub};
    ThermodynamicConstraints thermo_constraints{
        constrained_rxns_ids.cast<Eigen::Index>(), vars_to_drg};

    SteadyStateFreeEnergiesDescriptor<Scalar> descriptor(
        vars_constraints, flux_constraints, thermo_constraints, directions_transform,
        settings);
    MvnPdfSampler<Scalar> chord_sampler(AffineTransform<double>(E, f));

    const size_t preallocated_states =
        (settings.num_steps - settings.num_skipped_steps) / settings.steps_thinning;

    TFSSampler::LoggerType loggers(
        TFSSampler::LoggerType::Logger<0>(settings.worker_id, settings.steps_thinning,
                                          settings.num_skipped_steps,
                                          preallocated_states),
        TFSSampler::LoggerType::Logger<1>(settings.worker_id,
                                          settings.steps_thinning_directions,
                                          settings.num_skipped_steps));

    TFSSampler sampler(descriptor, chord_sampler, loggers);
    sampler.get_logger().get<1>().set_descriptor(sampler.get_space_descriptor());
    sampler.get_logger().get<1>().set_sampler(sampler.get_chord_sampler());
    sampler.set_state(initial_state);
    sampler.simulate(settings.num_steps);

    // Copy back resulting samples.
    TFSResult result;
    result.chains = python_helper::vector_of_eigen_matrices_to_numpy_3d_array(
        sampler.get_logger().get<0>().get_states()),
    std::tie(result.directions, result.direction_counts) =
        python_helper::direction_counts_to_python(
            sampler.get_logger().get<1>().get_directions_counts());
    return result;
}

//==============================================================================
//  Define Pybind11 bindings.
//==============================================================================

PYBIND11_MODULE(_pta_python_binaries, m)
{
    m.doc() = R"pbdoc(
        PTA binaries interface.
    )pbdoc";

    py::class_<Settings>(m, "SamplerSettings")
        .def(py::init<>())
        .def_readwrite("worker_id", &Settings::worker_id)
        .def_readwrite("num_steps", &Settings::num_steps)
        .def_readwrite("num_chains", &Settings::num_chains)
        .def_readwrite("steps_thinning", &Settings::steps_thinning)
        .def_readwrite("num_skipped_steps", &Settings::num_skipped_steps)
        .def_readwrite("log_interval", &Settings::console_logging_interval_ms)
        .def_readwrite("log_directory", &Settings::log_directory);

    py::class_<UniformFluxSamplingSettings, Settings>(m, "UniformSamplerSettings")
        .def(py::init<>());

    py::class_<FreeEnergySamplingSettings, Settings>(m, "FreeEnergySamplerSettings")
        .def(py::init<>())
        .def_readwrite("truncation_multiplier",
                       &FreeEnergySamplingSettings::truncation_multiplier)
        .def_readwrite("feasibility_cache_size",
                       &FreeEnergySamplingSettings::feasibility_cache_size)
        .def_readwrite("drg_epsilon", &FreeEnergySamplingSettings::drg_epsilon)
        .def_readwrite("flux_epsilon", &FreeEnergySamplingSettings::flux_epsilon)
        .def_readwrite("min_rel_region_length",
                       &FreeEnergySamplingSettings::min_rel_region_length)
        .def_readwrite("steps_thinning_directions",
                       &FreeEnergySamplingSettings::steps_thinning_directions);

    py::class_<TFSResult>(m, "TFSResult")
        .def(py::init<>())
        .def_readwrite("chains", &TFSResult::chains)
        .def_readwrite("directions", &TFSResult::directions)
        .def_readwrite("direction_counts", &TFSResult::direction_counts);

    m.def("sample_flux_space_uniform", &sample_flux_space_uniform);
    m.def("sample_free_energies", &sample_free_energies);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
