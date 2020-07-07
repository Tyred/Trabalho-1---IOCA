###################################################
# DC - Departamento de Computação UFSCar          #
#                                                 #
# Bacharelado em Ciência da Computação - 018      #
#                                                 #
# Introdução a Otimização Combinatória Aplicada   # 
#                                                 # 
# Trabalho 1                                      #
#                                                 #
# Autor: Yuri Gabriel Aragão da Silva  RA: 758608 #
#                                                 #
###################################################

from collections import namedtuple

from ortools.linear_solver.pywraplp import Solver

time_limit = 1000000 # miliseconds

Item = namedtuple("Item", ['index', 'value', 'weight'])

DEBUG = 0

def solve_it(input_data):
	# parse the input
	lines = input_data.split('\n')

	firstLine = lines[0].split()
	item_count = int(firstLine[0])
	capacity = int(firstLine[1])
	conflict_count = int(firstLine[2])

	items = []
	conflicts = []

	for i in range(1, item_count+1):
		line = lines[i]
		parts = line.split()
		items.append(Item(i-1, int(parts[0]), int(parts[1])))

	for i in range(1, conflict_count+1):
		line = lines[item_count + i]
		parts = line.split()
		conflicts.append((int(parts[0]), int(parts[1])))

	return knapsack(item_count, items, capacity, conflict_count, conflicts)


def knapsack(num_items, items, capacity, num_conflicts, conflicts):

	if DEBUG >= 1:
		print(f"numero de itens = {num_items}")
		print(f"capacidade da mochila = {capacity}")
		print(f"numero de conflitos = {num_conflicts}")

	if DEBUG >= 2:
		print("Itens na ordem em que foram lidos")
		for item in items:
			print(item)
		print()

	if DEBUG >= 2:
		print("Conflitos na ordem em que foram lidos")
		for conflict in conflicts:
			print(conflict)
		print()

	# Modify this code to run your optimization algorithm

	solution = [0]*num_items
	result_value = 0
	solution_weight = 0

	# Baseado na aula de cobertura por conjuntos com OR-Tools   
	solver = Solver('SolveIntegerProblem',Solver.CBC_MIXED_INTEGER_PROGRAMMING)

	solver.SetTimeLimit(time_limit)

	# Create the decision variables
	x = []
	for j in range(0, num_items):
		x.append(solver.IntVar(0.0, 1.0, 'x[%d]' % j))

	# Define the constraints
	constraint_type1 = solver.Constraint(0, capacity)
	for i in range(0, num_items):
		constraint_type1.SetCoefficient(x[i], items[i].weight) # With weight constraints
	
	# Solve the conflicts (I hope) 
	for conflict in conflicts:
		solver.Add(solver.Sum((x[conflict[0]], x[conflict[1]])) <= 1)

	# Define the objective of the solver
	objective = solver.Objective()
	objective.SetMaximization()
	for i in range(0, num_items):
		objective.SetCoefficient(x[i], items[i].value) # Maximize the value
   
	result_status = solver.Solve()
	
	if result_status == Solver.OPTIMAL:
		result_value = int(solver.Objective().Value())  
	elif result_status == Solver.FEASIBLE:
		result_value = int(solver.Objective().Value())
	else:
		result_value = -1

	for i in range(0, num_items):
		solution[i] = int(x[i].solution_value())
		
	# Naive solution
	#for item in items:
	#    if solution_weight + item.weight <= capacity:
	#        solution[item.index] = 1
	#        solution_value += item.value
	#        solution_weight += item.weight

	# prepare the solution in the specified output format
	output_data = str(result_value) + '\n'
	output_data += ' '.join(map(str, solution))

	return output_data


if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		with open(file_location, 'r') as input_data_file:
			input_data = input_data_file.read()
		output_data = solve_it(input_data)
		print(output_data)
		solution_file = open(file_location + ".sol", "w")
		solution_file.write(output_data)
		solution_file.close()
	else:
		print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')