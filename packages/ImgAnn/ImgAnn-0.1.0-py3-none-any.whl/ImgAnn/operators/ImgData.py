# data extract from image dataset.

import os
import random
import logging
import traceback
import pandas as pd

# create a logger
logging.basicConfig()
logger = logging.getLogger(__name__)

# set log Level
logger.setLevel(logging.INFO)

# define fileHandler and formatter
# file_handler = logging.FileHandler('../logs/ImgAnn/operators/log_ImgData.txt')
# formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
# file_handler.setFormatter(formatter)

# add file handler to logger
# logger.addHandler(file_handler)

""":cvar
image_df attributes:
    - image_id : int
    - image_name : str
    - folder : str
    - path : str (separated by / )
    - width : int
    - height : int
    - format : class [(default) RGB, GBR, SHA ]

"""


class ImgData:

    def __init__(self, root: str, dataset: dict):
        self.dataset = dataset
        self.root = root

    @classmethod
    def extract(cls, dataset_path: str):
        """
        :param: dataset_path: directory of the dataset.
        :return: ImgData instance
        Extract folder names, all the files in the dataset.pip
        """
        folders = ImgData.ext_folders(dataset_path)
        files = ImgData.ext_files(dataset_path)
        dataset = {"folders": folders, "files": files}

        folders = ImgData.ext_folders(dataset_path)
        if type(folders) == str:
            logger.error("you have entered a file directory. Enter Folder directory.")
        else:
            data_list = []
            if len(folders) == 1:
                files = ImgData.ext_files(os.path.abspath(dataset_path))
                if files:
                    data_list.extend(ImgData.list_creator(os.path.abspath(dataset_path), folders[0], files))
                else:
                    logger.error("Error: there are no files in given directory!")
            else:
                for folder in folders:
                    files = ImgData.ext_files(os.path.abspath(dataset_path)+"\\"+folder)
                    if files:
                        data_list.extend(ImgData.list_creator(os.path.abspath(dataset_path+"\\"+folder), folder, files))
                    else:
                        continue

            if data_list:
                data_df = pd.DataFrame.from_records(data_list, columns=['name', 'folder', 'path'])
            else:
                logger.error("there was some error, record tuples are empty.")
        return cls(root=dataset_path, dataset=data_df)

    @staticmethod
    def list_creator(root: str, folder: str, files: list):
        """

        :param root: absolute path for the folder
        :param folder: parent folder of a file
        :param files: all the files
        :return: [(name, folder, path), ..]
        """
        tol_list = []
        for file in files:
            tol_list.append((file, folder, root+"\\"+file))
        return tol_list

    @staticmethod
    def ext_folders(path):
        """
        :param: path: absolute or relative path
        :return: all the folder names in the given directory.
        """
        folders = []
        try:
            assert os.path.exists(path), "path does not exists"
            folders = [x[1] for x in os.walk(path) if x[1] != []]
            if not folders:
                if not [x for x in os.walk(path)]:
                    parent_path, file_name = os.path.split(path)
                    folders = os.path.basename(parent_path)
                else:
                    folders = [os.path.basename(path)]
            else:
                folders = folders[0]
        except Exception as error:
            logger.exception("There is no folder in given directory.")
        return folders

    @staticmethod
    def ext_files(path):
        """
        :param: path: absolute or relative path
        :return: list of files in the directory or file name
        Output all the files in the given directory.
        """
        format_list = ['png', 'jpg', 'jpeg']
        files = []
        try:
            assert os.path.exists(path), "path does not exists"
            files = [x[2] for x in os.walk(path) if x[2] != []]
            if not files:
                if not [x for x in os.walk(path)]:
                    parent_path, file_name = os.path.split(path)
                    files = file_name
                else:
                    files = None
            else:
                if len(files) == 1:
                    files = files[0]
        except Exception as error:
            logger.exception("Error : There are no files in the given directory")

        return files


    def sample_dataset(self, numOfSamples: int):
        """
        :param: numOfSample : number of sample images required to show.
        :return: Dataframe object from self.dataset with numOFSample records.
        """
        numOfrecords, _ = self.dataset.shape
        rnd_numbers = sorted(random.sample(range(0, numOfrecords), numOfSamples))
        sample_df = self.dataset.iloc[rnd_numbers,:]
        return sample_df
