from util.population import *
import matplotlib.pyplot as plt
from main import EXIT_STR

print('\nWhich population history would you like to visualize?\n')

print(Population.list_all_saved())

while True:
    name = input('Choice (or exit): ')

    if name == EXIT_STR:
        print('Exiting...')
        exit()

    if Population.is_valid_population_directory(name):
        break
    else:
        print('\nInvalid choice.\n')

pop = Population.load_from_dir(name)

plt.plot(
    pop.generational_fitnesses,
    label=pop.dir_name
)

plt.xlabel('Generation')
plt.ylabel('Max Fitness')
plt.legend()
plt.show()
