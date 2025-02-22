# Elevator simulator
Have you ever wondered how much longer you have to wait for an elevator when one of them stops working? The high rise that I am in currently has that issue constantly – one of the two elevators seems to often be broken, and I feel like I have to wait so much longer. I set out to create a very simple command line-based simulator to measure elevator wait times. <br/>
## How it works
I want to add that I am NOT a data scientist, so please forgive my crude estimation methods. I made the following assumptions: <br/>
<ul>
  <li>Elevators start at ground floor, but start at slightly offset times</li>
  <li>Elevators go up all the way, then down all the way
  <li>Passengers are placed randomly on floors, five initially and then more at a preset time interval</li>
  <li>Each passenger gets on when the elevator is going in the direction of their destination (not the opposite)</li>
  <li>Each passenger takes between 1 and 2 seconds to get on and off the elevator</li>
  <li>The wait time is measured from when the person instance is created to when they off-board at their destination and is recorded to the spreadsheet elevator_sim_[current time].csv (located in the directory program was run from)</li>
</ul>

## User-set values
There are a few values that are set when the program is run:<br/>
<ul>
  <li><b>elevators:</b> this is the number of elevators running at once (default: 2 elevators)</li>
  <li><b>floors:</b> the number of floors in the building (default: 10 floors)</li>
  <li><b>people_interval:</b> the number of seconds between people being placed on floors (default: 1 person added every 15 seconds)</li>
  <li><b>elevator_speed:</b> the number of seconds it takes each elevator to get from one floor to the next (default: 1 floor every 3 seconds)</li>
  <li><b>trips:</b> prevents script from infinitely looping (note that you cannot stop the program running until all trips are complete) (default: 5 trips)</li>
</ul>

## Dependencies
This program requires the <b>pandas</b> module to display the “elevators” in a table format.

## Example output
![image](https://github.com/user-attachments/assets/83bc2a13-c7bb-4378-9fab-af3c9210e045)
