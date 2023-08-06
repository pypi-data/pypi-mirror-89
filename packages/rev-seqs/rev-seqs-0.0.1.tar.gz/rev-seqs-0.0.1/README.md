# rev-seqs: Revert Sequences to Consensus Preserving Variants

rev-seqs is a command line utility to revert sequences to consensus preserving variants detected in a VCF file. It reverts all other positions the sample consensus

# Usage
Once installed rev-seqs is just a simple command line command.

```shell
python -m revseqs --input <input file> --vcf <vcf file> > <output_file>
```

run `python revseqs -h` for more options

The new bam file is written to standard output.
Input file must be an indexed bam file

## Inserts
Any inserts that are not flagged as variants are removed, those inserts along with sample header are printed to standard error. The sample name is followed by a comma separated list of insert positions that were removed.

To save this file for future inspect redirect standard error to a file using the command below 

```shell
python -m revseqs --input <input.bam> --vcf <variants.vcf> > <output.bam> 2> <inserts>
```

# Installation

```shell
pip install rev-seqs
```

# Collaboration
If you have any issues, bugs, or feature requests please contact the author, <nhannguyen72089@gmail.com>
