// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_ORTHANTS_WEIGHT_CALCULATOR_H
#define HYPERFLUX_ORTHANTS_WEIGHT_CALCULATOR_H

#include <memory>
#include <set>
#include <vector>

#include <Eigen/Dense>
#include <gurobi_c++.h>

#include "eigen-hash.h"
#include "lrucache.hpp"
#include "flux_constraints.h"
#include "rays_packet.h"

namespace hyperflux {

struct Orthants {
	std::vector<size_t> ids;
	samply::Vector<double> weights;
};

/**
 * @brief Class for the verification of the steady state of the steady state
 * condition in a reaction network.
 */
template<typename Scalar>
class OrthantsWeightCalculator {
public:
	/**
	 * @brief Construct a new instance of the SteadyStateVerifier class.
	 *
	 * @param S The stoichiometric matrix of the reaction network.
	 */
	OrthantsWeightCalculator(
		const FluxConstraints& flux_constraints,
		const Eigen::Matrix<Eigen::Index, -1, 1>& has_drg_reaction_ids, 
		const double flux_threshold, const size_t cache_size,
		const samply::Matrix<double>& objective, const double ref_objective,
		const double gamma);

	/**
	 * @brief Verify whether the given flux constraints allow at least one
	 * steady state flux distribution, i.e. whether there is a flux distribution
	 * v such that v_mins[i] <= v <= v_maxs[i] and S*v = 0.
	 *
	 * @param v_mins Matrix composed by column vectors representing
	 * the lower bounds on the reaction fluxes that must be tested for
	 * steady state feasibility.
	 * @param v_maxs Matrix composed by column vectors representing
	 * the upper bounds on the reaction fluxes that must be tested for
	 * steady state feasibility.
	 * @return Vector of booleans determining the steady state feasibility of
	 * the input constraints.
	 */
	Orthants get_steady_state_orthants(
		const samply::RaysPacket<Scalar>& drg_rays,
		const samply::Vector<Scalar>& region_starts,
		const samply::Vector<Scalar>& region_ends,
		const Eigen::VectorXi& ray_indices);

private:
	struct Orthant_ {
		bool is_steady_state;
		double weight;
	};

	typedef cache::lru_cache<samply::Vector<Scalar>, Orthant_> OrthantsCache_;
	/**
	 * @brief Create variables representing the reaction fluxes. The objective
	 * coefficients are set to zero and the variables are added to the current
	 * model.
	 *
	 * @param num_reactions The number of reactions in the network.
	 * @return Array containing the created variables.
	 */
	std::unique_ptr<GRBVar[]> create_v_variables_(
		const FluxConstraints& flux_constraints, 
		const samply::Matrix<double>& objective);

	/**
	 * @brief Create the linear flux constraints based on the stoichiometry. The
	 * constraints are automatically added to the model.
	 *
	 * @param S The stoichiometric matrix of the system.
	 * @return Array containing the created constraints.
	 */
	std::unique_ptr<GRBConstr[]> create_v_constraints_(
		const samply::Matrix<double>& S);

	void create_stedy_state_conditions_(
		const FluxConstraints& flux_constraints);

	bool is_origin_region_(const Scalar region_start, const Scalar region_end);

	Orthant_ is_steady_state_region_(const samply::Vector<Scalar>& drg);

	bool is_influx_outflux_consistent_(
		const samply::Vector<Scalar>& direction_vector);

	std::vector<Eigen::Index> find_constrained_rev_reaction_ids_(
		const Eigen::Matrix<Eigen::Index, -1, 1> has_drg_reaction_ids,
		const FluxConstraints & flux_constriants);

	// The gurobi environment in which the model is created.
	const GRBEnv gurobi_environment;

	// The gurobi model containing the linear program that determines
	// thermodynamic feasibility.
	GRBModel model;

	// Gurobi variables representing the reaction fluxes in the model.
	const std::unique_ptr<GRBVar[]> v_variables;

	// Gurobi constraints on the reaction fluxes based on the stoichiometry of
	// the reaction network.
	const std::unique_ptr<GRBConstr[]> v_constraints;

