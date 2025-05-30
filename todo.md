# To do

- Parse CIDR range input so only those IPs in scope are displayed
- Add instructions to readme. Use the `help` command for now.
- Add support for nmaps gnmap and xml outputs
- Track a list of all findings to be decided on keeping or replacing, so that the 'All' option can be included. Also to allow for a counter for how many are left to be checked.

# Done

- Handle duplicates in the findings. Figure out how to decide which to keep (The one with more info or the one that is newer?) 
- Add a datetime element in the finding class
- Add a file element in the finding class < to keep track of where the finding was added from
- Add a config file to keep track of settings like 'no-comments' and last open session
- Parse multiple IP scans into separate classes to allow for selected IP display
- Prompt export on exit? 
- Track session name so when it us exported again the name is not overwritten to "_" and uses the previous session name unless otherwise specified
- Have Import/Export output a message saying they have done something
- lower input so mixed capitals work
- Add Message for when show subcommand does not exist
- Make sessions save in the same session they were opened from (if imported from a session). So, overwrite if a previous session is saved instead of creating a new one
- Add a check when reading a file via load for '.nmap' extension as to not break the parser
- Add a check to make sure when exporting a session the provided name is unique
- try except block on base64 decode, will stop the program from crashing if the base64 encoded json is damaged
- Parse .nessus content too to also allow for the use of the commands from this script with nessus output
- Save contents as a config file of some kind to allow merger of nessus and nmap scans to allow this tool to keep track of all scans done 
- Include some kind of command line utility to allow for multiple commands in the same session