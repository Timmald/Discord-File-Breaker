# Discord-File-Breaker
I try to let myself and a few friends circumvent the oppressive discord upload limits.

**HOW IT WORKS:**
1. You upload files and it breaks them into chunks that fit the upload restriction and uploads those to discord via a bot, along with a report of what it uploaded
2. The master bot reads the report and updates `filePieces.json` on my home computer
3. The app uses another bot to ask for the current choices when it opens and when you refresh downloads list
4. The master bot picks the 10 most recent files that have been uploaded and sends them to your bot over discord
5. Your bot reads that and updates your personal `currentChoices.json`, and uses the choice data to make a list of buttons in the download screen
6. Each button makes a bot search the channel to find when that file was uploaded and then download all the attachments and recombine them into the original file
