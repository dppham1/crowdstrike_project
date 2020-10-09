# Breaches Project
- Gets a list of known breaches associated with a User and stores this into the breaches.json file
- Newly updated breach information from the Haveibeenpwned API is automatically fetched on a daily basis
- In the event that a breach is reported, all metadata for that breach is sent to a syslog server with the appropriate syslog format
- Scaled the application by using Python's threadpool module in order to check for all email addresses in parallel
