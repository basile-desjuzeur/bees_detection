import os
import pandas as pd
import dask.dataframe as dd
import shutil


def part_to_csv():
    # set directory path
    directory_path = "/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/inat_12_04/observations_research_quality.csv"

    print("directory_path: ", directory_path)

    # create directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # get list of all .part files in directory
    part_files = os.listdir(directory_path)
    part_files = [os.path.join(directory_path, file) for file in part_files]

    # ouptut file path
    output_file = '/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/inat_12_04/observations_research_quality_file.csv'

    if os.path.exists(output_file):
        os.remove(output_file)
    



    # read each .part file and write to output file

    for file in part_files:

        # read the .part file
        df = pd.read_csv(file, sep=',', low_memory=False, header=None,
dtype = {
    'observation_uuid': 'object',
    'observer_id': 'Int64',
    'latitude': 'float64',
    'longitude': 'float64',
    'positional_accuracy': 'Int64',
    'taxon_id': 'Int64',
    'quality_grade': 'object',
    'observed_on': 'object'
})

        # write to output file
        df.to_csv(output_file, mode='a', header=False, index=False)

    return


def csv_to_hierarchical():

    csv_path = '/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/inat_12_04/observations.csv'
    output_file = '/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/inat_12_04/observations_research_quality.csv'

    # Load the data in a dask dataframe

    df = dd.read_csv(csv_path, sep='\t',low_memory = False, header=None,
dtype = {
    'observation_uuid': 'object',
    'observer_id': 'Int64',
    'latitude': 'float64',
    'longitude': 'float64',
    'positional_accuracy': 'Int64',
    'taxon_id': 'Int64',
    'quality_grade': 'object',
    'observed_on': 'object'
})

    
    # Rename the columns

    df.columns = ['observation_uuid','observer_id','latitude','longitude','positional_accuracy','taxon_id','quality_grade','observed_on']

    # Filter the data, taking only the observations with quality_grade = research

    df = df[df['quality_grade'] == 'research']

    

    # remove output file if it exists
    if os.path.exists(output_file):
        shutil.rmtree(output_file)

    

    # Save the data in a csv file
    df.to_csv(output_file, index=False, header=True, single_file=False)

    return

def test():


    output_file = '/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/inat_12_04/observations_research_quality_file.csv'

    # Load the data in a dask dataframe

    df = dd.read_csv(output_file, sep=',',low_memory = False, header=None,dtype = {
    'observation_uuid': 'object',
    'observer_id': 'Int64',
    'latitude': 'float64',
    'longitude': 'float64',
    'positional_accuracy': 'Int64',
    'taxon_id': 'Int64',
    'quality_grade': 'object',
    'observed_on': 'object'
})

    df.head().to_csv('/home/basile/Documents/projet_bees_detection_basile/data_bees_detection/inat_12_04/observations_research_quality_file_test.csv', index=False, header=None)
    print(df.shape)

test()