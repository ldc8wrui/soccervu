# SoccerVu Data Analysis

## Soccer Player Movements

This is a visualization demo soccer game from raw SportVU data: *RawPauseResumeWithGameTimeIndicator.txt*
The profile of the data:
* 300 records totally, containing a game fragment with *12 secs*.
* Contains the position of the ball and the players of home/visitor team at each *0.04ms*.

### 3rd party dependency
* [imagemagick](http://macappstore.org/imagemagick)
* [ffmpeg](https://trac.ffmpeg.org/wiki/CompilationGuide/MacOSX)

### [python requirements](https://github.ibm.com/ruiwcdl/soccervu/blob/master/requirements.txt)

### command
> python Main.py --path=football_player_header.json --event=0

### visualization 
![](https://github.com/ruiwcdl/soccervu/blob/master/soccer_small.gif)

### visualization with full back player's convex hull of movements
![](https://github.com/ruiwcdl/soccervu/blob/master/soccer-convexhull.gif)
