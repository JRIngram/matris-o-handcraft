'''
Created on 9 Apr 2019

@author: jamie

        Take in an input of column differences
        Find 0s
        Check right column or left difference is 0
        Check opposite column to the one checked above.
        Choose column with the large column difference opposite value.
'''

from random import randint
import copy

def gen_batch(samples):
    """
    Generates a batch of samples for column differences
    """
    column_differences = []
    for x in range(0, samples):
        column_difference = [0]
        for y in range(0,9):
            column_difference.append(randint(-4,4))
        
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

def choose_column(batches):
    """
        for each batch:
            Take in an input of column differences
            Find 0s
            Check right column or left difference is 0
            Check opposite column to the one checked above.
            Choose column with the large column difference opposite value.
    """
    for batch in batches:       
        zero_locations=[]
        for column_number in range(0, len(batch)):
            if batch[column_number] == 0:
                zero_locations.append([column_number])
        for column in zero_locations:
            if column[0] < len(batch) - 1: #For all columns that are not the last
                if batch[column[0]+1] == 0: #Means value next to this cell is also 0
                    if column[0] == 0:
                        column.append(0)
                    else:
                        column.append(batch[column[0]-1])
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
        

twoD = [[0,1],[2,6],[5,-1], [7,100]]
sort_two_dimensions(twoD)
choose_column(gen_batch(20000))


        