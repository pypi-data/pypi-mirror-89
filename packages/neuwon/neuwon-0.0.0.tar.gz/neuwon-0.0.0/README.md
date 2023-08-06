# NEUWON

NEUWON is a simulation framework for neuroscience and artificial intelligence
specializing in conductance based models. This software is a modern remake of
the NEURON simulator. It is accurate, efficient, and easy to use.

## Model Architecture

Models are composed of three types of components: physical structures,
reactions, and diffusions.

#### Physical Structures

Neurons are composed of discrete segments which are connected into a tree
structure. The shape of each segment is a frustum, also known as a truncated
cone. The physical locations of the tips of the frustums in the system serve as
tracking points for all cellular processes: intracellular, extracellular, and
membrane-related. The extracellular space is partitioned into voronoi cells
which are centered on the tracking points. NEUWON provides the following
geometric properties for each tracking point:

* Cell Segment Properties
    + Length
    + Diameter
    + Cross-sectional Area
    + Membrane Surface Area
    + Intracellular Volume
    + Tree Structure
        - Parent Segment, unless segment is root of tree
        - Child Segments, list
* Extracellular Space Properties
    + Volume
    + Adjacent Tracking Points
        - Distance between points
        - Surface Area of border

#### Reactions

Chemical reactions are one of the mechanisms which the brain uses to implement
differential equations. Complex reactions are capable of performing arbitrary
calculations and large proteins can maintain a persistent state. Proteins
embedded in the cell membrane can react to the electrical potential across the
membrane, and can control the flow of chemicals across the membrane.

#### Diffusions and Electrotonics

Diffusion is the primary means of communication between locations in the brain.
Chemicals diffuse through the intracellular and extracellular fluids and across
cell membranes. Diffusion is modeled with a linear & time-invariant systems of
differential equations, and so it can be simulated using specialized method
which are both exact and efficient (Rotter & Diesmann, 1999). Electrically
charged ions flow throughout neurons; a phenomenon which is modeled with an
equivalent electrical circuit. The equivalent circuit is a linear &
time-invariant system of differential equations, and so it is also simulated
using the specialized methods.

### Integration Methods

Reactions and diffusions interact at staggered time steps, as explained in
chapter 4 of the NEURON book.
[Mention that mechanisms & reactions are reported at the unstable timepoint.]

[Talk about exact integration in more detail]

## Usage

#### Installation

Prerequisites:
* [Python 3](https://www.python.org/)
* numpy & scipy

TODO: Install & Test instructions

#### Model Specification

TODO Document how to use the model builder class.
