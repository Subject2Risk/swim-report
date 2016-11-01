# swim-report
Excel sheet to format swimmer data with relevant standards.

## Importing data
### Directly into Excel
1. Goto swimrankings.net and lookup the athelete your interested in, taking note of their 6 digit swimmer ID.
2. Copy the swimmer data (using your mouse to select the table data)
3. Paste it into an empty Excel sheet as plain text.
  1. In the empty Excel sheet, select, then right click on cell A1.
  2. Choose "Paste Special ..."
  3. In the "As:" dialogue, select "Text" then click "OK"
4. Add the swimmer's name and 6 digit ID to the swimmer's page.
5. Add the distance and event names to the csv .... Ugghh ... just figure it out or use the unix scripts.


### Unix
1. Goto swimrankings.net and lookup the athelete your interested in, taking note of their 6 digit swimmer ID.
2. Copy the swimmer data (using your mouse to select the table data)
3. In a Bash prompt at the root directory of the this project, run this command:
    bin/swimmer-cut-n-past | bin/cut-sort > swim-data/{6 digiti swimmer ID}.csv
4. Add the swimmer data to the blue "Swimmers" page (be sure to insert a row).

