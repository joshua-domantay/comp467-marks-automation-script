# Joshua Anthony Domantay
# Kevin Chaja
# COMP 467 - 21333
# 5 March 2023
# Import / export data

import sys
import argparse
import csv

def read_file(filename):
    iofile = open(filename, 'r')
    lines = iofile.readlines()
    iofile.close()
    return lines

def get_baselight_info(filename):
    # Get lines from baselight file
    lines = read_file(filename)

    # Read each line
    info = {}
    for line in lines:
        line_info = line.strip().split(" ")     # TODO: Does not take into account if file or folder has space
        
        # If "location" is not recorded in info yet, instantiate a list for its value
        if line_info[0] not in info:
            info[line_info[0]] = []

        # Read frames
        for frame in line_info[1:]:
            if frame.isdigit():     # Avoid <err> or <null>
                info[line_info[0]].append(frame)
    
    return info

def get_xytech_info(filename):
    # Get lines from xytech file
    lines = read_file(filename)

    # Get header and locations info
    header = {
        "producer" : "",
        "operator" : "",
        "job" : "",
        "notes" : ""
    }
    locations = []
    for i in range(len(lines)):
        if "location:" == lines[i].strip().lower():
            i += 1
            while lines[i].strip() != "":       # Add to locations until newline
                locations.append(lines[i].strip())
                i += 1
        if "notes:" == lines[i].strip().lower():
            header["notes"] = lines[i + 1].strip()
        elif ":" in lines[i]:
            line_info = lines[i].strip().split(":")
            key = line_info[0].lower()
            val = line_info[1].strip()
            header[key] = val
    
    return header.values(), locations

def main(args):
    if args.jobFolder is None:
        print("No job selected")
        return 2
    # else if(if directory not exists)
    else:
        xytech_filename = args.jobFolder + "/xytech.txt"
        header, locations = get_xytech_info(xytech_filename)
        baselight_filename = args.jobFolder + "/baselight_export.txt"
        get_baselight_info(baselight_filename)

        csv_filename = args.jobFolder + ".csv"
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerow([])
            writer.writerow([])
            writer.writerow([])
        csv_file.close()
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", dest="jobFolder", help="job to process")
    # parser.add_argument("--verbose", action="store_true", help="show verbose")
    # parser.add_argument("--TC", dest="timecode", help="Timecode to process")
    args = parser.parse_args()
    sys.exit(main(args))
