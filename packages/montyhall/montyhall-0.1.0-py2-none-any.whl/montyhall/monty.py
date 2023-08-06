
class MontyHall():

    def __init__(self, numberDoors = 3, numberIterations = 100, numberExperiments = 100):
        """
        This calls the Monty Hall function
        Params:
            numberDoors The number of doors on the experiment. Default is 3
            numberIterattions The number of iterations for each experiment. Default is 100
            numberExperiments The number of experiments. Default is 100
        """
        self.numberDoors = numberDoors
        self.numberIterations = numberIterations
        self.numberExperiments = numberExperiments
  
    def createExperiment(self, switch):
        """
        This function creates an experiment
        Params:
            switch: A boolean value if the the switch function will be used on the experiment
        Returns:
            A float value
        """  
        numberIterations = self.numberIterations
        numberDoors = self.numberDoors

        import random as r
        
        doors = [x for x in range(numberDoors)]
        result = 0
        for _ in range(numberIterations):
            prizedDoor = r.choice(doors)
            pickedDoor = r.choice(doors)
            openedDoor = r.sample([x for x in doors if x not in [prizedDoor, pickedDoor]], numberDoors - 2)
            if switch:
                pickedDoor = r.choice([x for x in doors if x not in openedDoor + [pickedDoor]])
            if pickedDoor == prizedDoor:
                result+=1
            
        return result / numberIterations
  
    def runExperiments(self):
        """
        This function runs a series of experiments to compare results with switch or no swith
        params:
            None
        returns:
            A pandas dataframe
        """ 
        import pandas as pd
        result = pd.DataFrame()
        for i in range(self.numberExperiments):
            result = result.append(pd.DataFrame({'i': [i], 'switch': [True], 'value': self.createExperiment(True)}))
            result = result.append(pd.DataFrame({'i': [i], 'switch': [False], 'value': self.createExperiment(False)}))
      
        return result