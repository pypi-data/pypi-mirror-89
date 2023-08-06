import sys
import argparse
import logging
import getpass
import os
from . import samTobed
from . import pyWriter
from . import henipipe

POLL_TIME = 5
LOG_PREFIX = '[HENIPIPE]: '

# Set up a basic logger
LOGGER = logging.getLogger('something')
myFormatter = logging.Formatter('%(asctime)s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(myFormatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)
myFormatter._fmt = "[HENIPIPE]: " + myFormatter._fmt


def run_henipipe(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser('A wrapper for running henipipe')
    parser.add_argument('job', type=str, choices=['MAKERUNSHEET', 'ALIGN', 'SCALE', 'MERGE', 'SEACR', 'MACS2', 'AUC', 'GENOMESFILE', 'FASTQC'], help='a required string denoting segment of pipeline to run.  1) "MAKERUNSHEET" - to parse a folder of fastqs; 2) "ALIGN" - to perform alignment using bowtie and output bed files; 3) "SCALE" - to normalize data to reference (spike in); 4) "MERGE" - to merge bedgraphs 5) "SEACR" - to perform SEACR; 6) "MACS" - to perform MACS2; 7) "AUC" - to calculate AUC between normalized bedgraph using a peak file; 8) "GENOMESFILE" - print location of genomes.json file; 9) "FASTQC" - run fastqc on cluster')
    parser.add_argument('--sample_flag', '-sf', type=str, default="", help='FOR MAKERUNSHEET only string to identify samples of interest in a fastq folder')
    parser.add_argument('--fastq_folder', '-fq', type=str, help='For MAKERUNSHEET only: Pathname of fastq folder (files must be organized in folders named by sample)')
    parser.add_argument('--genome_key', '-gk', type=str, default="default", help='For MAKERUNSHEET only: abbreviation to use "installed" genomes in the runsheet (See README.md for more details')
    parser.add_argument('--filter_high', '-fh', type=int, default=None, help='For ALIGN only: upper limit of fragment size to exclude, defaults is no upper limit.  OPTIONAL')
    parser.add_argument('--filter_low', '-fl', type=int, default=None, help='For ALIGN only: lower limit of fragment size to exclude, defaults is no lower limit.  OPTIONAL')
    parser.add_argument('--output', '-o', type=str, default=".", help='For MAKERUNSHEET only: Pathname to write runsheet.csv file (folder must exist already!!), Defaults to current directory')
    parser.add_argument('--runsheet', '-r', type=str, help='tab-delim file with sample fields as defined in the script. - REQUIRED for all jobs except MAKERUNSHEET')
    parser.add_argument('--log_prefix', '-l', type=str, default='henipipe.log', help='Prefix specifying log files for henipipe output from henipipe calls. OPTIONAL')
    parser.add_argument('--select', '-s', type=str, default=None, help='To only run the selected row in the runsheet, OPTIONAL')
    parser.add_argument('--debug', '-d', action='store_true', help='To print commands (For testing flow). OPTIONAL')
    parser.add_argument('--bowtie_flags', '-b', type=str, default='--end-to-end --very-sensitive --no-mixed --no-discordant -q --phred33 -I 10 -X 700', help='For ALIGN: bowtie flags, OPTIONAL')
    parser.add_argument('--cluster', '-c', type=str, default='SLURM', choices=['PBS', 'SLURM', 'local'], help='Cluster software.  OPTIONAL Currently supported: PBS, SLURM and local')
    parser.add_argument('--threads', '-t', type=str, default=None, help='number of threads')
    parser.add_argument('--gb_ram', '-gb', type=str, default=None, help='gigabytes of RAM per thread')
    parser.add_argument('--install', '-i', type=str, default=None, help='FOR GENOMESFILE: location of file to install as a new genomes.json file, existing genomes.json will be erased')
    parser.add_argument('--norm_method', '-n', type=str, default='coverage', choices=['coverage', 'read_count', 'spike_in'], help='For ALIGN and SCALE: Normalization method, by "read_count", "coverage", or "spike_in".  If method is "spike_in", HeniPipe will align to the spike_in reference genome provided in runsheet. OPTIONAL')
    parser.add_argument('--user', '-u', type=str, default=None, help='user for submitting jobs - defaults to username.  OPTIONAL')
    parser.add_argument('--SEACR_norm', '-Sn', type=str, default='non', choices=['non', 'norm'], help='For SEACR: Normalization method; default is "non"-normalized, select "norm" to normalize using SEACR. OPTIONAL')
    parser.add_argument('--SEACR_stringency', '-Ss', type=str, default='stringent', choices=['stringent', 'relaxed'], help='FOR SEACR: Default will run as "stringent", other option is "relaxed". OPTIONAL')
    parser.add_argument('--keep_files', '-k', action ='store_true', default=False, help='FOR ALIGN: use this flag to turn off piping (Will generate all files).')
    parser.add_argument('--verbose', '-v', default=False, action='store_true', help='Run with some additional ouput - not much though... OPTIONAL')
    """
    call = 'henipipe MAKERUNSHEET -fq ../fastq -sf mini -gk heni_hg38 -o .'
    call = 'henipipe MACS2 -r ./runsheet.csv -d -mk -s 1:10'
    call = 'henipipe GENOMESFILE'
    call = 'henipipe MAKERUNSHEET -fq ../fastq'
    call = 'henipipe MAKERUNSHEET -fq ../fastq'
    call = 'henipipe ALIGN -r runsheet.csv -d'
    args = parser.parse_args(call.split(" ")[1:])
    """
    args = parser.parse_args()

    if args.job=="GENOMESFILE":
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        if args.install is None:
            GENOMES_JSON = os.path.join(_ROOT, 'data', 'genomes.json')
            print(GENOMES_JSON)
        if args.install is not None:
            from shutil import copyfile
            args.install = os.path.abspath(args.install)
            copyfile(args.install, os.path.join(_ROOT, 'data', 'genomes.json'))
        exit()
    #log

    #deal with user
    if args.user is None:
        args.user = getpass.getuser()

    #deal with paths
    if args.job=="MAKERUNSHEET":
        if os.path.isabs(args.fastq_folder) is False:
            if args.fastq_folder == ".":
                args.fastq_folder = os.getcwd()
            else :
                args.fastq_folder = os.path.abspath(args.fastq_folder)
        if os.path.exists(args.fastq_folder) is False:
            raise ValueError('Path: '+args.fastq_folder+' not found')
        if os.path.isabs(args.output) is False:
            if args.output == ".":
                args.output = os.getcwd()
            else :
                args.output = os.path.abspath(args.output)
        if os.path.exists(args.output) is False:
            raise ValueError('Path: '+args.output+' not found')
    if args.job != "MAKERUNSHEET":
        if os.path.exists(args.runsheet) is False:
            raise ValueError('Path: '+args.runsheet+' not found')
        args.output = os.path.abspath(args.output)


    if args.job=="MAKERUNSHEET":
        LOGGER.info("Parsing fastq folder - "+args.fastq_folder+" ...")
        LOGGER.info("Writing runsheet to - "+os.path.join(args.output, 'runsheet.csv')+" ...")
        LOGGER.info("Using genome_key - "+args.genome_key+" ...")
        henipipe.make_runsheet(folder=args.fastq_folder, output=args.output, sample_flag = args.sample_flag, genome_key = args.genome_key, no_pipe=args.keep_files)
        exit()

    #parse and chech runsheet
    args.runsheet = os.path.abspath(args.runsheet)

    """
    parsed_runsheet = list(parse_runsheet(args.runsheet))
    check_runsheet(args, parsed_runsheet, verbose=args.verbose)
    """
    parsed_runsheet = list(henipipe.parse_runsheet(args.runsheet))

    henipipe.check_runsheet(args, parsed_runsheet, verbose=args.verbose)

    #deal with sample selection
    if args.select is not None:
        parsed_runsheet = [parsed_runsheet[i-1] for i in list(henipipe.parse_range_list(args.select))]

    if args.debug == False:
        LOGGER.info("Logging to %s... examine this file if samples fail." % args.log_prefix)

    if args.job=="FASTQC":
        LOGGER.info("Running fastqc on all fastqs in runsheet")
        Fastqcjob = henipipe.Fastqc(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, cluster=args.cluster, log=args.log_prefix, user=args.user)
        Fastqcjob.run_job()
        exit()

    if args.job=="ALIGN":
        #deal with filtering
        LOGGER.info("Aligning reads...")




        #Alignjob = Align(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, no_pipe=args.keep_files, cluster=args.cluster, bowtie_flags=args.bowtie_flags, log=args.log_prefix, user=args.user, norm_method=args.norm_method, filter = [args.filter_low, args.filter_high])


        Alignjob = henipipe.Align(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, no_pipe=args.keep_files, cluster=args.cluster, bowtie_flags=args.bowtie_flags, log=args.log_prefix, user=args.user, norm_method=args.norm_method, filter = [args.filter_low, args.filter_high])
        LOGGER.info("Submitting alignment jobs... Debug mode is %s" % args.debug)
        Alignjob.run_job()
        exit()

    if args.job=="SCALE":
        LOGGER.info("Calculating %s", args.norm_method)
        Scalejob = henipipe.Scale(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, cluster=args.cluster, log=args.log_prefix, norm_method=args.norm_method, user=args.user)
        LOGGER.info("Submitting bedgraph jobs... Debug mode is %s" % args.debug)
        Scalejob.run_job()
        exit()

    if args.job=="MERGE":
        Mergejob = henipipe.Merge(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, cluster=args.cluster, log=args.log_prefix, norm_method=args.norm_method, user=args.user, out=args.output)
        #Mergejob = Merge(runsheet_data = parsed_runsheet, debug=args.debug, cluster=args.cluster, log=args.log_prefix, norm_method=args.norm_method, user=args.user)
        LOGGER.info("Submitting merge-bedgraph jobs... Debug mode is %s" % args.debug)
        Mergejob.run_job()
        exit()

    if args.job=="SEACR":
        LOGGER.info("Running SEACR using settings: SEACR_norm = %s, SEACR_stringency = %s" % (args.SEACR_norm, args.SEACR_stringency))
        SEACRjob = henipipe.SEACR(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, cluster=args.cluster, norm=args.SEACR_norm, stringency=args.SEACR_stringency, user=args.user, log=args.log_prefix)
        SEACRjob.run_job()
        exit()

    if args.job=="MACS2":
        LOGGER.info("Running MACS2")
        MACS2job = henipipe.MACS2(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, cluster=args.cluster, user=args.user, log=args.log_prefix, out=args.output)
        MACS2job.run_job()
        exit()

    if args.job=="AUC":
        LOGGER.info("Running AUC")
        AUCjob = henipipe.AUC(runsheet_data = parsed_runsheet, threads = args.threads, gb_ram = args.gb_ram, debug=args.debug, no_pipe=args.keep_files, cluster=args.cluster, user=args.user, log=args.log_prefix, out=args.output, norm=args.SEACR_norm, stringency=args.SEACR_stringency)
        AUCjob.run_job()
        exit()


if __name__ == "__main__":
    run_henipipe()

"""
[parsed_runsheet[i-1] for i in list(parse_range_list("1:4,11,12"))]

"""



