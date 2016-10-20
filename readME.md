Hi Github Community!

This is Vbob the codebuilder with my first ever git push.

This is basically something I threw together during downtime in my midterm week. Essentially, using an Microcontroller (MCU) like RPi or Intel Edison to connect to a Juicero (definitely a "must buy" when I have more money lol) and update me on my daily carb/fat/protein/caloric intake through text. It starts after I drink my morning fresh juice, and then I can text it back (using twilio) saying I had more protein or fat in a meal, and it will respond saying what percentage of my daily intake I have had so far.
I have a twilio trial account so I couldn't manage a lot of phone numbers it, so I chose to upload this CommandLine based program, rather than the SMS based (since it only works with my phone number and has private info to authenticate it). I also barely did this in a few gap hours during a busy week, so hopefully I'll go back and modify this when I have more time. 

Note: This push is the command line edited version, because I have a twilio trial account and was a litte limited on time/resources.

EXAMPLE OF HOW IT WORKS:

1. Microcontroller(MCU) texts "you have drank juice X with 10 grams protein -> 20% of daily intake"
2. User eats some food and texts back "protein 20"
3. MCU respones "You have consumed 60% of your daily protein intake" (10g+20g) / 50g total daily limit
4. User eats some food and texts "protein 30"
5. MCU responds "you have consumed more than your daily intake"

Note: Program accounts a little for typos and forgetting to send the amount of carbs/protein etc., because I felt like those would be things I forget or mess up while texting back, if I used this app reguarly.

TO RUN AT HOME:

1. comment out the libraries that are not installed on the computer that the program is being compiled on (most likely bs4, urrlib, matplotlib, numpy, twilio* and maybe flask)
2. run python3 Juicero_Code.py
