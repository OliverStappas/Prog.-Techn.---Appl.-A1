"""
Oliver Stappas, 1730124
Tuesday, February 5
R. Vincent, instructor
Assignment 1
"""

class stack(list):
    '''A very simple stack class derived from a Python list.'''
    def isEmpty(self):
        '''return True if the stack is empty.'''
        return self == []

    def push(self, value):
        '''Add a value to the stack.'''
        self.append(value)

    def top(self):
        '''Check the top of the stack, without changing the stack.'''
        if self.isEmpty():
            raise ValueError("Stack underflow")
        return self[-1]

    def pop(self):
        '''Remove the top of the stack, returing the value found there.'''
        if self.isEmpty():
            raise ValueError("Stack underflow")
        return super().pop()

def main(): # Create a function to run all the code so I can use return
    file = input("Please input a file name: ") # Asks the user to input a file name, then make that file name equal to file
    fp = open(file) # Open the file
    line = fp.readline() # Reads the line in the file
    s = stack() # Creates an initially empty stack 
    line_nbr = 1 # The number of the line that is being analyzed. This will increase later in the while loop
    left_right_map = {'[':']', '{':'}', '(':')'} # Makes a dictionary with left brackets, curly braces and parentheses as they keys and the right equivalent of the these characters as the values
    while line: # While there is a line of text to analyze
        for char in line: # For every character (string) in each line
            if char in left_right_map: # If the character is a key in the left_right_map dictionary
                s.push(char) # Appends that character to s
            elif char in left_right_map.values(): # If the character is a value in the left_right_map dictionary
                if s.isEmpty(): # If the stack list is empty
                    print("Extra brackets at line {}.".format(line_nbr)) # Prints the extra brackets error with the line number of the error
                    return # Stops running
                left_char = s.pop() # Removes the last value from the stack list and makes a variable equal to it
                if left_right_map[left_char] != char: # If the value (right parentheses, braces, brackets) of the left_right_map dictionary associated with the popped value is not equal to the next character
                    print("Mismatched brackets at line {}.".format(line_nbr)) # Prints the mismatched brackets error with the line number of the error
                    return # Stops running  
        line_nbr += 1 # Increases by 1 the number of the line that is being analyzed
        line = fp.readline() # Continues reading the file lines
    if not s.isEmpty(): # If the stack list is not empty
        print("Unclosed (missing) brackets at line {}.".format(line_nbr)) # Prints the unclosed (missing) brackets error with the line number of the rror
    else: # If there were no errors
        print("All checks have passed.") # Prints that there were no mistakes
    fp.close() # Closes the file

main() # Call the function to run the file
                
            
            
            
        
