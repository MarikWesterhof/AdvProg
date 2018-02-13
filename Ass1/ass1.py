# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:40:35 2018

@author: Marik
"""

# Import the necessary modules for CSV, shuffling, and unit testing.
import csv
import random
import unittest
import os

# Main function that uses four inputs:
# - # of Assignments                    ass
# - # students per group                spg
# - Name of input file                  inp
# - Name of output file                 out
def groupify(ass, spg, inp, out):
    
    # Read the given CSV file name and turn it into a student info list.
    with open(inp, 'r') as f:
        reader = csv.reader(f)
        studentinfo = list(reader)
    # Skim all info but people's first names
    students = [s[0] for s in studentinfo]
    
    # Raise exception if given group size is too big or small
    if spg > len(students):
        raise Exception('Group size given exceeds amount of students.')
    elif spg < 1:
        raise Exception('Group size has to be at least one.')
    
    # This will be the list that the reader will turn into a CSV file.
    # As such, we have to format it properly in the following loop.
    groups = []

    # This loop creates the groups. It repeats for every assignment time.
    for i in range(ass):
        # Shuffle the list of students for each iteration
        random.shuffle(students)
        # Make lists depending on group size
        a = ([students[i:i + spg] for i in range(0, len(students), spg)])
        
        # Group size difference can't be more than one. If so:
        if len(a[-1]) < (len(a[0])-1):
            # Raise exception if group sizedifference is > 1
            if len(a[-1]) > len(a[:-1]):
                raise Exception('Group size difference would too big')
            # Take the 'leftover list' and divide it over the others
            a, b = a[:-1], a[-1]
            for i in range(len(b)):
                a[i].append(b[i])
                
        # Formatting the lists so that they will be properly done in CSV
        # Firstly, a line for "Assignment #"
        groups.append(['Assignment ' + str(i + 1)])
        # Secondly, a loop that writes the groups out for each assignment
        for i in range(len(a)):
            groups.append(a[i])
        # Thirdly, a blank line between assignments for tidiness
        groups.append('\n')
    
        # Write the now completed groups list to the given csv
        with open(out, 'w', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(groups)
        
    # Return the set. Not used for the CSV, but only for unittesting.
    # 'a' is the unformatted list, while 'groups' is formatted for CSV.
    return(a)
 
# Unittests. Writes to att.csv as to not overwrite the normal one
class TestPM(unittest.TestCase):
    def setUp(self):
        pass
    # Splitting up the group of 23 into groups of 5 should return
    # four groups of length [6, 6, 6, 5]: this is tested as such.
    def test_group_amount(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')),4)
    def test_group1_length(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[0]),6)
    def test_group2_length(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[1]),6)
    def test_group3_length(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[2]),6)
    def test_group4_length(self):
        self.assertEqual(len(groupify(1,5,'students.csv','att.csv')[3]),5)
    # Test Exception for when the group size is too high or low.
    def test_group_size_too_high(self):
        self.assertRaises(Exception,groupify,2,24,'students.csv','att.csv')
    def test_group_size_too_low(self):
        self.assertRaises(Exception,groupify,2,0,'students.csv','att.csv')
    # Test Exception for when the group size difference is > 1
    def test_group_size_too_different(self):
        self.assertRaises(Exception,groupify,3,9,'students.csv','att.csv')

if __name__ == '__main__':
    unittest.main()
 
# Clean up the CSV file used for testing afterwards.
os.remove('att.csv')