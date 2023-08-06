#===============================================================================
# splitbam.py
#===============================================================================

"""Split a BAM file into two subsamples"""

import os.path
import pysam
import subprocess
import tempfile

from argparse import ArgumentParser


# Functions ====================================================================

def parse_arguments():
    parser = ArgumentParser(description='Split a BAM file into two subsamples')
    parser.add_argument(
        'input',
        metavar='<path/to/input.bam>',
        help='path to input BAM file'
    )
    parser.add_argument(
        'output',
        metavar=('<path/to/output1.bam>', '<path/to/output2.bam>'),
        nargs=2,
        help='paths to output BAM files'
    )
    parser.add_argument(
        '--tmp-dir',
        metavar='<path/to/tmp/dir>',
        help='directory for temporary files'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    with tempfile.TemporaryDirectory(dir=args.tmp_dir) as temp_dir:
        temp_in = os.path.join(temp_dir, 'namesort_in.bam')
        temp_out0 = os.path.join(temp_dir, 'namesort_out1.sam')
        temp_out1 = os.path.join(temp_dir, 'namesort_out2.sam')
        pysam.sort('-n', '-o', temp_in, args.input)
        pysam.view('-H', '-o', temp_out0, temp_in)
        pysam.view('-H', '-o', temp_out1, temp_in,)
        with open(temp_in, 'r') as f:
            with subprocess.Popen(
                ('samtools', 'view'), stdin=f, stdout=subprocess.PIPE
            ) as view:
                subprocess.run(
                    ('awk', f'{{if(NR%4<2){{print >> "{temp_out0}}}"}} else {{print >> "{temp_out1}}}"}}}}'),
                    stdin=view.stdout,
                )
        pysam.view('-bh', '-o', args.output[0], temp_out0)
        pysam.view('-bh', '-o', args.output[1], temp_out1)



    
    