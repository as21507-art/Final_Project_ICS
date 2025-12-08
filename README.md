# Final_Project_ICS
**Setting up the application** <br>
The folder main contains six Python files: **tank, bar, bullet, intro, globals, and game**. It also includes a 
processing file in Python mode: **main.pyde**, which is the main program that should be executed. The 
main program makes reference to the six Python modules during execution. This helps in the 
decomposition of the problem and makes it easy to work on a particular feature of the game. It also 
contains four folders: **tank images, images, sounds,** and **data** (stores fonts). To run the game, make sure 
that the “minim” library is installed. If any error occurs, please save and run again to see if the issue is 
resolved. <br><br>
**Intro Screen** <br>
● The play button (text is highlighted when hovered) starts the game. <br>
● The tutorial button displays a pop-up of instructions on how to play the game (this contains 6 
slides). <br>
● The mute/unmute button mutes/unmutes the background music only.  <br>
● The quit button can be used to exit the game <br>
● Below, there are spaces to change the names of the players (default is player 1 and player 2). And 
it allows a maximum of 12 characters. The name can be entered by clicking on the box (after 
which it will be highlighted) and typing. <br><br>
**The Main Game** <br>
● The game will display the following: background, tanks, and player names with health bars. <br>
● The turn of the player will be displayed on the screen until the user interacts with the device.<br> 
● Player 1 can move using the A and D keys, and change angle using the S key. <br>
● Player 2 can move using the Left and Right arrow keys and change angle using the Down arrow 
key. <br>
● While changing the angle, the player can not move; if they wish to move, they can press S again. <br>
● To shoot the bullet, click and hold on the screen while the nozzle is in motion, and drag it. <br>
● The power bar will be displayed while dragging, indicating the velocity. <br>
● The bullet is shot when the mouse is released (however, there is a minimum limit to drag, so a 
player must drag at least 60 pixels for it to be considered a drag. Otherwise, the player will be 
considered not to have made the selection, and the tank will continue changing angle. <br>
● After the bullet is shot, the effect on the opponent’s health will be displayed on the health bar. 
● The players change turns as indicated by the prompt before each player’s turn. <br>
● The game ends when one player wins, and the other player has zero health. <br><br>
**Pause** <br>
● The game can be paused by pressing “P” and resumed by clicking on the Resume button. <br>
● It also has features like a tutorial and a mute button, like the intro screen. <br>
● It has a “Main menu” option, which ends the game without any results and takes the users to the 
intro screen. <br><br>
**Outro Screen** <br>
● This part displays the winner and an instruction to return to the intro screen. The game can be 
exited from the intro screen if required. <br><br>
**Sources for graphics, sounds, and fonts** <br>
Image of tank: “Panther Ausf. D 1943 (Side View)” by ThunderFenrirson <br>
Source:https://www.furaffinity.net/view/44398781/ (Fur Affinity) <br>
Image of play button: “blank button. blank square 3d push button” by Aquir <br>
Source:https://as2.ftcdn.net/v2/jpg/03/63/54/57/1000_F_363545787_JnnT3ce8qxmeACf0ZIa7P58i6uRgb1mk.jpg (Adobe Stock) <br>
Image of tutorial and quit button: "A glossy yellow button with rounded corners isolated on white background, ideal for websites, 
apps, and graphic design projects needing a vibrant touch" by Wasif - Studio <br>
Source:https://as1.ftcdn.net/v2/jpg/17/66/69/20/1000_F_1766692023_M5FpSXpxJU9Cz66B5pVIiQpGiGx6GOLr.jpg (Adobe 
Stock) <br>
Image of mute button: “Glossy yellow button” by vuang <br>
Source:https://as2.ftcdn.net/v2/jpg/10/39/19/59/1000_F_1039195978_4PCetXy4aUuLe8EwpvSpRRPL1GlKY08J.webp (Adobe 
Stock) <br>
Image for the speaker icon: “Audio speaker volume on line art icon for apps and websites” by martialred <br>
Source:https://t4.ftcdn.net/jpg/01/11/83/19/240_F_111831968_vCgI1K6RSfB6x5EpKfRe6CweyY9JS7BD.jpg (Adobe Stock) <br>
Patterned backgrounds, purple and blue: Made using Chat GPT  <br>
Game logo: Made using ChatGPT <br>
Source:https://chatgpt.com/ <br>
Other graphics: Made via Canva’s templates and elements features <br>
Source:https://www.canva.com/templates <br>
Shooting noise: “Nuclear Explosion” by DRAGON-STUDIO <br>
Source:https://pixabay.com/sound-effects/search/nuclear%20explosion%20sound/ (Pixabay) <br>
Background music: “Victory Awaits in the Gaming Universe_Astronaut” by Astronaut12  <br>
Source:https://pixabay.com/music/rock-victory-awaits-in-the-gaming-universe-astronaut-265184/ 
(Pixabay) <br>
Game Font: “Press+Start+2P font” by Google fonts 
Source:https://fonts.google.com/specimen/Press+Start+2P
