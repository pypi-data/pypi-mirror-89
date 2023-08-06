# Zoom Meet Attendance Visualizer
#### About
This module is to help to visualize your meeting attendance helper data created using 
<a href="https://github.com/mahbd/zoom_meet_attendance">zoom_meet_attendance</a>. You 
don't have to repeat anything except selecting data file. It will remember everything
in config.json.
#### Installation
`pip install zoom-meet-attendance-visualizer`
### How to use
<ol>
<li>Write this code, and you're ready to go. <br>
<pre>from zoom_meet_attendance_helper.main import run_attendance_helper

run_attendance_helper()
</pre>
</li>
<li>When you run this code it will ask you to select the text file created by 
<a href="https://github.com/mahbd/zoom_meet_attendance">zoom_meet_attendance</a>.
</li>
<li>Then it will ask **class**. Class will be used to avoid repetition. In class all attendee 
name will be saved to show who is absent. Also, if rename any name, it will remember it and
if you reuse the same class it will automatically suggest renaming.
</li>
<li>Then it will ask if you want to rename any name. If you want to rename then type a new name,
otherwise pre Enter without typing anything.
</li>
<li>
Then it will show all the names and ask you if you want to add more name. If you want to 
add then type else type Exit to show you the graph.
</li>
<li>
If you made any mistake you can manually edit config.json file automatically created on
the same directory.
</li>
</ol>