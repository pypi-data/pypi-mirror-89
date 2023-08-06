import sys
import pathlib
working_directory = pathlib.Path().absolute()
script_directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(working_directory))
import unittest


from pyadlml.dataset import set_data_home, load_act_assist
from pyadlml.dataset import ACTIVITY, DEVICE, END_TIME, START_TIME, VAL, \
    TIME

class TestEmptyDataset(unittest.TestCase):
    def setUp(self):
        dataset_dir = str(script_directory) + '/datasets/empty_dataset'
        self.data = load_act_assist(dataset_dir, subjects=['one', 'two'])

    def test_activities_loaded(self):
        df_one = self.data.df_activities['one']['df_activities'] 
        df_two = self.data.df_activities['two']['df_activities']
        activity_header = [START_TIME, END_TIME, ACTIVITY]

        assert (df_one.columns == activity_header).any()
        assert (df_two.columns == activity_header).any()
        assert len(df_one) == 0
        assert len(df_two) == 0

    def test_devices_loaded(self):
        df_devices = self.data.df_devices
        device_header = [TIME, DEVICE, VAL]
        print(df_devices.columns)

        assert (df_devices.columns == device_header).all()
        assert len(df_devices) == 0


if __name__ == '__main__':
    unittest.main()