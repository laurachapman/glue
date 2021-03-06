from __future__ import absolute_import, division, print_function

import os

from numpy.testing import assert_array_equal

from glue.core import data_factories as df
from glue.tests.helpers import requires_xlrd, make_file


DATA = os.path.join(os.path.dirname(__file__), 'data')


@requires_xlrd
def test_load_data():

    data = b'x\xda\xedX=h\x14A\x14\xfef\xf7\xfeI.\xbb\xe7EL\x84\xb0\x04\x8c\x1a\xd3\x04\x1b\x9bdOAS\x19\xa2\x16\x8a\x08z1\x0bJ\xc2E\x8e\x14\xc6\xc6h\xbcR\x10\xac\x14\x9b@\x1a\x9b\xa8\x8d?\x18A;\x0b!\xa2\x85 \x08w\n6V\x82B\x8a\xe4\xd67og\xcd%^q\x07\x1aT\xe6[\xe6\xcd\xdb7\xdf\xdby\xc7\xbcy{\xb3\xaf\x97\xec\xf2\xdc\x83\xce\n6`\x10&\xaa~\x12\xb1\x1a\x9b\xa0\x96\x0co,\xd0\xb8\xefK5\xec\x13\xd4|\x8d\x7f\n\xc9\x04-d,\x8a\xa7\xad\xaf\xe2r\r\xe5zW`\xe0~\xe4\x05I\xe0#\xb5S\xb8\x80\xe1\xc9\x82\xe7l"\x0ep\x0cy!c\x18 )p\x87,itpT\x19\x96gYnay\x8f\x99\x8b,sl\xb9\xcer\x80\xb8eq\x12K\xeep\xef>\x95\xc5\'\x8cn\x1eKC>\xf7\x11\xfb\xbcgK?\xda\xf1Rf\xf1\xe5\x1b"\xe0F\xb1\xbfx>?\xf1\x17\x0c\x08\x1aX4\x1a\xf3\xe8\x8a\xb4`\x1e\xb4\xa0C^\xc1+\xe6\'\xca\xc8\xd2\xca\xce\xe3\xbb\xef\x00\xdf\xc2-\xfc\xdc\xd1\xf6\xcd\xb5\x0b\x90}y\xbd=\xcevZ\xd8e\xdb\xce99\'\xb4\'\xea\xf0o\x1a\x11`\x06\xfe\x19\xde\x11%\xca\xe0\xcff\xb0k\x8f\x9d\xf3\xbc\xa9\xfe\x15*\xcb2E\x8c\xa0Z_\xa46\x9d\x92U\x9bw\xb9\xb5n\x97\xb7r\xf6\xb7\x90\x1cC\x1b\xeb6\xfbY4\xf3\xca\xdd\xafo\x0e\x8f\x8e\xb8\xa7\xd92\xc3\x95=\xa8\xff;d\x04\xf0qEz\x90s\x9aG",e(\xbd\xec\xb1\x87\xe5U~\xeav\xd6;Yf)A\xa9\xef\x19iW\xca\xa1Y\xe6\\\xe3\xd1\x1e\x9ag/\xe3\xad\xbb\xb3F\xdfEz\xe9\xcb\x91\xc7]\xa5O\xeen\xd2\x17\x86*\x97\xb2\x0b\xef\xdc9t\xd3\xfbh\x8c\xfc\xe55\x8b>\xd1\'n\xdf\x92x\xe2\x86\xbdP\xb5\xe2\x03\xcb\x8e_\xeaF\xc2\xb0T\xec\xbez\xc9\xb5a\x15)\xfe\xb56\x1b\x82;\x83\xee\x84\xe2\x8b\r\xfcg\xd8\xc66[\xd5\xa6\x18\xcb\xc0K\xf2\x8d:|\x83\xf9k\xcc\x0c\xd2?\xf9f\x1d\xbe\xc9\xfc5f\x86.\xc9\x1f42x\xc8U!W\xf3\xa6NACCCCCCCCC\xa3\x1e\x84:-\x98\xea_|T\x9d\x0e\xe2\xea\xbb\xce*\xb5\xaa\xfeL\xf2\xdf\xe2(&\xe9\x9a\xa2s\xe6A\x14\xa8/b\xba\xa9\xfc\xd9\x8a\xa8\x08\x9f%\x1a\xf4\t\xbf\x17J\x1c\xa7\xd9\x8b\x18\xc7(\xc71\xdet\xfe\xd2\xe9N\xd4\xfe\x9e\x86\x1d\xad\xdf\xb7\x85\x9a\x9d\xbf\xdaL\x9c\x7fx\xfe\x1f\xf5\x81\xcaV'

    with make_file(data, '.xlsx', decompress=True) as fname:
        d = df.load_data(fname)

    assert_array_equal(d['x'], [1, 2, 3])
    assert_array_equal(d['y'], [2, 3, 4])

    assert d.label.endswith(':Sheet1')


@requires_xlrd
def test_excel_multiple():

    datasets = df.load_data(os.path.join(DATA, 'simple_data.xlsx'))

    assert_array_equal(datasets[0]['a'], [1, 2, 3, 4, 5])
    assert_array_equal(datasets[0]['b'], ['a', 'c', 'd', 'e', 'f'])

    assert datasets[0].label == 'simple_data:Data1'

    assert_array_equal(datasets[1]['1'], [2, 3, 4, 5])
    assert_array_equal(datasets[1]['a'], ['b', 'c', 'd', 'e'])

    assert datasets[1].label == 'simple_data:Data2'


@requires_xlrd
def test_excel_single():

    from ..excel import panda_read_excel

    d = panda_read_excel(os.path.join(DATA, 'simple_data.xlsx'), sheet='Data2')[0]

    assert_array_equal(d['1'], [2, 3, 4, 5])
    assert_array_equal(d['a'], ['b', 'c', 'd', 'e'])

    assert d.label == 'simple_data:Data2'