	const FluxConstraints flux_constraints_;

	const Eigen::Matrix<Eigen::Index, -1, 1> has_drg_reaction_ids_;

	const std::vector<Eigen::Index> has_drg_rev_reaction_ids_;

	samply::Matrix<Scalar> equations_lhs_;
    samply::Vector<Scalar> equations_lhs_offset_;
	samply::Vector<Scalar> equations_rhs_;

	samply::Vector<Scalar> template_direction_;

	OrthantsCache_ cache_;

	Scalar flux_threshold_;

	double reference_objective_;
	double gamma_;
};

//==============================================================================
//	SteadyStateVerifier public methods implementation.
//==============================================================================

template<typename Scalar>
OrthantsWeightCalculator<Scalar>::OrthantsWeightCalculator(
	const FluxConstraints& flux_constraints,
	const Eigen::Matrix<Eigen::Index, -1, 1>& has_drg_reaction_ids,
	const double flux_threshold, const size_t cache_size,
	const samply::Matrix<double>& objective, const double ref_objective,
	const double gamma)
	: gurobi_environment()
	, model(gurobi_environment)
	, v_variables(create_v_variables_(flux_constraints, objective))
	, v_constraints(create_v_constraints_(flux_constraints.S))
	, flux_constraints_(flux_constraints)
	, has_drg_reaction_ids_(has_drg_reaction_ids)
	, has_drg_rev_reaction_ids_(find_constrained_rev_reaction_ids_(
		has_drg_reaction_ids, flux_constraints))
	, flux_threshold_(static_cast<Scalar>(flux_threshold))
	, cache_(cache_size)
	, reference_objective_(ref_objective)
	, gamma_(gamma)
{
	// Use one thread only, since the sampling process is already parallelized
	// at the samples level.
	model.set(GRB_IntParam_Threads, 1);
	model.set(GRB_IntParam_OutputFlag, 0);
    model.set(GRB_DoubleParam_FeasibilityTol, 1e-9);
	model.set(GRB_IntAttr_ModelSense, GRB_MAXIMIZE);

	create_stedy_state_conditions_(flux_constraints);
}

template<typename Scalar>
Orthants OrthantsWeightCalculator<Scalar>::get_steady_state_orthants(
	const samply::RaysPacket<Scalar>& rev_drg_rays,
	const samply::Vector<Scalar>& region_starts,
	const samply::Vector<Scalar>& region_ends, 
	const Eigen::VectorXi& ray_indices)
{
	Orthants steady_state_orthants;
	steady_state_orthants.ids.reserve(region_starts.size());
	std::vector<double> weights;
	weights.reserve(region_starts.size());

	for (Eigen::Index region_idx = 0; region_idx < region_starts.size();
		++region_idx) {

		const Scalar region_start = region_starts(region_idx);
		const Scalar region_end = region_ends(region_idx);
		const int ray_index = ray_indices(region_idx);

		if (is_origin_region_(region_start, region_end) && false) {
			steady_state_orthants.ids.push_back(region_idx);
			weights.push_back(0.0);
		} else {
			const auto region_mid_t = (region_end + region_start) / 2.0;
			const auto region_mid_drg = rev_drg_rays.at(ray_index, region_mid_t);
			const Orthant_ orthant = is_steady_state_region_(region_mid_drg);
			if (orthant.is_steady_state) {
				steady_state_orthants.ids.push_back(region_idx);
				weights.push_back(orthant.weight);
			}
		}
	}

	steady_state_orthants.weights = 
		Eigen::Map<samply::Vector<double>, Eigen::Unaligned>(
			weights.data(), weights.size());
	return steady_state_orthants;
}

//==============================================================================
//	SteadyStateVerifier private methods implementation.
//==============================================================================

template<typename Scalar>
inline bool OrthantsWeightCalculator<Scalar>::is_origin_region_(
	const Scalar region_start, const Scalar region_end)
{
	return region_start <= Scalar(0.0) && Scalar(0.0) <= region_end;
}

template<typename Scalar>
inline typename OrthantsWeightCalculator<Scalar>::Orthant_ 
OrthantsWeightCalculator<Scalar>::is_steady_state_region_(
	const samply::Vector<Scalar>& rev_drg)
{
	const samply::Vector<Scalar> directions = -rev_drg.array().sign();
	if (!is_influx_outflux_consistent_(directions))
		return { false, 0.0 };

	if (cache_.exists(directions))
		return cache_.get(directions);

	constexpr Scalar infinity = std::numeric_limits<Scalar>::infinity();
	const size_t num_constraints = has_drg_rev_reaction_ids_.size();

	const samply::Vector<Scalar> v_mins = (rev_drg.array() < Scalar(0)).select(
		samply::Vector<Scalar>::Ones(num_constraints) * flux_threshold_ * 0.001,
		-infinity);
	const samply::Vector<Scalar> v_maxs = (rev_drg.array() > Scalar(0)).select(
		samply::Vector<Scalar>::Ones(num_constraints) * -flux_threshold_ * 0.001,
		infinity);

	for (size_t constraint_idx = 0u; constraint_idx < num_constraints;
		++constraint_idx) {
		const auto reaction_idx = has_drg_rev_reaction_ids_[constraint_idx];
		const double vmin = static_cast<double>(std::max(v_mins(constraint_idx),
			flux_constraints_.lower_bounds(reaction_idx)));
		const double vmax = static_cast<double>(std::min(v_maxs(constraint_idx),
			flux_constraints_.upper_bounds(reaction_idx)));

		v_variables[reaction_idx].set(GRB_DoubleAttr_LB, vmin);
		v_variables[reaction_idx].set(GRB_DoubleAttr_UB, vmax);
	}

	// Optimize the model. If a solution exists, then the constraints allow
	// a steady state flux distribution.
	model.optimize();
	bool is_steady_state = model.get(GRB_IntAttr_Status) == GRB_OPTIMAL;
	Orthant_ orthant{ is_steady_state, 0.0 };
	if (is_steady_state) {
		const double objective_value =  model.get(GRB_DoubleAttr_ObjVal);
		const double weight = exp(
			(objective_value - reference_objective_) / reference_objective_ * gamma_);
		orthant.weight = weight;
	}

	cache_.put(directions, orthant);
	return orthant;
}

template<typename Scalar>
inline bool OrthantsWeightCalculator<Scalar>::is_influx_outflux_consistent_(
	const samply::Vector<Scalar>& direction_vector)
{
	const auto lhs = (equations_lhs_ * direction_vector +
        equations_lhs_offset_).cwiseAbs();
	return (lhs.array() < equations_rhs_.array()).all();
}

template<typename Scalar>
inline std::unique_ptr<GRBVar[]>
OrthantsWeightCalculator<Scalar>::create_v_variables_(
	const FluxConstraints& flux_constraints,
	const samply::Matrix<double>& objective)
{
	return std::unique_ptr<GRBVar[]>(model.addVars(
		flux_constraints.lower_bounds.data(),
		flux_constraints.upper_bounds.data(), objective.data(), nullptr, 
		nullptr, static_cast<int>(flux_constraints.upper_bounds.size())));
}

template<typename Scalar>
inline std::unique_ptr<GRBConstr[]>
OrthantsWeightCalculator<Scalar>::create_v_constraints_(
	const samply::Matrix<double>& S)
{
	const size_t num_metabolites = S.rows();
	const size_t num_reactions = S.cols();

	// Create the linear expressions according to the stoichiometric matrix.
	const std::unique_ptr<GRBLinExpr[]> linear_expressions(
		new GRBLinExpr[num_metabolites]);
	for (size_t metabolite_idx = 0u; metabolite_idx < num_metabolites;
		metabolite_idx++) {
		for (size_t reaction_idx = 0u; reaction_idx < num_reactions;
			reaction_idx++) {

			GRBLinExpr& expression = linear_expressions[metabolite_idx];
			const double coefficient = S(metabolite_idx, reaction_idx);
			if (coefficient != 0) {
				expression += GRBLinExpr(
					v_variables[reaction_idx], coefficient);
			}
		}
	}

	// Set constraint senses and right-hand sides.
	std::unique_ptr<char[]> senses(new char[num_metabolites]);
	std::unique_ptr<double[]> rhs_values(new double[num_metabolites]);
	for (size_t metabolite_idx = 0u; metabolite_idx < num_metabolites;
		metabolite_idx++) {

		senses[metabolite_idx] = '=';
		rhs_values[metabolite_idx] = 0.0;
	}

	// Finally create and return the constraints.
	return std::unique_ptr<GRBConstr[]>(model.addConstrs(
		linear_expressions.get(), senses.get(), rhs_values.get(), nullptr,
		static_cast<int>(num_metabolites)));
}

template<typename Scalar>
inline void OrthantsWeightCalculator<Scalar>::create_stedy_state_conditions_(
	const FluxConstraints& flux_constraints)
{
	const size_t num_metabolites = flux_constraints.S.rows();
	const size_t num_reactions = flux_constraints.S.cols();

	std::set<size_t> constrained_reaction_ids(
		has_drg_reaction_ids_.begin(), has_drg_reaction_ids_.end());
	std::vector<size_t> unconstrained_reaction_idx;
	for (size_t reaction_idx = 0u; reaction_idx < num_reactions;
		++reaction_idx) {
		if (flux_constraints.lower_bounds(reaction_idx) < 0 &&
			flux_constraints.upper_bounds(reaction_idx) > 0 &&
			(constrained_reaction_ids.find(reaction_idx) ==
				constrained_reaction_ids.end()))
			unconstrained_reaction_idx.push_back(reaction_idx);
	}
	const auto unconstrained_S =
		flux_constraints.S(Eigen::all, unconstrained_reaction_idx).eval();

	std::vector<size_t> constrained_metabolite_ids;
	constrained_metabolite_ids.reserve(num_metabolites);
	for (size_t metabolite_idx = 0u; metabolite_idx < num_metabolites;
		++metabolite_idx) {
		if (!(unconstrained_S.row(metabolite_idx).array() != 0).any())
			constrained_metabolite_ids.push_back(metabolite_idx);
	}

	equations_lhs_ = flux_constraints_.S(
		constrained_metabolite_ids, Eigen::all);
	equations_rhs_ = equations_lhs_.cwiseAbs().rowwise().sum();

	template_direction_ = samply::Vector<Scalar>::Zero(num_reactions);
	template_direction_ = (flux_constraints.lower_bounds.array() >= 0)
		.select(1, template_direction_);
	template_direction_ = (flux_constraints.upper_bounds.array() <= 0)
		.select(-1, template_direction_);

	// Simplify the system of equations by precomputing the part related to 
	// irreversible reactions.
	equations_lhs_offset_ = equations_lhs_ * template_direction_;
	const samply::Matrix<Scalar> tmp(
            equations_lhs_(Eigen::all, has_drg_rev_reaction_ids_));
	equations_lhs_ = tmp;
}

template<typename ScalarType>
inline std::vector<Eigen::Index>
OrthantsWeightCalculator<ScalarType>::find_constrained_rev_reaction_ids_(
	const Eigen::Matrix<Eigen::Index, -1, 1> has_drg_reaction_ids,
	const FluxConstraints& flux_constriants)
{
	std::vector<Eigen::Index> constrained_rev_reactions_ids;
	constrained_rev_reactions_ids.reserve(has_drg_reaction_ids.size());

	// Find indices of all the reversible constrained reactions.
	for (const Eigen::Index i : has_drg_reaction_ids) {
		if (flux_constraints_.lower_bounds[i] < 0 &&
			flux_constraints_.upper_bounds[i] > 0) {
			constrained_rev_reactions_ids.push_back(i);
		}
	}

	return constrained_rev_reactions_ids;
}

} // namespace hyperflux

#endif