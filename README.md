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

## Minimal examples

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

<img width="400" alt="image" src="https://github.com/RaunakDey/phamily/assets/39820997/44a2f67e-6d66-46c5-bdd6-4d862e22009d">

### One-step growth curve for bacteriophages

Initialize your nodes in the model.

```python
latent_period = 1

ecoli = Node('susceptible', 'ecoli', value=1e4)
lambda_virus = Node('free_virus','lambda',value= 2e3)
exposed = Node('exposed','exposed-coli',multiple_compartments=True,latent=True,value = 0,number_of_latent_variables=10)
connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)

```

Build your model by writing the connections, or edges of a network

```python
#E-coli growing
connection1 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'growth_rate':1, 'linear_model_mult_constant': 1}})
connection1.connection_value = connection1.connections(name = 'type-I' )

#Ecoli getting exposed
connection2 = Connect(ecoli,exposed,lambda_virus)
connection2.connection_value = connection2.connections(name='new-infection')

#Exposed cells grow
connection3 = Connect(exposed,ecoli,lambda_virus)
connection3.connection_value = connection3.connections(name='new-infection')

#Transition across exposed compartments
connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)
### Debug this!!!!
connect_lastcompartment_to_one(exposed,Node,lambda_virus,func_name='lysis')

# Virus getting adsorped to all types of hosts
connect_one_to_multi(lambda_virus,exposed,Node,parameters_input_list=None,func_name='adsorption')
connection4 = Connect(lambda_virus,ecoli)
connection4.connection_value = connection4.connections(name='adsorption')

```
Simulate and visualize

```python
# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 3.15, 0.01)
dt = time[1] - time[0]
solution = solve_network_euler(time,initial_values)
```
<img width="400" alt="image" src="https://github.com/RaunakDey/phamily/assets/39820997/09579321-fa05-43b3-b446-9c970e814f9a">


## Contributors

The models are designed, tested and implemented by the members of the [Weitz group](https://weitzgroup.biosci.gatech.edu) at Georgia Institute of Technology. 





 
