#!/usr/bin/env python3.4
import ursgal
import os
import pprint
from collections import defaultdict as ddict
import csv
import itertools
import sys

from .msfragger_20190628 import msfragger_20190628 as msfragger

class msfragger_2_3( msfragger ):
    """
    MSFragger unode

    Note:
        Please download and install MSFragger manually from
        http://www.nesvilab.org/software.html

    Reference:
    Kong, A. T., Leprevost, F. V, Avtonomov, D. M., Mellacheruvu, D., and Nesvizhskii, A. I. (2017)
    MSFragger: ultrafast and comprehensive peptide identification in mass spectrometry–based
    proteomics. Nature Methods 14

    Note:
        Addition of user amino acids not implemented yet. Only mzML search
        possible at the moment. The mgf file can still be passed to the node,
        but the mzML has to be in the same folder as the mgf.

    Warning:
        Still in testing phase!
        Metabolic labeling based 15N search may still be errorprone. Use with
        care!

    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'MSFragger',
        'version'                     : '2.3',
        'release_date'                : '2020-01-30',
        'utranslation_style'          : 'msfragger_style_3',
        'input_extensions'            : ['.mgf', '.mzML', '.mzXML'],
        'output_extensions'           : ['.csv'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'           : False,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'engine'                      : {
            'platform_independent'    : {
                'arc_independent' : {
                    'exe'            : 'MSFragger-2.3.jar',
                    'url'            : 'http://www.nesvilab.org/software.html',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation'                   : \
            'Kong, A. T., Leprevost, F. V, Avtonomov, '
            'D. M., Mellacheruvu, D., and Nesvizhskii, A. I. (2017) MSFragger: '
            'ultrafast and comprehensive peptide identification in mass '
            'spectrometry-based proteomics. Nature Methods 14'
    }