# montyHall
Monty Hall is a package that allows you to run the Monty Hall paradox experiment.

# Installation instructions
```python
pip install montyhall
```
# usage
```python
import montyhall

# call the class
monty = montyhall.MontyHall(numberDoors=3, numberIterations=100, numberExperiments=100)

# run a single experiment. This function will return a float value
print(monty.createExperiment(switch=True))

#run a serie of experiments. This functionwill return a pandas dataframe
print(monty.runExperiments())
```