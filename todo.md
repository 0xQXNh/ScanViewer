# todo

- [x] Parse multiple IP scans into separate classes to allow for selected IP display
    - [ ] Parse CIDR range input so only those IPs in scope are displayed

- [ ] Add instructions to readme. Use the `help` command for now.

- [ ] Prompt export on exit? 
- [ ] Track session name so when it us exported again the name is not overwritten to "_" and uses the previous session name unless otherwise specified
- [x] Have Import/Export output a message saying they have done something
- [x] lower input so mixed capitals work
- [x] Add Message for when show subcommand does not exist
- [x] Make sessions save in the same session they were opened from (if imported from a session). So, overwrite if a previous session is saved instead of creating a new one
- [x] Add a check when reading a file via load for '.nmap' extension as to not break the parser
- [x] Add a check to make sure when exporting a session the provided name is unique
- [x] try except block on base64 decode, will stop the program from crashing if the base64 encoded json is damaged

# Maybe todo

- [x] Parse .nessus content too to also allow for the use of the commands from this script with nessus output
- [x] Save contents as a config file of some kind to allow merger of nessus and nmap scans to allow this tool to keep track of all scans done 
- [x] Include some kind of command line utility to allow for multiple commands in the same session
