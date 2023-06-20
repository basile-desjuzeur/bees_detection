import pandas as pd 
import argparse
import json 


argparser = argparse.ArgumentParser(description='Get all the labels of the dataset')

argparser.add_argument(
    '-c',
    '--conf',
    default='/workspaces/projet_bees_detection_basile/bees_detection/src/classification/config.json')



def _main_(args):
    """
    Rewrite the config file with the labels of the dataset
    
    :param args: arguments of the command line
        dataset csv file specified in the config file must be 
        # path/to/img # bbox coordinates # label # width # height
        with no header 

    :return: None

    """
    c = args.conf

    with open(c,'w+') as config_buffer:
        config = json.loads(config_buffer.read())

    dataset = pd.read_csv(config['data']['dataset_csv_file'])

    labels = dataset.iloc[:,-3].unique()

    config['model']['labels'] = labels.tolist()

    with open(c,'w') as config_buffer:
        json.dump(config, config_buffer)


if __name__ == '__main__':
    args = argparser.parse_args()
    _main_(args)


