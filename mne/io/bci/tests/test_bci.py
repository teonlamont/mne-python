"""Data Equivalence Tests"""
from __future__ import print_function

# Authors: Teon Brooks <teon.brooks@gmail.com>
#
# License: BSD (3-clause)

import os.path as op
import inspect
import warnings

from nose.tools import assert_equal, assert_true

from mne import pick_types, concatenate_raws
from mne.utils import run_tests_if_main
from mne.io import read_raw_bci
from mne.io.constants import FIFF

warnings.simplefilter('always')

FILE = inspect.getfile(inspect.currentframe())
data_dir = op.join(op.dirname(op.abspath(FILE)), 'data')
bci_path = op.join(data_dir, 'test_bci.txt')
bci_missing_path = op.join(data_dir, 'test_bci_missing.txt')


def test_bci_data():
    """Test reading raw bci files"""
    sfreq = 125.
    raw = read_raw_bci(bci_path, eog=[0, 1], misc=[2], sfreq=sfreq,
                       preload=False)
    assert_true(raw.info['sfreq'] == sfreq)
    eog_picks = pick_types(raw.info, eog=True)
    misc_picks = pick_types(raw.info, misc=True)

    raw.info['chs'][eog_picks[0]]['kind'] == FIFF.FIFFV_EOG_CH
    raw.info['chs'][misc_picks[0]]['kind'] == FIFF.FIFFV_MISC_CH

    raw = read_raw_bci(bci_path, preload=True)
    assert_true('RawBCI' in repr(raw))
    picks = pick_types(raw.info, meg=False, eeg=True, exclude='bads')
    data, _ = raw[picks]

    with warnings.catch_warnings(record=True) as w:
        read_raw_bci(bci_missing_path, missing_tol=0)
    assert len(w) == 1

    # Make sure concatenation works
    raw_concat = concatenate_raws([raw.copy(), raw])
    assert_equal(raw_concat.n_times, 2 * raw.n_times)


run_tests_if_main()
