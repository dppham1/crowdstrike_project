A brief description of what I made for this project, followed by what was my justification for why I chose to do so:

    - Client (main.py and get_breaches.py)
        - get_breaches.py
            - Various functions that retreive breach data from the haveibeenpwned API, then send the data over to the syslog server
        - main.py
            - Main function that relies on functions from the "get_breaches.py" file
            - Handles the daily updating of the "breaches.json" file using a python library called "Schedule". If you'd rather not have the main.py script 
              running 24/7 to have the daily update happen, you can also schedule cron to run the "main.py" file every day. I tested this and it also works,
              but on Macs with Mojave OS and onwards, there is an access control mechanism that prevents cron from accessing the drive. In order to fix this, 
              you have to give cron full access to your drive (which can be a big security issue), so I'm opting to keep the python script up 24/7. 
              These are the steps to give cron full access to get the other approach to work: https://blog.bejarano.io/fixing-cron-jobs-in-mojave/

    - Server (syslogger.py)
        - Created a mock syslog server using Flask. Though I know that you mentioned this wasn't necessary, I couldn't think of a clearer way to prove that
          data from the client was being sent to the server-side correctly. The server has 2 endpoints that logs files using python's logging module.
            - logDomainBreach
                - Logs all domain-related breaches to a folder called domain_logs
            - logUserBreach 
                - Logs all user-related breaches to a folder called user_logs 


Justifications

- Why did I choose to store the data inside a .json file?
    - I didn't think there was a need to do anythign complex and run a DB for this project for 2 reasons:
        
        1) The data we're dealing with on a day-to-day basis isn't terribly large and can easily be parsed as a JSON object for easy access. The size for
           the "breaches.json" file (which contains all breaches) is only around 447KB.
        
        2) This application only runs once a day, and there are very minimal interactions. Obviously for a larger application, we'd need to migrate to an
           actual DB, but for the sake of time and functionality, .json local storage works well for this project.