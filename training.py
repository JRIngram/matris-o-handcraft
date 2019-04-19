'''
Created on 9 Apr 2019

@author: jamie

        Take in an input of column differences
        Find 0s
        Check right column or left difference is 0
        Check opposite column to the one checked above.
        Choose column with the large column difference opposite value.
'''

import random
from random import randint
import copy
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pickle
import time

random.seed(0)
def gen_batch(samples):
    """
    Generates a batch of samples for column differences
    """
    column_differences = []
    column_differences.append([0,0,0,0,0,0,0,0,0,0])
    column_differences.append([0,0,2,0,0,0,0,0,0,0])
    column_differences.append([0,0,0,0,2,0,0,0,0,0])
    column_differences.append([0,0,0,0,0,0,2,0,0,0])
    column_differences.append([0,0,0,0,0,0,0,0,2,0])
    for x in range(0, samples):
        column_difference = [0]
        for y in range(0,9):
            column_difference.append(randint(-2,2) * 2)
        
        zero_locations = []
        for z in range(0, len(column_difference)):
            if column_difference[z] == 0:
                zero_locations.append(z)
                if len(zero_locations) > 1:
                    zero_location = randint(0, len(zero_locations))
                    
                    if zero_location == 0:
                        #make column to the right also 0
                        column_difference[zero_location+1] = 0
                        break
                    elif zero_location == len(column_difference) - 1:
                        #make column to the left also 0
                        column_difference[zero_location-1] = 0
                        break
                    else:
                        left = randint(0,1)
                        if left == 0:
                            #make column to the right 0
                            column_difference[zero_location+1] = 0
                            break
                        else:
                            #make column to the left 0
                            column_difference[zero_location-1] = 0
                            break
        print(column_difference)
        column_differences.append(column_difference)
    return column_differences

def create_appended_batches(batches):
    """
        for each batch:
            Take in an input of column differences
            Find 0s
            Check right column or left difference is 0
            Check opposite column to the one checked above.
            Choose column with the largest column difference opposite value.
    """
    appended_batches=[]
    for batch in batches:       
        zero_locations=[]
        for column_number in range(0, len(batch)):
            if batch[column_number] == 0:
                zero_locations.append([column_number])
        for column in range(0, len(zero_locations)):
            if zero_locations[column][0] < len(batch) - 1: #For all columns that are not the last
                #if batch[column[0]+1] == 0: #Means value next to this cell is also 0
                if zero_locations[column][0] == 0:
                    zero_locations[column].append(0)
                else:
                    placement_column = zero_locations[column][0] - 1
                    zero_locations[column].append(batch[placement_column])
        cleaning = True
        while cleaning == True:
            #Clears zero locations that do not have a 0 next to it
            cleaning = False
            for location in range(0, len(zero_locations)):
                if len(zero_locations) > 0:
                    #print(batch)
                    #print(zero_locations)
                    if len(zero_locations[location]) <= 1:
                        zero_locations.pop(location)
                        location = -1
                        cleaning = True
                        break
        if len(zero_locations) == 0:
            #Ensures there is at least one value 
            zero_locations.append([0,0])
        sorted = sort_two_dimensions(zero_locations)
        target_list = create_target(sorted[0][0])
        appended_batch = [batch,target_list]
        appended_batches.append(appended_batch)
    return appended_batches
        
def sort_two_dimensions(array):
    """
    Sorts a 2D array by its values in the second index in descending order
    """
    sorted_array = copy.deepcopy(array)
    sorting=True
    while sorting == True:
        sorting=False
        for row in range(0, len(sorted_array)):
            if row != 0:
                if sorted_array[row][1] > sorted_array[row-1][1]:
                    sorting=True
                    temp=sorted_array[row-1]
                    sorted_array[row-1] = sorted_array[row]
                    sorted_array[row] = temp
    return sorted_array

def create_target(column_number):
    """
    Creates a 40 item array based off of the column the tetromino should be placed 
    """
    target = []
    for x in range(0, 10):
        """
        if x == column_number or x == (10 + column_number) or x == (20 + column_number) or x == (30 + column_number):
            target.append(2)
        """
        if x == column_number - 1:
            target.append(2)
        else:
            target.append(0)
    return target

def convert_array_to_numpy(array):
    #numpy_array = np.zeros((len(array), 1))
    #for x in range(0, len(array)):
     #   numpy_array[x,0] = array[x]
    x = np.array([array])
    return np.array([array])

def save_neural_network(neural_net):
        """
        Serializes the neural network.
        """
        file_path = "trim-" + str(time.strftime("%d-%m-%y_%H:%M:%S"))
        agent_information = [0.1, False, False, neural_net]
        handler = open(file_path + ".obj", 'wb')
        pickle.dump(agent_information, handler)
        handler.close()

batch_number = 1000 
appended_batches = create_appended_batches(gen_batch(batch_number - 5))
neural_net = Sequential()
neural_net.add(Dense(10, input_dim=10, activation='tanh'))
neural_net.add(Dense(10, activation='linear'))
neural_net.add(Dense(10, activation='linear'))
neural_net.compile(loss='mean_squared_error',
    optimizer='sgd',
    metrics=['accuracy'])
x = appended_batches[0][0]
y = appended_batches[0][1]
convert_array_to_numpy([1,2,3,4,3,2,1])
foo="bar"
training = []
target = []
for x in range(0, batch_number):
    training.append(appended_batches[x][0])
    target.append(appended_batches[x][1])
for x in range(0, 30000): #Decides number of rounds of training
    for training_round in range(0, batch_number):
        print("Round: " + str(x) + " / " + str(30000))
        print("Batch: " + str(training_round))
        training_data = convert_array_to_numpy(training[training_round])
        target_data = convert_array_to_numpy(target[training_round])
        neural_net.fit(training_data, target_data, epochs=1)
print("***********************\n"+str([0,0,4,4,-4,4,2,2,-2,-4]))
print(neural_net.predict(convert_array_to_numpy([0,0,4,4,-4,4,2,2,-2,-4])))
print("***********************\n"+str([0,8,0,0,-4,4,2,2,-2,-4]))
print(neural_net.predict(convert_array_to_numpy([0,8,0,0,-4,4,2,2,-2,-4])))
print("***********************\n"+str([0,8,0,0,-4,4,0,0,-2,-4]))
print(neural_net.predict(convert_array_to_numpy([0,8,0,0,-4,4,0,0,-2,-4])))
print("***********************\n"+str([0,0,0,0,0,0,0,0,0,0]))
print(neural_net.predict(convert_array_to_numpy([0,0,0,0,0,0,0,0,0,0])))
print("***********************\n"+str([0,0,2,0,0,0,0,0,0,0]))
print(neural_net.predict(convert_array_to_numpy([0,0,2,0,0,0,0,0,0,0])))
print("***********************\n"+str([0,0,2,0,0,0,0,0,0,0]))
print(neural_net.predict(convert_array_to_numpy([0,0,2,0,0,0,0,0,0,0])))
print("***********************\n"+str([0,0,0,0,2,0,0,0,0,0]))
print(neural_net.predict(convert_array_to_numpy([0,0,0,0,2,0,0,0,0,0])))
print("***********************\n"+str([0,0,0,0,0,0,2,0,0,0]))
print(neural_net.predict(convert_array_to_numpy([0,0,0,0,0,0,2,0,0,0])))
print("***********************\n"+str([0,0,0,0,0,0,0,0,2,0]))
print(neural_net.predict(convert_array_to_numpy([0,0,0,0,0,0,0,0,2,0])))
print("***********************\nSaving neural network.")
save_neural_network(neural_net)
print("done")


        
