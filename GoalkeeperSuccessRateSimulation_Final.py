"""
IS 590PR - Programming for Analytics & Data Processing
Final Project- Goalkeeper Success Rate Simulation
Authors:
Samuel John
Salonee Shah
Claire Wu
"""

from random import choice, randint
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Player:
    """
        The Player class has been created to create instances of players, both strikers and goalkeeper.
        It also has an instance of team which is a collection of player instances.
        The class has a number of functions that simulate the various aspects of a penalty kick from both the stiker's
        as well as the goalkeeper's point of view.
        The goalkeeper can be trained to use adaptive training techniques by recording strikers' kick directions
        or the team's kick direction and act accordingly
        """

    # create instances for team, keeper and team jump direction
    team = []
    keeper = None
    team_jump_dir = []

    # define an init class with the initial parameters of class objects
    def __init__(self, name=None):
        """
            This function checks if a player is a striker or keeper. 
            Strikers are added to the shooting team while a keeper is assigned the role of a Goalkeeper.
            :param:name:Name of the player either 'Player'  as Striker or 'Goalie' as goalkeeper
            :return: none
        """

        if name != 'Goalie':
            Player.team.append(self)
        else:
            Player.keeper = self
        self.name = name
        (self.wins_case1, self.wins_case2, self.wins_case3) = (0, 0, 0)
        (self.losses_case1, self.losses_case2, self.losses_case3) = (0, 0, 0)
        self.tendency = [1, 1, 1]
        self.jump_dir_history = []

    @staticmethod
    def choose_direction_goalie(team, consider_direction, striker):
        """
            This function chooses is used to select the goalkeeper's jump direction.
            The keeper's direction is chosen randomly in scenario 1, based on team tendency in scenario 2 or based on
            striker's tendency in scenario 3. 
            :param team: indicates if the team tendency is being considered, holds value of true or false
            :param consider_direction: indicates if direction is being considered, holds value of true or false
            :param striker: player who kicks the ball
            :return: jump_dir,direction: direction in which goalie should jump randomly or the direction left,right 
            or middle
            >>> np.random.seed(1)
            >>> team=True
            >>> consider_direction=True
            >>> striker='Player A'
        """

        # consider direction is false for scenario 1 and true for scenario 2 and 3
        if not consider_direction:
            # if scenario 1, select random value of right, left or middle
            directions = ['Right', 'Left', 'Middle']
            jump_dir = choice(directions)
            return jump_dir
        else:
            if team:
                # if scenario 2 check the count of all directions of entire team
                counter = Counter(Player.team_jump_dir)
            else:
                # if scenario 3 check the count of all directions for that player
                counter = Counter(striker.jump_dir_history)
            # find the most frequent direction and return that direction. If the player hasn't shot before,
            # meaning there is no frequent direction, then the goalie selects a random direction
            if counter == {}:
                directions = ['Right', 'Left', 'Middle']
                direction = choice(directions)
            else:
                max_count = max(counter.values())
                mode = [i for i, j in counter.items() if j == max_count]
                direction = choice(mode)
            return direction

    def choose_direction_striker(self, consider_direction):
        """
            Function to choose striker's direction - randomly from the list of direction when consider_direction is 
            false or based on striker's tendency when consider_direction is true
            :param self: Striker
            :param consider_direction: indicates if direction is being considered, holds value of true or false
            :return: jump_dir,left,right,middle: direction in which goalie should jump randomly
            or the direction left,right or middle
            >>> np.random.seed(1)
            >>> consider_direction=True
            >>> consider_direction=False
        """
        # consider direction is false for scenario 1 and true for scenario 2 and 3
        if not consider_direction:
            # if scenario 1, striker selects a random direction
            directions = ['Right', 'Left', 'Middle']
            jump_dir = choice(directions)
            return jump_dir
        else:
            # if scenario 2 or 3, striker selects a direction based on their tendency
            n = randint(1, sum(self.tendency))
            if n <= self.tendency[0]:
                self.tendency[0] += 1
                jump_dir = 'Right'
            elif n <= self.tendency[0] + self.tendency[1]:
                self.tendency[1] += 1
                jump_dir = 'Left'
            else:
                self.tendency[2] += 1
                jump_dir = 'Middle'

            # add player's selection to the list of last 5 shot directions for player and team
            # FIFO - pop oldest value and append latest value
            if len(Player.team_jump_dir) == 5:
                Player.team_jump_dir.pop(0)
            if len(self.jump_dir_history) == 5:
                self.jump_dir_history.pop(0)
            Player.team_jump_dir.append(jump_dir)
            self.jump_dir_history.append(jump_dir)
            return jump_dir

    @staticmethod
    def record_play(gk: 'Player', opponent: 'Player', opp_dir: str, winner: 'Player', consider_direction, team):
        """
            To record goalie's wins or losses count when the goalie jumps in random direction to save the goal
            or jumps in the team's frequent direction or striker's frequent direction
            by calculating team's tendency or striker's tendency respectively
            :param gk: Player
            :param opponent: Player
            :param opp_dir: opponent's direction
            :param winner: Player who can be either striker or a goalie
            :param consider_direction: direction of strikers either true or false
            :param team: team of strikers, true for team else false
            :return: none
        """

        # record goalies wins and losses
        if winner == gk:  # Goalie win count
            if not consider_direction:  # Scenario 1
                winner.wins_case1 += 1
            else:
                if team:  # Scenario 2
                    winner.wins_case2 += 1
                else:  # Scenario 3
                    winner.wins_case3 += 1
        else:  # Goalie loss count
            if not consider_direction:
                Player.keeper.losses_case1 += 1
            else:
                if team:
                    Player.keeper.losses_case2 += 1
                else:
                    Player.keeper.losses_case3 += 1

    def penalty_sim(self, match, striker, tests, print_result=False, team=False, consider_direction=False):
        """
            To calculate penalty simulation by considering the striker's and goalie's direction,
            when both are in same direction results in goalie's win for maximum cases else striker wins
            :param self: Goalie
            :param match: n scenarios for range in tests
            :param striker: opponent player
            :param tests: number of cases for which simulation should work
            :param print_result: prints saved or missed, it's either true or false
            :param team: team of strikers, true only for team else false
            :param consider_direction: direction of strikers, either true or false
            :return: wins_case1,wins_case2,wins_case3: Goalie's win % for case 1,case 2 or case 3
        """

        # In this function, goalie is 'self' and 'striker' is the player who is currently taking the penalty kick
        if team and match < 5:  # For scenario 2, run the code 5 times to obtain enough values to start
            striker_direction = striker.choose_direction_striker(consider_direction)
            return 0
        # goalie and striker choose directions by calling respective functions
        goalie_direction = self.choose_direction_goalie(team, consider_direction, striker)
        striker_direction = striker.choose_direction_striker(consider_direction)

        # Case 1 - goalie selects the right direction
        if goalie_direction == striker_direction:
            different = False
            # Call fail or succeed to check if goalie saved the goal
            result = fail_or_succeed(striker_direction, different)
            if result == "Miss" or result == "Save":
                winner = self
            else:
                winner = striker
        else:
            # Goalie selected the wrong direction
            different = True
            # Call fail or succeed function to check if striker missed the goal
            result = fail_or_succeed(striker_direction, different)
            if result == "Miss":
                winner = self
            else:
                winner = striker

        # Record goalie stats
        Player.record_play(self, striker, striker_direction, winner, consider_direction, team)

        # print the results of the match if print option is set to True
        if print_result:
            if result == "Miss":
                print(match, "Player", striker.name, "missed the goal entirely. The winner is the the Goalie")
            else:
                print(match, "Player", striker.name, "kicked to the ", striker_direction,
                      ", goal keeper jumped to the ", goalie_direction, ", the winner is ", winner.name)

        # Return the results as a win percentage
        if not consider_direction:
            return (self.wins_case1 / tests) * 100
        else:
            if team:
                return (self.wins_case2 / tests) * 100
            else:
                return (self.wins_case3 / tests) * 100


