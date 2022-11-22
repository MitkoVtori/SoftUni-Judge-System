from judge.softuni_judge.public_source.output import output # from here, I get the expected output for every problem
import GivenInput # this imports a hidden file, that has all input checks for the current Problems
import restart # imports a hidden file, that avoid problems and retry the code 10 times.
import Test # imports a hidden file, that tests the code with the given input.
from UserCode import executed_code as code # from a hidden file that executes the user code, we import just the executed version and use it for the test
import code_problem_number as currProblem # Checks for which problem the code is


class Problems:

    def __init__(self):
        self.score = 0

    def first_problem(self, given_output):
        expected_output = output.first_problem()
        if given_output == expected_output:
            self.score += 10

    def second_problem(self, given_output):
        expected_output = output.second_problem()
        if given_output == expected_output:
            self.score += 10

    def third_problem(self, given_output):
        expected_output = output.third_problem()
        if given_output == expected_output:
            self.score += 10

    def fourth_problem(self, given_output):
        expected_output = output.fourth_problem()
        if given_output == expected_output:
            self.score += 10

    def fifth_problem(self, given_output):
        expected_output = output.fifth_problem()
        if given_output == expected_output:
            self.score += 10

    def sixth_problem(self, given_output):
        expected_output = output.sixth_problem()
        if given_output == expected_output:
            self.score += 10

    def seventh_problem(self, given_output):
        expected_output = output.seventh_problem()
        if given_output == expected_output:
            self.score += 10

    def eight_problem(self, given_output):
        expected_output = output.eight_problem()
        if given_output == expected_output:
            self.score += 10

    def ninth_problem(self, given_output):
        expected_output = output.ninth_problem()
        if given_output == expected_output:
            self.score += 10

    def tenth_problem(self, given_output):
        expected_output = output.tenth_problem()
        if given_output == expected_output:
            self.score += 10

    def show_result(self):
        return self.score


problems = Problems()

for check in range(10):
    
    if currProblem.check() == 1:
        given_input = GivenInput.problem1()
        curr_output = Test.first_check(code, given_input)
        problems.first_problem(curr_output)

    elif currProblem.check() == 2:
        given_input = GivenInput.problem2()
        curr_output = Test.second_check(code, given_input)
        problems.second_problem(curr_output)

    elif currProblem.check() == 3:
        given_input = GivenInput.problem3()
        curr_output = Test.third_check(code, given_input)
        problems.third_problem(curr_output)

    elif currProblem.check() == 4:
        given_input = GivenInput.problem4()
        curr_output = Test.fourth_check(code, given_input)
        problems.fourth_problem(curr_output)

    elif currProblem.check() == 5:
        given_input = GivenInput.problem5()
        curr_output = Test.fifth_check(code, given_input)
        problems.fifth_problem(curr_output)

    elif currProblem.check() == 6:
        given_input = GivenInput.problem6()
        curr_output = Test.sixth_check(code, given_input)
        problems.sixth_problem(curr_output)

    elif currProblem.check() == 7:
        given_input = GivenInput.problem7()
        curr_output = Test.seventh_check(code, given_input)
        problems.seventh_problem(curr_output)

    elif currProblem.check() == 8:
        given_input = GivenInput.problem8()
        curr_output = Test.eight_check(code, given_input)
        problems.eight_problem(curr_output)

    elif currProblem.check() == 9:
        given_input = GivenInput.problem9()
        curr_output = Test.ninth_check(code, given_input)
        problems.ninth_problem(curr_output)

    elif currProblem.check() == 10:
        given_input = GivenInput.problem10()
        curr_output = Test.tenth_check(code, given_input)
        problems.tenth_problem(curr_output)

    else:
        print("*", end='')
        restart.refresh()
    
print(problems.show_result())