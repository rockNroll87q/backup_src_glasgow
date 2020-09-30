# Backup source code in project folders [GLASGOW]

Hello there!

Are you worried about possible losses of your source code in the project folder?
Do you make, as myself, so many stupid errors and wrongly delete/modify src code?
Do you think could be a good idea to have a local version of your code?
If yes, this is the email for you!

This post is meant to be useful to my colleagues in Glasgow. 
This code performs automatic weekly full backups (not incremental nor sequential) of source codes only, 
from my project folders (grid) to a local folder (i.e., in my desktop), 
and send a full report to my email address. 
It is scheduled, which means you don’t need to do anything else than check the weekly email that arrives you.
In the email (see attached an example) there is also written the size of your project folder.
Being backup only src code, the size is very small ~40MB per backup, which means <3GB per year!

First, you need:

* a local PC with:
* space to store data;
* `python3`;
* access to project folders;
* an email address as sender (optional).

Second, you need to download the script called `backup_srcs.py` and modify the part `Paths and Constants`, specifying:

~~~
Path_in = '/analyse/'
Proj_to_backup = ['Project0204','Project0233','Project0235']
Path_out = '/path/to/your/local/folder/'
Files_to_keep = ['.py', '.m', '.sh', '.md', '.ipynb', 'what.txt']   # which files to keep
Path_to_exclude = ['/analyse/Project0204/packages/']

HOST = 'smtp.gmail.com'
USER = 'your_account@gmail.com'
PWD = 'you_PSW'
TO = 'Michele.Svanera@glasgow.ac.uk'
~~~

Finally, to schedule the weekly task, we use cron. Take a look [here](https://crontab.guru/) on how to specify the scheduling.

~~~
$ crontab -e        # to enter the editor 

# Insert weekly backup
00 20 * * 2 /usr/bin/python3 /path/to/backup_srcs.py
~~~

In my case, my script runs at 20:00 on Tuesday (2nd day of the week).

Done!
