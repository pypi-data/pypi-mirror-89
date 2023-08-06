# Probabilistic Thermodynamic Analysis of Metabolic Networks
[![Join the chat at https://gitter.im/CSB-ETHZ/PTA](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/CSB-ETHZ/PTA?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Probabilistic Thermodynamic Analysis (PTA) is a framework for the exploration of
the thermodynaic properties of a metabolic network. In PTA, we consider the 
*thermodynamic space* of a network, that is, the space of standard reaction 
energies and metabolite concentrations that are compatible with steady state
flux constraints. The uncertainty of the variables in the thermodynamic space is 
modeled with a probability distribution, allowing analysis with optimization and
sampling approaches:
- **Probabilistic Metabolic Optimization (PMO)** aims at finding the most probable 
values of reaction energies and metabolite concentrations that are compatible 
with the steady state constrain. This method is particularly useful to indentify
features of the network that are thermodynamically unrealistic. For example, PMO
can identify substrate channeling, incorrect cofactors or inaccurate 
directionalities.
- **Thermodynamic and Flux Sampling (TFS)** allows to jointly sample the 
thermodynamic and flux spaces of a network. The method provides estimates of 
metabolite concentrations, reactions directions, and flux distributions.

## Cite us

If you use PTA in a scientific publication, please cite our paper:

Gollub, M.G., Kaltenbach, H.M., Stelling, J., 2020. "Probabilistic Thermodynamic 
Analysis of Metabolic Networks". *biorXiv*. - 
[pdf](https://www.biorxiv.org/content/10.1101/2020.08.14.250845v1.full.pdf)

## Installation
The complete installation of `PTA` has several dependencies. However, what you 
actually need to install depends on the functionalities you want to use. Reproducing 
the results in [[1]](https://gitlab.com/csb.ethz/pta/-/edit/master/README.md#references) requires a complete installation.

### Base installation

The base installation allows to run PMO on existing thermodynamic models.

1.  Install MATLAB R2019a (or newer) with the Parallel Computing Toolbox.
2.  Download and install the [Gurobi](https://www.gurobi.com/) solver, installing the MATLAB [interface](https://www.gurobi.com/documentation/9.0/quickstart_windows/matlab_setting_up_grb_for_.html). Academic licenses are available for free.  
3.  Download and install the [COBRA Toolbox](https://opencobra.github.io/cobratoolbox/stable/installation.html).
4.  Clone the `PTA` repository, including its submodules.
    ```
    git clone --recurse-submodules https://gitlab.com/csb.ethz/pta.git pta
    ```
5. In MATLAB, navigate to the `MATLAB` folder and execute the initialization script.
    ```
    initPta();
    savepath            % Optional. Alternatively, you can execute initPta() every time you start MATLAB.
    ```

### Tools for constructing thermodynamic models

1. *(Optional, only for generating compressed models)* Download and install [CellNetAnalyzer (CNA)](https://www2.mpi-magdeburg.mpg.de/projects/cna/download.html) and its dependencies (efmtool and IBM CPLEX). Refer to CNA's documentation for detailed instructions. \
   *Note:* Only the examples based on iML1515 require CNA and its dependencies. You can skip this step if you only use the core model examples or custom models.
2. Install the [equilibrator-api](https://gitlab.com/equilibrator/equilibrator-api) Python package, version `0.2.9` (available through pip). It is recommended to do that in a virtual environment such as Anaconda.
3. Edit the `config/config.yaml` file to reflect your python installation. Specify the name of the Python executable you want to use and, if needed, how to activate the desired virtual environment (see examples in the file).

### Compiling the samplers for TFS

TFS uses two samplers, one for the thermodynamic space and one for the flux
space. The samplers consist of high performance code written in C++, with MEX
interface for MATLAB.
1. Make sure you have cmake and a compiler supporting C++ 14 (e.g. GCC, MSVC or 
XCode depending on your system). Note that MATLAB has strict 
[requirements](https://www.mathworks.com/support/requirements/supported-compilers.html) 
regarding which compilers are supported.
2. On **Linux** and **OSX** systems: configure, build and install the CMake project:
   ```
   mkdir pta/cpp/build
   cd pta/cpp/build
   cmake -DCMAKE_BUILD_TYPE=Release ..  
   make install
   ```
   On **Windows** systems: open the repository in Visual Studio. Configure (using `Release` configuration), build and install the CMake project 
   using the integrated tools.

**Note**: the CMake project automatically uses all the instructions available on your
CPU. If you are compiling binaries for a different machine, specify the 
architecture of the target machine adding the `-DTARGET_ARCHITECTURE=<arch-name>` 
flag. Check 
[cpp/cmake/OptimizeForArchitecture.cmake](https://gitlab.com/csb.ethz/pta/-/blob/master/cpp/cmake/OptimizeForArchitecture.cmake#L134)
for additional information.

## Usage

### Examples
- `analysis/examples/e_coli_core/EColiCoreExample.m`: minimal example for
constructing a thermodynamic model of *E. coli*'s core metabolism and running
PMO on it.
- `analysis/examples/Recon3D/Recon3DExample`: minimal example for
adding thermodynamic constraints to glycolysis in Recon3D and running PMO on it.
Modeling thermodynamics for specific pathways only reduces coverage but results 
in significant speed up.

### Analysis of *E. coli* metabolism.
These scripts have been used to analyze iML1515-CAN (reduced version of iML1515, 
focused on **C**arbon, **A**mino acid and **N**ucelotide metabolism) in 
[[1]](https://gitlab.com/csb.ethz/pta/-/edit/master/README.md#references)
using data from [[2]](https://gitlab.com/csb.ethz/pta/-/edit/master/README.md#references). 
All results are saved in `data/results/`. We generated the figures using the R scripts in 
`analysis/pta_paper/figures`.
- `analysis/pta_paper/runModelsAnalysis.m` PMO analysis of iML1515-CAN. The
script covers the identification of thermodynamic inconsistencies and the 
quantitative assesment of the model using metabolomics data.
- `analysis/pta_paper/runSamplingWithoutMetabolomics.m` Application of TFS to 
the iML1515-CAN model in different growth conditions without integrating 
metabolomics data. As comparison, the script also samples the models with 
uniform sampling and estimates concentration ranges with TMFA.
- `analysis/pta_paper/runSamplingWithMetabolomics.m` Application of TFS to 
the iML1515-CAN model in different growth conditions integrating 
metabolomics data. As comparison, the script also samples the models with 
uniform sampling and estimates concentration ranges with TMFA.

*Note*: Simulation of a chain in the examples above requires about 10 hours on a
single core depending on the system. We ran 200 chains to gain confidence 
on the convergene time, however this may be prohibitive on personal computers.
Users that want to run the complete simulation but do not have access to an HPC 
system can optionally reduce the number of chains to the number of cores on 
their machine (`freeEnergySampling.samplerSettings.nChains` in 
`analysis/pta_paper/gerosa2015/settings/iML1515_CAN_with[out]_metabolomics.yaml`). 
Alternatively, the example below runs the same sampling pipeline on a core 
model, where the entire analysis only takes few minutes on a personal computer.

- `analysis/pta_paper/runCoreModelExample.m` Constructs and samples an *E. coli*
  core model using the same pipeline and data as in the scripts above.

### General workflow

A complete model analysis with PTA typically consists of the following steps:
1. Create a `.yaml` file describing how to construct and annotate the model.
   This file specifies: the input model (e.g. iML1515), possible modifications to 
   the model (e.g. to address thermodynamic inconsistencies) and estimates relevant 
   for thermodynamics (pH, ionic strength, metabolite concentrations, ...). TODO EXAMPLE
2. Use `cobragen` to generate the model and retrieve estimates of standard 
   reaction energies:
   ```
   model = cobragen.generateCobraModelFromYaml('my_model.yaml')
   model = removeRxns(model, findBlockedReaction(model));
   model = cobragen.addThermodynamicDataToModel(model)
   ```
   Note that in PTA, every reaction must have a well-defined direction, thus we 
   remove blocked reations in advance.
3. Run PMO.
4. Analyze the PMO results and curate the model if needed.
5. Sample the thermodynamic space of the model.
6. Sample fluxes conditioned on the distributions of reaction directions found 
in (5).

### References

1. Gollub, M.G., Kaltenbach, H.M., Stelling, J., 2020. "Probabilistic Thermodynamic 
Analysis of Metabolic Networks". *biorXiv*.
2. Gerosa, L., van Rijsewijk, B.R.H., Christodoulou, D., Kochanowski, K., Schmidt, T.S., Noor, E. and Sauer, U., 2015. Pseudo-transition analysis identifies the key regulators of dynamic metabolic adaptations from steady-state data. *Cell systems*, 1(4), pp.270-282.