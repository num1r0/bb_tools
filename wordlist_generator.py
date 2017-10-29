"""
Wordlist generator tool.

Generates extended wordlist based on an initial list of possible words
Used mainly with hash cracking tools: hashcat, john, etc.

TO DO:
    - Add logging function

"""

import datetime
import itertools
import sys
import os

def usage():
    """ Usage function """
    usage_message = """Usage wordlist_generator.py [ OPTIONS ]

OPTIONS:
    -i          Path to initial wordlist file (default: wordlist.txt)
    -o          Name of the file to save generated wordlist (default: gen_ext_wl.txt)
    -t          Datetime got from 'date' command, used as origin timestamp (ex.: Sat 28 Oct 22:06:28 BST 2017)
    -w          Time window size (in seconds). Subtracted/added to origin timestamp
    -h          Display this menu
    
EXAMPLES:
    wordlist_generator.py -i wl.txt -o res.txt -t "Sat 28 Oct 22:06:28 BST 2017" -w 10
    """
    print usage_message

def create_permutations(wordlist):
    """
    Creates all possible permutations for given wordlist
    """
    extended_wordlist = []
    for length in range(0, len(wordlist)+1):
        for subset in itertools.permutations(wordlist, length):
            extended_wordlist.append("".join(subset))
    return extended_wordlist

def convert_to_epoch_time(origin):
    """
    Converts datetime into unix timestamp. Gets as an argument, result of linux 'date' command.

    Input example: Sat 28 Oct 22:06:28 BST 2017

    """
    pattern = "%a %d %b %H:%M:%S %Z %Y"
    timestamp = datetime.datetime.strptime(origin, pattern).strftime("%s")
    return timestamp

def generate_timestamps(epoch_origin, seconds_interval):
    """
    Gets origin timestamp and generates a list of them, based on specified interval of seconds
    """
    timestamps = []
    past_timestamp = int(epoch_origin) - int(seconds_interval)
    future_timestamp = int(epoch_origin) + int(seconds_interval)
    for timestamp in range(past_timestamp, future_timestamp+1):
        timestamps.append(timestamp)
    return timestamps

def generate_extended_wordlist(timestamps, wordlist):
    """
    For each timestamp, we generate the wordlist using permutations
    """
    extended_wordlist = []
    iter_wordlist = []
    for timestamp in timestamps:
        iter_wordlist = list(wordlist)
        iter_wordlist.append(str(timestamp))
        iter_extended_wordlist = create_permutations(iter_wordlist)
        del iter_wordlist[:]
        diff_wordlist = list(set(iter_extended_wordlist) - set(extended_wordlist))
        extended_wordlist += diff_wordlist
    return sorted(extended_wordlist)

def get_wordlist_from_file(file_path):
    """
    Simple read file function; omits newline '\n' character on each line
    """
    f = open(str(file_path), "r")
    wordlist = f.read().splitlines()
    return wordlist

def save_to_file(file_path, wordlist):
    """
    Simple write file function
    """
    if not str(file_path):
        file_path = "gen_ext_wl.txt"
    with open(file_path, 'w') as f:
        for word in wordlist:
            f.write(word)
            f.write("\n")
    f.close()

def main():
    """
    Entry point
    """
    arguments = sys.argv[1:]
    if len(arguments) <= 1:
        usage()
        exit(0)
    
    try:
        # Need help?
        arguments.index("-h")
        usage()
    except:
        # Get initial wordlist file name
        try:
            initial_wordlist_path = str(arguments[int(arguments.index("-i") + 1)])
        except:
            # Logging function
            initial_wordlist_path = "wordlist.txt"
        print initial_wordlist_path
        
        # Get file name to store generated wordlist
        try:
            new_wordlist_path = str(arguments[int(arguments.index("-o") + 1)])
        except:
            # Logging function
            new_wordlist_path = "gen_ext_wl.txt"
        print new_wordlist_path
        
        # Get origin timestamp
        try:
            origin_timestamp = str(arguments[int(arguments.index("-t") + 1)])
        except:
            # Logging function
            process = os.popen("date")
            origin_timestamp = str(process.read()).strip()
            process.close()
        print origin_timestamp
        
        # Get time window in seconds
        try:
            time_window_seconds = str(arguments[int(arguments.index("-w") + 1)])
        except:
            # Logging function
            time_window_seconds = 45
        print time_window_seconds

        initial_wordlist = get_wordlist_from_file(initial_wordlist_path)
        if not origin_timestamp.isdigit():
            origin_timestamp = convert_to_epoch_time(origin_timestamp)
        generated_timestamps = generate_timestamps(origin_timestamp, time_window_seconds)
        generated_extended_wordlist = generate_extended_wordlist(generated_timestamps, initial_wordlist)
        save_to_file(new_wordlist_path, generated_extended_wordlist)


if __name__ == "__main__":
    main()
