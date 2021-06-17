"""
    @package
    pooling out:
        refs as "Designator", 
        Comment, 
        Qnty and 
        PN of 
    GROUPPED symbols into CSV file
    
    (c) VORELEC
"""
# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2]+'.csv', 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout


# subset the components to those wanted in the BOM, controlled
# by <configure> block in kicad_netlist_reader.py
components = net.getInterestingComponents()


# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

out.writerow(['Designator','Comments', 'Qnty', 'PN']) #column names go to scv already


grouped = net.groupComponents()
# Output all of the component information
for group in grouped:
    refs = ""
    
    for component in group:
        refs += component.getRef() + ", "   #collecting refs into one string with commas
        c = component
    refs = refs[:-2] #remouving last comma and space     
    out.writerow([refs, c.getPartName(),len(group), c.getField("PN")])  #write each group as a line to csv file
    