# outside class Player
def fail_or_succeed(strike_dir, different, n=None, sc=None, gc=None):
    """
        To check whether the goal has been saved or missed by the goalie by considering 0,1 and 2
        values based on convenience to reach
        :param strike_dir: Striker's direction either left right or middle
        :param different: different is just true or false where if both direction are same it is true
        or if both direction are different it is false
        :param n: a parameter added for doctest, passing 1 will return miss, passing anything else will run the next code
        :param sc: a parameter added for doctest in order to have a SET select_difficulty value for doctest
        :param gc: a parameter added for doctest in order to have a SET goalie_difficulty value for doctest
        :return: 'Save' or 'Goal' or 'Miss'
        >>> fail_or_succeed('Left', True, 3, 1, 1)
        'Goal'
        >>> fail_or_succeed('Left', True, 1)
        'Miss'
        >>> fail_or_succeed('Left', False, 3, 2, 2)
        'Save'
        >>> fail_or_succeed('Right', True, 3, 2, 1)
        'Goal'
        >>> fail_or_succeed('Right', False, 3, 0, 0)
        'Save'
        >>> fail_or_succeed('Middle', True, 3)
        'Goal'
        >>> fail_or_succeed('Middle', False, 3, 2, 0)
        'Goal'
    """

    # create 1 out of 10 chance for player to miss the goal entirely
    if n is None:
        n = randint(1, 10)
    if n == 1:
        return "Miss"
    # if player misses, function ends here and returns 'Miss' for both cases, goalie jumps in same/opposite direction
    # if goalie had jumped in opposite direction and player did not miss, function skips the else and returns 'Goal'
    # if goalie jumped in the same direction and player did not miss, program moves to else
    # goal has been divided into three sections, left, center, right, (Seen below) each section has subsection which
    # have been assigned difficulty values with respect to how difficult it is for the goalie to reach that subsection
    # 0 being the easiest to reach and 2 being the hardest to reach
    #   ___________________________
    #  || 2 | 1 || 1 | 1 || 1 | 2 ||
    #  || 1 | 0 || 0 | 0 || 0 | 1 ||
    #  || 1 | 0 || 0 | 0 || 0 | 1 ||

    # goal has been divided into three sections, left, center, right, (Seen below) each section has subsection which
    # have been assigned difficulty values with respect to how difficult it is for the goalie to reach that subsection
    # 0 being the easiest to reach and 2 being the hardest to reach
    #   ___________________________
    #  || 2 | 1 || 1 | 1 || 1 | 2 ||
    #  || 1 | 0 || 0 | 0 || 0 | 1 ||
    #  || 1 | 0 || 0 | 0 || 0 | 1 ||
    else:
        if not different:
            if strike_dir == "Left" or strike_dir == "Right":
                striker_difficulty = [0, 0, 1, 1, 1, 2]
                goalie_difficulty = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2]
            else:
                striker_difficulty = [0, 0, 0, 0, 1, 1]
                goalie_difficulty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

            if sc is None:
                select_difficulty = choice(striker_difficulty)
            else:
                select_difficulty = sc  # added for doc test
            if gc is None:
                goalie_choice = choice(goalie_difficulty)
            else:
                goalie_choice = gc  # added for doc test
            if select_difficulty == goalie_choice:
                return "Save"
            else:
                return "Goal"
    return "Goal"


