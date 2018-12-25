# IS590PR Final_Project

# Title: Goalkeeper Success Rate Simulation

## Team Member(s): Claire Wu | Salonee Shah | Samuel John

# Monte Carlo Simulation Scenario & Purpose:
The program would simulate the success percentage of a goalkeeper and the purpose would be checking if using different strategies can improve the success percentage or not.  

The simulation conditions we are considering are: 

• The Goalkeeper jumps in a random direction for each opponent over a set number of runs 

•	The Goalkeeper jumps in the direction of the opponent team's most frequent kick direction for a set number of runs

•	The Goalkeeper jumps in the direction of each striker's most frequently kick direction for a set number of runs

Assumptions we are using are as follows:

•	The Goalkeeper is positioned at the center of the goal line, at the start of each penalty

•	There are three main directions which both the goalkeeper and striker can choose from - Left, Middle, Right, which correspond to the region of the goal in which the ball is headed and not each individual's bearing. 
This means that if the Striker chooses Left and the Goalkeeper also chooses Left, they have both selected the same region of the goal and their choices match.

•	Since the goalkeeper cannot reach every part of the goal with the same level of ease (eg. it would be harder to save a goal in the top corner than it is to save a goal in the center), we have divided the whole goal area into 3 regions, Left, Middle and Right and each region is further divided into 6 sectors that are assigned a difficulty value that ranges from 0 to 2, 0 being the easiest sector to reach and 2 being the hardest sector to reach

• The Goalkeeper saves the goal only if he selects the right direction and sub-sector as that of the Striker. All other cases count as a goal, apart from cases in which the striker misses the goal entirely (which we have assumed is a 1 out of 10 chance).

•	The Striker’s kicking direction will not change based on the Goalkeeper's behavior. It will be based solely on the Striker's tendency over his past kicks (Exception to this rule - Scenario 1 where the direction selection is random).

## Simulation's variables of uncertainty
Variable 1：Striker's kick direction (striker_direction)
The Striker's kick direction is completely random for the first scenario and thereafter is selected based on the Striker's tendency ontained from the initial scenario. 
The range of this variable is limited to three values, Left, Middle and Right.

Variable 2: Goalkeeper's jump direction (goalie_direction)
The Goalkeeper's jump direction is completely random in the first scenario, selected based on the Team's frequently chosen direction in the second scenario and selected based on each Striker's individual tendency in the third scenario. 
The range of this variable is limited to three values, Left, Middle and Right.  

Variable 3: Striker's kick sector (striker_difficulty)
The area of the goal that the Striker chooses is based off of a random selection of a sector within the direction selected based on the Striker's tendency. 
The values of this variable are either 0, 1, 2 or Miss. 
This variable helps account for Striker's error which is seen in reality, which means that the Striker misses the goal entirely, irrespective of the direction of the kick.

Variable 4: Goalkeeper's jump sector (goalie_difficulty)
The area of the goal that the Striker chooses is based off of a random selection of a sector within the direction selected based on the Striker's tendency. 
Like the striker_difficulty, this variable has a value of 0, 1 or 2 but not a 'Miss' value. Instead, the Goalkeepers probability of selecting a value is altered by selecting this value from a list of values in which the easier sectors 0 and 1 appear more number of times than the harder sectors 2 in the ratio of 3:2:1 for 0,1 and 2 respectively. 
This variable helps account for Goalkeeper error which is seen in reality.

The Goalie's saving difficulty and the Striker's kicking area is as below: 
![Alt text](http://funkyimg.com/i/2Pcoj.png)

Variable 5: Goalkeeper's win percentage
This is the most important variable of this program. It indicates what percentage of the goals the Goalkeeper was able to save, using the hypothesis for each scenario. 
The value of this variable is a percentage represented as a float. 
The reality of this variable is determined by the results obtained while running the program.

## Hypothesis or hypotheses before running the simulation:
- Recording the team’s most frequent kick direction and then reacting accordingly can help in increasing the Goalkeeper's success rate when compared to that obtained by the Goalkeeper jumping in a random direction.

- Recording each striker’s most frequent kick direction, can help increase the Goalkeeper's success rate when compared to that obtained by the Goalkeeper jumping in a random direction or the direction of a team's most frequent kick direction.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
Our initial decision was to add a scenario where the Goalkeeper would select a direction based on the Striker's dominant foot.
We did create the logic for this case; however, we were able to find only one dataset online that contained this data and the data was very limited. On further research, we learned that this variable would not have an adverse effect on the win percentage. Thus, we added the team's frequent kick direction to our program instead. 

Secondly, in the earlier versions of our code, we did not consider the probability of the Striker completely missing the goal or the fact that the Goalkeeper could miss the save even if he jumped in the right direction. This caused our results to vary. Thus, we added a 1 out of 10 chance that the striker may miss the goal completely and created sub-regions within the goal area that added a difficulty aspect to the Goalkeeper's jump selection decision.
 
Based on a number of sample tests with runs of counts ranging from 1 to 20, where each scenario was run between 5000 and 100000 times, we have the following findings:

Conclusion 1: 
There is a minimal increase in the success percentage of the goalie while considering the team's last 5 directions compared to the goalie choosing random directions. This is due to the fact that a Striker considers his/her own tendency while choosing a direction to shoot in and not the team's tendency. In fact, the success percentage goes down if the strikers' tendency does not match the team tendency. 
eg., striker A could have a tendency to shoot towards the Left while the team tendency is to shoot to the Right, causing the Goalkeeper's win percentage to decrease. 
Hence, we concluded that the success percentage of this Scenario is totally dependent on how well each striker's tendency mirros that of the team.

Conclusion 2:
There is a noticeable increase in the success percentage of the Goalkeeper when he/she knows the Striker's most frequently chosen direction as compared to the win percentage when the Goalkeeper chooses random directions. This is because there is a direct correlation between the Striker selecting their shots based on their own tendency and the most frequent direction, unlike what was seen in scenario 2.

## Instructions on how to use the program:
1. Please download the code GoalkeeperSuccessRateSimulation_Final.py
2. Install Pandas, Random and Matplotlib libraries before running the code if not installed
3. Run the code and enter the number of times to repeat the entire program
4. Then enter the number of test cases per scenario (preferably a larger value > 1000)
5. View and close the graph to end the program

## Member Contributions
### Initial algorithm and code structure:
Early ideas and program structure decided by all three team members in initial few meetings and subsequent changes were discussed in further meetings.

### Code and documentation:
#### Claire
Worked on coding for Scenarios 2 and 3 as well as all functions involved, doctests, visual representation of output and readme. 
#### Salonee
Worked on coding for Scenarios 1, 2 and 3 as well as all functions involved, docstrings, doctests, visual representation of output and doctests.
#### Samuel
Worked on coding for Scenarios 1, 2 and 3 as well as all functions involved, code debugging and restructuring of overall program, dataframes, docstrings, comments, readme.

### Method of work:
Each member of the team would pick up a part of the code, complete it and hand it over to another member of the team for review, then upload it to git, after which the code would be combined by one member and tested by each member.

All three members contributed equally to all stages of the assignment.

## All Sources Used:
1. https://en.wikipedia.org/wiki/Penalty_shot
2. Refered 'Simulation of a multi-player tournament of Rock, Paper, Scissors' - J. Weible
