import argparse
from revseqs.revseqs import make_no_change_dict, revert_mutations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Revert sequences to consensus, but leave mutations positions unchanged',
            usage='revert_mutations_bam.py [-h] [-i,--input] [-v,--vcf] > <output_file>',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    g = parser.add_argument_group(title='input options',
                    description='''-in, --input <input>      Input file, must in indexed bam file
-vp, --vcf <vcf-file>     Path to vcf file''')
    parser.add_argument('-in', '--input', metavar='',
            help=argparse.SUPPRESS)
    parser.add_argument('-vp', '--vcf', metavar='',
            help=argparse.SUPPRESS)
    args=parser.parse_args()
    NO_CHANGE_DICT = make_no_change_dict(args.vcf)
    revert_mutations(args.input, NO_CHANGE_DICT)
    