if __name__ == '__main__':
    # define number of runs
    input_check = 1
    while input_check == 1:
        try:
            program_run = int(input("Enter the number of times to repeat the entire program: "))
            input_check = 0
        except ValueError:
            print('\nYou did not enter a valid integer')

    # define the number of tests cases per scenario
    input_check = 1
    while input_check == 1:
        try:
            tests = int(input("Enter the number of test cases per scenario (preferably a larger value > 1000): "))
            input_check = 0
        except ValueError:
            print('\nYou did not enter a valid integer')

    # define a dataframe to store overall results
    df = pd.DataFrame(columns=['Scenario 1', 'Scenario 2', 'Scenario 3'])

    for i in range(0, program_run):
        temp_result = []
        print("Beginning Run ", (i + 1))
        # SCENARIO 1: goal keeper jumps in random direction
        # step 1: create 5 striker and 1 goalie
        print("\nBeginning Scenario 1 - Goalie jumps in Random Direction")
        print("-------------------------------------------------------")
        Player(name='Player A')
        Player(name='Player B')
        Player(name='Player C')
        Player(name='Player D')
        Player(name='Player E')
        Player(name='Goalie')

        # step 2: run n scenarios where each player kicks in a random direction and goalie jumps in random direction
        for match in range(tests):
            # select a random player as kick_taker from the team and select goalie as goal_keeper
            kick_taker = choice(Player.team)
            goal_keeper = Player.keeper
            # run the program for these two players and obtain the goalie's win % as a result
            win_perc = goal_keeper.penalty_sim(match, kick_taker, tests, print_result=False, team=False,
                                               consider_direction=False)

        print("Number of penalties: ", tests, "\nGoals: ", goal_keeper.losses_case1, "\nSaves: ",
              goal_keeper.wins_case1,
              "\nGoalkeeper Success Rate: ", round(win_perc, 2), "%")
        temp_result.append(win_perc)
        print("Scenario 1 done\n\nStarting scenario 2 - Goalie jumps in Team's frequent kick direction")
        print("-------------------------------------------------------")

        # SCENARIO 2: goal keeper jumps in the direction of team's frequent shot direction
        # clear goalie's statistics from scenario 1
        (Player.keeper.wins_case1, Player.keeper.wins_case2, Player.keeper.wins_case3) = (0, 0, 0)
        (Player.keeper.losses_case1, Player.keeper.losses_case2, Player.keeper.losses_case3) = (0, 0, 0)
        (Player.keeper.count_r_total, Player.keeper.count_l_total, Player.keeper.count_m_total) = (0, 0, 0)
        for match in range(tests):
            kick_taker = choice(Player.team)
            goal_keeper = Player.keeper
            # run 5 tests to obtain enough data to start comparisons
            if match < 5:
                train = goal_keeper.penalty_sim(match, kick_taker, tests, print_result=False, team=True,
                                                consider_direction=True)
            else:
                # run scenario for team stats and obtain goalie's win % as result
                win_perc = goal_keeper.penalty_sim(match, kick_taker, tests, print_result=False, team=True,
                                                   consider_direction=True)
        print("Number of penalties: ", tests, "\nGoals: ", goal_keeper.losses_case2, "\nSaves: ",
              goal_keeper.wins_case2,
              "\nGoalkeeper Success Rate: ", round(win_perc, 2), "%")
        temp_result.append(win_perc)
        print("Scenario 2 done\n\nStarting scenario 3 - Goalie jumps in Player's frequent kick direction")
        print("-------------------------------------------------------")

        # SCENARIO 3: goal keeper jumps in the direction the individual players' frequent shot direction
        # clear goalie stats from scenario 2
        (Player.keeper.wins_case1, Player.keeper.wins_case2, Player.keeper.wins_case3) = (0, 0, 0)
        (Player.keeper.losses_case1, Player.keeper.losses_case2, Player.keeper.losses_case3) = (0, 0, 0)
        (Player.keeper.count_r_total, Player.keeper.count_l_total, Player.keeper.count_m_total) = (0, 0, 0)
        for match in range(tests):
            kick_taker = choice(Player.team)
            goal_keeper = Player.keeper
            # run program for player stats and obtain goalie's win % as result
            win_perc = goal_keeper.penalty_sim(match, kick_taker, tests, print_result=False, team=False,
                                               consider_direction=True)
        print("Number of penalties: ", tests, "\nGoals: ", goal_keeper.losses_case3, "\nSaves: ",
              goal_keeper.wins_case3,
              "\nGoalkeeper Success Rate: ", round(win_perc, 2), "%")
        temp_result.append(win_perc)
        print("Scenario 3 done")
        print("-------------------------------------------------------\n\n")
        # append values from all 3 scenarios to the dataframe
        df = df.append(pd.Series(temp_result, index=df.columns), ignore_index=True)
    df.loc['Average'] = df.iloc[[x for x in range(0, len(df.axes[0]) - 1)]].mean()  # find average of all runs
    df = df.round(2)

    print(df)

    # Output observations from the tests run above
    print("\n\n***** Results *****\n")
    print("Observation 1:\nIn Case 1 where the goalie and player both chose random directions, the goalie saved ",
          df.loc['Average']['Scenario 1'], "% of the goals, on average.")
    print(
        "Observation 2:\nIn Case 2 where the goalie selected direction based on team's past 5 kicks and players choose "
        "direction based on their individual tendency, the goalie saved ",
        df.loc['Average']['Scenario 2'], "% of the goals, on average.\n\nConclusion 1: ")
    diff_1and2 = df.loc['Average']['Scenario 2'] - df.loc['Average']['Scenario 1']
    if diff_1and2 == 0:  # no difference in results of scenario 1 and 2
        print(
            "There is no change in win % if the goalie knows the team's last 5 directions compared to the goalie "
            "choosing random directions.")
    elif diff_1and2 > 0:  # increase in win % for scenario 2
        print("There is an increase of ", format(diff_1and2, '.2f'),
              "% if the goalie knows the team's last 5 directions compared to the goalie choosing random directions.")
    else:  # decrease in win % for scenario 2
        print("There is an decrease of ", format(diff_1and2, '.2f'),
              "% if the goalie knows the team's last 5 directions compared to the goalie choosing random directions.")

    print(
        "\nObservation 3:\nIn Case 3 where the goalie selected direction based on player's past 5 kicks and players "
        "choose direction based on their individual tendency, the goalie saved ",
        df.loc['Average']['Scenario 3'], "% of the goals, on average.\n\nConclusion 2:")
    diff_1and3 = df.loc['Average']['Scenario 3'] - df.loc['Average']['Scenario 1']
    if diff_1and3 == 0:  # no difference in results of scenario 1 and 3
        print(
            "There is no change in win % if the goalie knows the player's last 5 directions compared to the goalie "
            "choosing random directions.")
    elif diff_1and3 > 0:  # increase in win % for scenario 3
        print("There is an increase of ", format(diff_1and3, '.2f'),
              "% if the goalie knows the player's last 5 directions compared to the goalie choosing random directions.")
    else:  # decrease in win % for scenario 3
        print("There is an decrease of ", format(diff_1and3, '.2f'),
              "% if the goalie knows the player's last 5 directions compared to the goalie choosing random directions.")

    # convert the data from dataframe in to a graph that shows the results of each run and the average across all runs
    plt.rcParams["figure.figsize"] = 18, 13
    df.index = np.arange(1, len(df) + 1)
    as_list = df.index.tolist()
    as_list[-1] = 'Average'
    df.index = as_list
    ax = df.plot.bar(rot=0)
    plt.xlabel('Scenarios per Run and Average of Each Scenario over All Runs')
    plt.ylabel('Win percentage of a Goalie')
    plt.title("Plot of Goalie's win % over the 3 scenarios for each run")
    print("\nA graph of the above observations is displayed in a separate window\nClose the Graph to end the program.")
    plt.show()
