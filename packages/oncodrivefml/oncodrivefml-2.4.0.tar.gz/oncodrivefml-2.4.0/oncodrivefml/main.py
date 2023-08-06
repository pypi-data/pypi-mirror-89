"""
Contains the command line parsing
"""

import logging
import os
import warnings
from collections import defaultdict
from os import path

import bglogs
import click

from oncodrivefml import __version__
from oncodrivefml.config import load_configuration, file_name
from oncodrivefml.oncodrivefml import OncodriveFML

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(mutations_file, elements_file, output_folder, config_file, samples_blacklist,
         config_override_dict=None, force=False):
    """
    Run OncodriveFML analysis

    Args:
        mutations_file (str): path to the mutations file
        elements_file (str): path to the elements file
        output_folder (str): path to the output folder. Set to :obj:`None` to create
           a folder with the elements file name in the current directory.
           If provided, and does not exists,
        config_file (str): path to configuration file
        samples_blacklist (str): path to samples blacklist file. Set to :obj:`None`
           if you are not using any blacklist file
        config_override_dict (dict, optional): override configuration from file

    """

    output_folder = file_name(elements_file) if output_folder is None else output_folder
    output_file = path.join(output_folder, file_name(mutations_file) + '-oncodrivefml.tsv.gz')
    # Skip if done
    if path.exists(output_file) and not force:
        logging.warning("Already calculated at '{}'".format(output_file))
        return
    else:
        if not path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)

    configuration = load_configuration(config_file, override=config_override_dict)
    if 'logging' in configuration:
        warnings.warn('"logging" option from configuration is no longer supported', DeprecationWarning)

    analysis = OncodriveFML(mutations_file, elements_file, output_folder,
                            configuration, samples_blacklist)

    bglogs.info('Running analysis')
    # Run the analysis
    analysis.run()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'mutations_file', type=click.Path(exists=True), help='Variants file', metavar='MUTATIONS_FILE', required=True)
@click.option('-e', '--elements', 'elements_file', type=click.Path(exists=True), metavar='ELEMENTS_FILE', help='Genomic elements to analyse', required=True)
@click.option('-t', '--type', type=click.Choice(['coding', 'noncoding']), help='Deprecated option')
@click.option('-s', '--sequencing', type=click.Choice(['wgs', 'wes', 'targeted']), help='Type of sequencing: whole genome, whole exome or targeted.')
@click.option('-o', '--output', 'output_folder', type=click.Path(), metavar='OUTPUT_FOLDER', help="Output folder. Default to regions file name without extensions.", default=None)
@click.option('-c', '--configuration', 'config_file', default=None, type=click.Path(exists=True), metavar='CONFIG_FILE', help="Configuration file. Default to 'oncodrivefml_v2.conf' in the current folder if exists or to ~/.config/bbglab/oncodrivefml_v2.conf if not.")
@click.option('--samples-blacklist', default=None, type=click.Path(exists=True), metavar='SAMPLES_BLACKLIST', help="Remove these samples when loading the input file.")
@click.option('--signature', 'signature_file', default=None, type=click.Path(exists=True), metavar='SIGNATURE', help="File with the signatures to use")
@click.option('--signature-correction', type=click.Choice(['wg', 'wx']), help='Correct the computed signutares by genomic or exomic signtures. Only valid for human genomes', default=None)
@click.option('--no-indels', help="Discard indels in your analysis", is_flag=True)
@click.option('--cores', help="Cores to use. Default: all", default=None, type=int)
@click.option('--seed', help="Set up an initial random seed to have reproducible results", type=click.IntRange(0, 2**32-1), default=None)
@click.option('--generate-pickle', help="Deprecated flag. Do not use.", is_flag=True)
@click.option('--force', help="Overwrite results if exists", is_flag=True)
@click.option('--debug', help="Show more progress details", is_flag=True)
@click.version_option(version=__version__)
def cmdline(mutations_file, elements_file, type, sequencing, output_folder, config_file, samples_blacklist,
            signature_file, signature_correction, no_indels, cores, seed, generate_pickle, force, debug):
    """
    Run OncodriveFML on the genomic regions in ELEMENTS FILE
    using the mutations in MUTATIONS FILE.

    """

    bglogs.configure(debug=debug)
    warnings.filterwarnings("default", category=DeprecationWarning, module='oncodrivefml*')

    dd = lambda: defaultdict(dd)
    override_config = dd()

    # Overrride the configuration
    if no_indels:
        override_config['statistic']['indels']['include'] = False

    if type is not None:
        warnings.warn('--type option is no longer supported. '
                      'Edit the configuration file appropriately',
                      DeprecationWarning)

    if sequencing is not None:
        warnings.warn('--sequencing option has been replaced by '
                      '--signature-correction',
                      DeprecationWarning)

    if signature_correction == 'wx' or (signature_correction is None and sequencing == 'wes'):
        override_config['signature']['normalize_by_sites'] = 'whole_exome'
    elif signature_correction == 'wg' or (signature_correction is None and sequencing == 'wgs'):
        override_config['signature']['normalize_by_sites'] = 'whole_genome'
    elif sequencing == 'targeted':
        override_config['signature']['normalize_by_sites'] = None

    if signature_file is not None:
        override_config['signature']['method'] = 'file'
        override_config['signature']['path'] = signature_file

    if generate_pickle:
        warnings.warn('--generate-pickle option is no longer supported', DeprecationWarning)
        return

    if seed is not None:
        override_config['settings']['seed'] = seed

    if cores is not None:
        override_config['settings']['cores'] = cores

    main(mutations_file, elements_file, output_folder, config_file, samples_blacklist, override_config, force)


if __name__ == "__main__":
    cmdline()
