import pytest
import pandas as pd
import numpy as np

from collections import namedtuple
from collections import OrderedDict

import pyactcv as cv

class TestActCV(object):

    def test_tuple_to_dict_general_output(self):
        Pandas = namedtuple('Pandas', [ 'Index', 
                                        'Sebastian', 
                                        'Tim', 
                                        'Alina', 
                                        'Max', 
                                        'Peter'])
        input_tuple = Pandas(0, 1, 2, 3, 4, 5)

        expected_output = OrderedDict([ ('Sebastian', 1), 
                                        ('Tim', 2), 
                                        ('Alina', 3), 
                                        ('Max', 4), 
                                        ('Peter', 5)])
        observed_output =  cv.ActCV.tuple_to_dict(self, input_tuple)

        assert observed_output == expected_output


    def test_tuple_to_dict_input(self):
        pass


    def test_convert_data_frame_general_output(self):
        input_data = {'col1': [1, np.nan, 3, 4], 
                      'col2': [5, 6, np.nan, 8], 
                      'col3': [9, 10, np.nan, 12], 
                      'col4': [13, 14, 15, np.nan]}
        input_frame = pd.DataFrame(data=input_data)

        expected_data = {'col1': [1.0, 0.0, 3.0, 4.0], 
                         'col2': [5.0, 6.0, 0.0, 8.0], 
                         'col3': [9.0, 10.0, 0.0, 12.0], 
                         'col4': [13.0, 14.0, 15.0, 0.0]}                        
        expected_frame = pd.DataFrame(data=expected_data)

        observed_frame =  cv.ActCV.convert_data_frame(self, input_frame)

        pd._testing.assert_frame_equal(observed_frame, expected_frame)
    

    def test_convert_data_frame_input(self):
        pass


    def test_set_states(self):
        pass


