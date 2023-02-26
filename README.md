# AI-pacman-with-ghosts
In this project, you will design an agent for the classic Pacman game, which this time also includes ghosts. In this way, we used minimax search and possible minimax and designed an evaluation function. <br>
The structure of this project has not changed much compared to the previous project. <br>
You can check the previous project at https://github.com/BornFromAshes/AI-pacman <br>
Similar to the previous project, you can run the following command to debug and test the correctness of the algorithms:
```
python autograder.py
```
By default, running autograder.py with the -t option will include the graphic display, but the =q option is without the graphic display. You can use the --graphics flag to force graphics execution, and --no-graphics to force no graphics display.
## Project Structure
- multiAgents.py : It includes all multi-factor search factors.
- pacman.py : The main file that runs Pacman games. This file describes the GameState class for the Pacman game that you use in this project.
- game.py : The implemented logic for the Pacman world is in this file. This file contains several classes such as AgentState, Agent, Grid, and Direction.
- util.py : Useful data structures for implementing search algorithms are located in this file.
- graphicsDisplay.py : Graphics implemented for Pacman game.
- graphicsUtils.py : Support for game graphics.
- textDisplay : ASCII graphics for Pacman.
- ghostAgent.py : Ghost controller.
- keyboardAgents.py : Keyboard interface to control Pacman.
- layout.py : Program to read map files and save their information.
- autograder.py : Project auto corrector.
- testParser.py : Parse autocorrect tests and solution files.
- testClasses.py : General automatic test classes.
- testCases/ : Folder containing different tests for each question.
- searchTestClasses.py : Automated testing classes.
## Welcome to Pacman MultiAgent!
You can run the Pacman game by typing the following commands:
```
python pacman.py
```
Now select ReflexAgent from the multiAgents.py file as the game agent:
```
python pacman.py -p ReflexAgent
```
You will see that the agent is not playing well. Even on simple terrains:
```
python pacman.py -p ReflexAgent -l testClassic
```
## ReflexAgent
We changed the evaluationFunction function in such a way that the evaluation is done based on the results of the action (action) and the secondary state (state) and not the obtained state alone. In this regard, there are methods at the beginning of evaluationFunction that extract important information such as the new position (newPos) (Pacman) or the state of food after the action (newFood) from GameState. Finally, ReflexAgent should take into account the position of food and ghosts, make the best choice and always win in testClassic map. To check this issue, you can use the following command:
```
python pacman.py -p ReflexAgent -l testClassic
```
To test the agent on the mediumClassic map with one or two ghosts and run the game at high speed, use the following commands:
```
python pacman.py --frameTime 0 -p ReflexAgent -k 1
```
```
python pacman.py --frameTime 0 -p ReflexAgent -k 2
```
## Minimax
The agent must work correctly for any number of ghosts, for this you must have one min layer per ghost and only one max layer per Pacman.
The minimax tree should be expanded to the desired depth and its leaves should be evaluated with the appropriate function. For this purpose, MinimaxAgent class inherits from MultiAgentSearchAgent, which contains self.evaluationFunction and self.depth, and they must be used for desired depth and leaves evaluation in MinimaxAgent. This evaluation function is by default scoreEvaluationFunction, which you can see in the same multiAgents.py file.
You can use the following command to test the agent:
```
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
```
## Alpha-beta pruning
We have improved minimax tree traversal by adding alpha-beta pruning. For this, we completed the AlphaBetaAgent class. Note that we will still have several min layers (per ghost) and one max layer (per Pacman). <br>
As a result of this upgrade, we see an increase in speed. You can check this issue by running the following command in depth 3 and comparing it with MinimaxAgent agent in depth 2. Both should be completed at about the same time.
```
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```
Minimax values in AlphaBetaAgent are exactly the same as MinimaxAgent values because both will use the same evaluation function. But the values chosen may be different in alpha-beta pruning due to boundary conditions.
![image](https://user-images.githubusercontent.com/117355603/221408039-7b9df6d9-424b-4b5a-9d38-fab2a12e2856.png)
## Expectiminimax
In minimax and alpha-beta pruning, it is assumed that the opponent makes the most optimal choices, while in reality this is not the case, and the possible modeling of the agent's behavior that may have non-optimal choices can have a better result. Random ghosts also do not have optimal choices, so their modeling by minimax search may not have optimal results. The expectiminimax method, instead of considering the smallest moves of the opponent, considers a model of the probability of moves. To simplify your probabilistic model, suppose that the spirits choose their movements from among their 4 allowed movements uniformly and randomly.
You can use the following command to see the performance of the agent
```
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```
As mentioned in the above, when Pacman comes to the conclusion that his death is inevitable, he tries to lose early in order to avoid losing points. But in this particular case, if he tries to escape to eat some more pieces of food, the game may continue.
## Evaluation function
We created a better evaluation function for Pacman in betterEvaluationFunction. This evaluation function should evaluate the states instead of the action. The evaluation function should complete the smallClassic scenario with a random ghost in half the time and win in search of depth 2.
## Known Issues
There aren't currently any issues so far so if you find any please create an issue on this repository. Any suggestions for implementation would also be greatly appreciated.










