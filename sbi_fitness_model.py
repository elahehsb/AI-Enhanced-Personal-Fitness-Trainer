import torch
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
from pyro.optim import Adam

# Define the probabilistic model for fitness
def fitness_model(data):
    fitness_mean = pyro.sample("fitness_mean", dist.Normal(50, 10))
    nutrition_mean = pyro.sample("nutrition_mean", dist.Normal(50, 10))
    recovery_mean = pyro.sample("recovery_mean", dist.Normal(50, 10))
    
    with pyro.plate("data", len(data)):
        observed_fitness = pyro.sample("obs_fitness", dist.Normal(fitness_mean, 5), obs=data['fitness_level'])
        observed_nutrition = pyro.sample("obs_nutrition", dist.Normal(nutrition_mean, 5), obs=data['nutrition_score'])
        observed_recovery = pyro.sample("obs_recovery", dist.Normal(recovery_mean, 5), obs=data['recovery_score'])

# Define the guide (variational distribution)
def fitness_guide(data):
    fitness_mean_loc = pyro.param("fitness_mean_loc", torch.tensor(50.0))
    fitness_mean_scale = pyro.param("fitness_mean_scale", torch.tensor(10.0))
    nutrition_mean_loc = pyro.param("nutrition_mean_loc", torch.tensor(50.0))
    nutrition_mean_scale = pyro.param("nutrition_mean_scale", torch.tensor(10.0))
    recovery_mean_loc = pyro.param("recovery_mean_loc", torch.tensor(50.0))
    recovery_mean_scale = pyro.param("recovery_mean_scale", torch.tensor(10.0))
    
    pyro.sample("fitness_mean", dist.Normal(fitness_mean_loc, fitness_mean_scale))
    pyro.sample("nutrition_mean", dist.Normal(nutrition_mean_loc, nutrition_mean_scale))
    pyro.sample("recovery_mean", dist.Normal(recovery_mean_loc, recovery_mean_scale))

# Generate synthetic data
def generate_data():
    return {
        'fitness_level': np.random.normal(50, 10, 100),
        'nutrition_score': np.random.normal(50, 10, 100),
        'recovery_score': np.random.normal(50, 10, 100)
    }

data = generate_data()
data_tensor = {key: torch.tensor(val, dtype=torch.float32) for key, val in data.items()}

# Run inference
optimizer = Adam({"lr": 0.01})
svi = SVI(fitness_model, fitness_guide, optimizer, loss=Trace_ELBO())

n_steps = 1000
for step in range(n_steps):
    loss = svi.step(data_tensor)
    if step % 100 == 0:
        print(f"Step {step} : Loss = {loss}")

# Extract inferred parameters
inferred_params = {
    "fitness_mean": pyro.param("fitness_mean_loc").item(),
    "nutrition_mean": pyro.param("nutrition_mean_loc").item(),
    "recovery_mean": pyro.param("recovery_mean_loc").item(),
}

print(f"Inferred parameters: {inferred_params}")
