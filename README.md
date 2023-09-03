# PHAMILY -- network model for PHAge MIcrobe LYsis LYsogeny
WARNING: UNDER DEVELOPMENT NOW -- minimal usage should be ready by end of July.
A large scale latent variable compartmental model for simulating abundance/population time series of interacting phages and microbes that undergoes lysis or lysogeny in presence of the phages, depending on other biotic, abiotic or environmental factors. PHAMILY is an extension of an older modeling toolkit VIMIMO (Virus Microbe Modeller) -- which is archived at https://github.com/RaunakDey/VIMIMO-Virus-Microbe-modeller (will be made public in July).

* PHAMILI (with an **I**) is part of the package that models the 'Lysis **I**nhibition' phenomena in these infection systems.
* PHAMILE (with an **E**) part models the '**E**nvironmental' factors that modifies the lysis behavior of these cells.

## Types of connections
* One to one
* One to multi-compartments in series
* Multi-compartments in series to one
* Multi-compartments to multi-compartments in parallel
* One to many
* Many to one

<img width="992" alt="image" src="https://github.com/RaunakDey/phamily/assets/39820997/3fab7dd8-0aa7-490b-bf2a-7ada92b06a6b">

## Minimal example

### Logistic growth

```python
ecoli = Node('susceptible', 'ecoli', value=1e4)
connection2 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'carrying_cap' : 70000,'growth_rate' : 0.3}})
connection2.connection_value = connection2.connections(name = 'logistic-growth')
# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 20, 0.01)
dt = time[1] - time[0]

solution = solve_network_euler(time,initial_values)
plot_node_time_series_euler(solution,Node,time,semilog=False)


```
which results in the solution visualized below.

<img width="389" alt="image" src="https://github.com/RaunakDey/phamily/assets/39820997/44a2f67e-6d66-46c5-bdd6-4d862e22009d">



## Contributors

The models are designed, tested and implemented by the members of the [Weitz group](https://weitzgroup.biosci.gatech.edu) at Georgia Institute of Technology. 





 
