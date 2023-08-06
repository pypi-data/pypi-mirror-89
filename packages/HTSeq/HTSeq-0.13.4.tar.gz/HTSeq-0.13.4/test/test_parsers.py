import pytest
import sys
import os
import glob
import distutils.util

build_dir = "build/lib.%s-%s" % (distutils.util.get_platform(), sys.version[0:3])

sys.path.insert(0, os.path.join(os.getcwd(), build_dir))
import HTSeq


def test_fasta_parser(data_folder):
    print("Test Fasta parser")
    for seq in HTSeq.FastaReader(data_folder+'fastaExLong.fa'):
        pass
    print("Test passed")
    print("Test Fasta parser (raw iterator)")
    for seq in HTSeq.FastaReader(data_folder+'fastaExLong.fa',
                                 raw_iterator=True):
        pass
    print("Test passed")

    print('Test Fasta parser (with statement)')
    with HTSeq.FastaReader(data_folder+'fastaExLong.fa') as f:
        for seq in f:
            pass
    print('Test passed')

    print('Test Fasta parser (with statement and file handle)')
    with open(data_folder+'fastaExLong.fa') as fraw:
        f = HTSeq.FastaReader(fraw)
        for seq in f:
            pass
    print('Test passed')


def test_fastq_parser(data_folder):
    print("Test Fastq parser")
    for seq in HTSeq.FastqReader(data_folder+'fastqEx.fastq'):
        pass
    print("Test passed")
    print("Test Fastq parser on gzip input")
    for seq in HTSeq.FastqReader(data_folder+'fastqExgzip.fastq.gz'):
        pass
    print("Test passed")
    print("Test Fastq parser on gzip input (raw iterator)")
    for seq in HTSeq.FastqReader(data_folder+'fastqExgzip.fastq.gz',
                                 raw_iterator=True):
        pass
    print("Test passed")

    print('Test Fastq parser (with statement)')
    with HTSeq.FastqReader(data_folder+'fastqExgzip.fastq.gz') as f:
        for seq in f:
            pass
    print('Test passed')

    print('Test Fastq parser (with statement and file handle)')
    import gzip
    with gzip.open(data_folder+'fastqExgzip.fastq.gz', 'rt') as fraw:
        f = HTSeq.FastqReader(fraw)
        for seq in f:
            pass
    print('Test passed')


def test_bam_reader(data_folder):
    print('Test BAM reader')
    bamfile = HTSeq.BAM_Reader(data_folder+"yeast_RNASeq_excerpt.sam")
    for read in bamfile:
        pass
    print('Test passed')

    print('Test BAM reader (with statement)')
    with HTSeq.BAM_Reader(data_folder+"yeast_RNASeq_excerpt.sam") as f:
        for read in f:
            pass
    print('Test passed')


def test_bam_inconsistent_mate(data_folder):
    print('Test inconsistent BAM file')
    bamfile = HTSeq.BAM_Reader(data_folder+"inconsistent_mate.bam")
    for read in bamfile:
        pass
    print("Test passed")


def test_pickle():
    import pickle

    print('Test pickling and inpickling')
    pickles = [
            {'name': 'HTSeq.Sequence',
             'object': HTSeq.Sequence(b'ACTG', 'sequence'),
             'assert_properties': ('seq', 'name', 'descr')},
            ]

    for pic in pickles:
        print('Pickling '+pic['name'])
        pickled = pickle.dumps(pic['object'])
        print('Done')

        print('Unpickling '+pic['name'])
        unpick = pickle.loads(pickled)
        print('Done')

        if 'assert_properties' in pic:
            print('Checking serialized/deserialized')
            for prop in pic['assert_properties']:
                assert getattr(pic['object'], prop) == getattr(unpick, prop)
            print('Done')
    print("Test passed")


def test_bamfile_nosq(data_folder):
    print('Test parsing BAM file with no SQ field (e.g. PacBio)')
    bamfile = HTSeq.BAM_Reader(
            data_folder+"short_test_ccs.bam",
            check_sq=False)
    for read in bamfile:
        pass
    print("Test passed")
