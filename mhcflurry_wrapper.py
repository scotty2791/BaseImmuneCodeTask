import argparse
import os
import re
import subprocess
import sys

ENV_NAME = "mhcflurry_env"


def main():

    tools_available = ['mhcflurry-predict-scan', 'mhcflurry-downloads info',
                       "mhcflurry-downloads fetch", "set up environment", "teardown environment"]
    print("Tools available are:")

    for index, val in enumerate(tools_available):
        print("{0}. {1}".format(index, val))

    valid_input = False
    while not valid_input:
        try:
            selection = int(input("Select tool to use:"))
        except ValueError as ve:
            continue
        if int(selection) < len(tools_available):
            valid_input = True
            tool_selected = tools_available[selection]

    match tool_selected:
        case "mhcflurry-predict-scan":
            command = run_mhcflurry_predict_scan_wrapper()
        case "mhcflurry-downloads info":
            command = run_mhcflurry_download_info()
        case "mhcflurry-downloads fetch":
            command = run_mhcflurry_fetch_downloads()
        case "set up environment":
            command = setup_env()
        case "teardown environment":
            command = teardown_env()

    run_wrapper(command)


def run_wrapper(command):
    '''Dedicated wrapper to run the command constructed'''
    subprocess.run(command, shell=True)

### Tool Options ###


def setup_env():
    '''This creates the conda environent based on the .yml file alongside this script.
    Note, when sharing the .yml file, the user will need to change their prefix folder directory.'''

    print("\nSetting up the run environment...")

    # Create a conda env from the environment.yml file. This ensures the latest repo version is used.
    create_env = "conda env create -f environment.yml"
    return create_env


def teardown_env():
    '''Clears the environment of installed packages.'''

    print("\nRemoving run environment...")

    # Teardown - remove the environment used
    remove_env = "conda remove --name {} --all".format(ENV_NAME)
    return remove_env


def get_inputs():
    '''Gather inputs for sequence, allele, output file location for interactive use'''

    valid_sequence = False
    valid_allele = False

    while not valid_sequence:
        sequence = input("Sequence to be tested: ")
        valid_sequence = check_sequence(sequence)

    while not valid_allele:
        allele = input("Allele to be tested: ")
        valid_allele = check_allele(allele)

    output = input("Location of output file: ")
    if not os.path.isdir(os.path.dirname(output)):
        print("No such directory exists, defaulting to './tempfile.csv'")
        output = "./tempfile.csv"

    return sequence, allele, output


def run_mhcflurry_predict_scan_wrapper():
    '''
    Collect args for the mhcflurry-predict-scan tool and 
    Sequence - String of uppercase letters
    Allele - String of uppercase letters, dash (-), asterisk (*), colon (:), numbers (0-9) only.
    '''

    print("\nRunning mhcflurry_predict_scan...")

    sequence, allele, output = get_inputs()
    command = run_mhcflurry_predict_scan(sequence, allele, output)
    return command


def run_mhcflurry_predict_scan(sequence, allele, output):
    '''Create the command needed to run, based on gathered inputs
    '''

    # Create the command to run the tool with correct cmd line args
    command = "conda activate {0} && mhcflurry-predict-scan --sequences {1} --allele {2} --out {3}".format(
        ENV_NAME, sequence, allele, output)
    return command


def run_mhcflurry_download_info():
    '''This will show the downloaded model data and if they are up-to-date'''

    print("\nShowing status of mhcflurry-downloads model data...")

    # Create the command to run the tool with correct cmd line args
    command = "conda activate {0} && mhcflurry-downloads info".format(ENV_NAME)
    return command


def run_mhcflurry_fetch_downloads():
    '''This will download the default model data.
    This is: models_class1_presentation, data_curated, models_class1'''

    print("\nFetching default mhcflurry-downloads data...")

    # Create the command to run the tool with correct cmd line args
    command = "conda activate {0} && mhcflurry-downloads fetch".format(
        ENV_NAME)
    return command


### Validation ###

def check_sequence(sequence):
    '''Check whether the sequence contains only uppercase letters A to Z.'''
    sequence_regex = re.compile('^[A-Z]+$')

    if sequence_regex.match(sequence):
        return True

    return False


def check_allele(allele):
    '''Check whether the allele contains only uppercase letters A to Z, numbers 0-9, asterisk, dash and colon only.'''
    allele_regex = re.compile('^[A-Z0-9:*-]+$')

    if allele_regex.match(allele):
        return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run mchflurry-predict-scan")
    parser.add_argument("--sequence", nargs='?', help="Sequence to input")
    parser.add_argument("--allele", nargs='?', help="Allele to input")
    parser.add_argument("--output", nargs='?',
                        help="Output file location and name")

    if len(sys.argv) > 1 and len(sys.argv) < 7:
        sys.exit("If any cmd line args are set, all arguments must be provided")

    if len(sys.argv) == 7:
        args = parser.parse_args()
        run_wrapper(run_mhcflurry_predict_scan(
            args.sequence, args.allele, args.output))
    else:
        main()


# sequence = "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHS"
# allele = "HLA-A*02:01"
