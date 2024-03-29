# Joshua Anthony Domantay
# Kevin Chaja
# COMP 467 - 21333
# 5 March 2023
# Import / export data

import os
import sys
import argparse
import csv

def read_file(filename):
    iofile = open(filename, 'r')
    lines = iofile.readlines()
    iofile.close()
    return lines

def quicksort(arr, low, high):
    if low < high:
        mid = partition(arr, low, high)
        quicksort(arr, low, (mid - 1))
        quicksort(arr, (mid + 1), high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if(int(arr[j]) <= int(pivot)):
            i += 1
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
    i += 1
    temp = arr[i]
    arr[i] = arr[high]
    arr[high] = temp
    return i

def get_xytech_info(job, filename):
    # Get lines from xytech file
    lines = read_file(filename)

    # Get header and locations info
    header = {
        "producer" : "",
        "operator" : "",
        "job" : "",
        "notes" : ""
    }
    path = ""
    for i in range(len(lines)):
        if "location:" == lines[i].strip().lower():
            # Get xytech file path
            i += 1
            path = lines[i].strip()
            path = path[:path.index(job)]
        if "notes:" == lines[i].strip().lower():
            header["notes"] = lines[i + 1].strip()
        elif ":" in lines[i]:
            line_info = lines[i].strip().split(":")
            key = line_info[0].strip().lower()
            val = line_info[1].strip()
            header[key] = val
    
    return header.values(), path

def get_baselight_info(job, filename):
    # Get lines from baselight file
    lines = read_file(filename)
    # Read each line
    data = []
    for line in lines:
        line_info = line.strip().split(" ")     # TODO: Does not take into account if file or folder has space
        if line_info[0] != "":
            new_row = []
            new_row.append(line_info[0].split(job)[1])      # Get path and remove local storage path
            frames = []
            for frame in line_info[1:]:     # Read frames
                if frame.isdigit():     # Avoid <err> or <null>
                    frames.append(frame)
            new_row.append(frames)
            data.append(new_row)
    return compress_baselight_data(data)

def compress_baselight_data(data):
    for i in range(len(data)):
        # Sort first just in case
        frames = data[i][1]
        quicksort(frames, 0, (len(frames) - 1))

        new_frames = []
        start_frame = frames[0]
        last_frame = frames[0]
        for frame in frames:
            if((int(frame) - int(last_frame)) > 1):     # Difference with last frame is greater than 1 = not consecutive
                if(start_frame != last_frame):
                    new_frames.append(start_frame + "-" + last_frame)       # Range
                else:
                    new_frames.append(start_frame)      # No consecutive frame
                start_frame = frame
            last_frame = frame
        if(start_frame != last_frame):
            new_frames.append(str(start_frame) + "-" + str(last_frame))     # Range
        else:
            new_frames.append(start_frame)      # No consecutive frame
        data[i][1] = new_frames
    return data

def add_sans_path_to_frames(job, path, job_and_frames):
    for i in range(len(job_and_frames)):
        job_and_frames[i][0] = path + job + job_and_frames[i][0]

def main(args):
    if args.jobFolder is None:
        print("No job selected")
        return 2
    if not os.path.isdir(args.jobFolder):
        print("Cannot find job")
        return 1
    else:
        xytech_filename = args.jobFolder + "/xytech.txt"
        if not os.path.exists(xytech_filename):
            print("Xytech file is missing")
            return 1
        header, sans_path = get_xytech_info(args.jobFolder, xytech_filename)
        baselight_filename = args.jobFolder + "/baselight_export.txt"
        if not os.path.exists(baselight_filename):
            print("Baselight export file is missing")
            return 1
        job_and_frames = get_baselight_info(args.jobFolder, baselight_filename)
        add_sans_path_to_frames(args.jobFolder, sans_path, job_and_frames)

        csv_filename = args.jobFolder + ".csv"
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerow([])
            writer.writerow([])
            for work in job_and_frames:
                for frames in work[1]:
                    writer.writerow([work[0], frames])
        csv_file.close()
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", dest="jobFolder", help="job to process")
    # parser.add_argument("--verbose", action="store_true", help="show verbose")
    # parser.add_argument("--TC", dest="timecode", help="Timecode to process")
    args = parser.parse_args()
    sys.exit(main(args))
