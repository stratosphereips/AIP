02/04/2020
V1.0.0
- First major commit, via the correct methods
- Removed old files that were no longer relevant
- Committed Main and Run-AIP.sh, but not Eval and Total_Eval.sh because both still contain personal identifiers

24/04/2020
V1.0.1
- Separated eval module into another repo
- Separated eval script and run AIP script
- Worked on organization
- Deleted unecessary functions in AIP.py
- Removed old module files

28/04/2020
V1.0.2
- Fixed problem with calling modules incorrectly
- Add ability to choose new instance, or running instance
- Asks for input data file location
- Checks if input directory exits
- If directoy exist, creates needed folders in it, if it does not, asks if we wisd to continue, and creates it all
- If not a new instance, simple asks where the old instance is.
- IMPORTANT - There is a bug with updating an old instance!

07/05/2020
V1.0.3
- Updated README.md files
- Updated AIP-How-To-Guide.md

22/07/2020
V2.0.0
- Added a whitlist module, namely before using the main data file, program will check for IPs that should not be blacklisted
- Added an auto-run script. 
- Changed the aging function so it keeps track og how much an IP needs to be reduced over time
- Changed the threshold so that it is dynamic again
- Fixed the cannot check whitelist bug
- Fixed the infinite loop bug for the prioritize new normalized rating function
- Fixed other small bugs and improved code

24/07/2020
V2.0.1
- Minor bug fixes

