import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generator.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        """
        for var in self.domains:
            self.domains[var] = {
                word for word in self.domains[var] 
                if len(word) == var.length
            }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        Return True if a revision was made to the domain of `x`.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        
        i, j = overlap
        to_remove = set()
        
        for x_word in self.domains[x]:
            # Check if there exists a y_word that satisfies the constraint
            if not any(
                y_word[j] == x_word[i]
                for y_word in self.domains[y]
                if i < len(x_word) and j < len(y_word)
            ):
                to_remove.add(x_word)
        
        if to_remove:
            self.domains[x] -= to_remove
            revised = True
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        """
        if arcs is None:
            arcs = [
                (x, y) 
                for x in self.crossword.variables 
                for y in self.crossword.neighbors(x)
            ]
        
        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete.
        """
        return all(var in assignment for var in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent.
        """
        # Check all values are distinct
        if len(set(assignment.values())) != len(assignment.values()):
            return False
            
        for var, word in assignment.items():
            # Check length matches
            if len(word) != var.length:
                return False
                
            # Check overlaps with neighbors
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if (i >= len(word) or 
                        j >= len(assignment[neighbor]) or 
                        word[i] != assignment[neighbor][j]):
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return values ordered by least constraining value heuristic.
        """
        def count_conflicts(value):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                i, j = self.crossword.overlaps[var, neighbor]
                if not any(
                    value[i] == word[j]
                    for word in self.domains[neighbor]
                    if i < len(value) and j < len(word)
                ):
                    count += 1
            return count
        
        return sorted(
            self.domains[var],
            key=lambda value: count_conflicts(value)
        )

    def select_unassigned_variable(self, assignment):
        """
        Select unassigned variable using MRV and degree heuristics.
        """
        unassigned = [
            var for var in self.crossword.variables 
            if var not in assignment
        ]
        return min(
            unassigned,
            key=lambda var: (
                len(self.domains[var]),
                -len(self.crossword.neighbors(var))
            )
        )

    def backtrack(self, assignment):
        """
        Backtracking search to find a complete assignment.
        """
        if self.assignment_complete(assignment):
            return assignment
            
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
            
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()