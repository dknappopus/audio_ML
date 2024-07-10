#!/usr/bin/env python
"""
This script creates the dataframe containing music file metadata.
"""

import os
import logging
import glob
import pickle
import pandas as pd


class MusicMetadataProcessor:
    """
    A class to process music file metadata and create a pandas DataFrame.

    Attributes:
        instrument_list (list): List of valid instrument names.
        logger (logging.Logger): Logger for the class.
    """
    def __init__(self,
                 instrument_list,
                 log_file='./project_logs/audio_preprocessing.log'):
        """
        Initializes the MusicMetadataProcessor with an instrument list and sets
        up logging.

        Args:
            instrument_list (list): List of valid instrument names.
            log_file (str): Path to the log file.
        """
        self.instrument_list = instrument_list
        self.setup_logger(log_file)

    def setup_logger(self, log_file):
        """
        Sets up the logger for the class.

        Args:
            log_file (str): Path to the log file.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('time:%(asctime)s,name:,%(name)s,levelname:%(levelname)s,message:%(message)s')

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def check_dict(self, py_dict: dict, dict_key: str) -> str:
        """
        Checks if a dictionary contains a key and returns the value or an empty string.

        Args:
            py_dict (dict): A Python dictionary.
            dict_key (str): A string indicating the key to be checked.

        Returns:
            str: The value of the dictionary for the key if it exists, otherwise returns an empty string.
        """
        return py_dict.get(dict_key, '')

    def find_matching_strings(self, string_list: list, target_string: str) -> list:
        """
        Checks if a string contains a target.

        Args:
            string_list (list): List of strings to check against the target.
            target_string (str): The string that will be checked against the list.

        Returns:
            list: List of matching strings.
        """
        target_string_l = target_string.lower()
        return [s.lower() for s in string_list if s.lower() in target_string_l]

    def check_wav_files(self, wav_directory: str) -> bool:
        """
        Checks if there are any .wav files in the given directory and its subdirectories.

        Args:
            wav_directory (str): The path to the directory to check.

        Returns:
            bool: True if there are .wav files in the directory or any of its subdirectories, False otherwise.

        Raises:
            ValueError: If the path is not a valid directory.
        """
        if not os.path.isdir(wav_directory):
            raise ValueError(f"The path {wav_directory} is not a valid directory.")
        for _, _, wav_files in os.walk(wav_directory):
            for file in wav_files:
                if file.endswith('.wav'):
                    return True
        return False

    def get_wav_files(self, wav_file_directory: str) -> str:
        """
        Gets the .wav files in a directory.

        Args:
            wav_file_directory (str): The path to the directory.

        Returns:
            str: The path to the .wav file if there is exactly one .wav file, otherwise None.
        """
        wav_files = glob.glob(os.path.join(wav_file_directory, '**', '*.wav'), recursive=True)
        return wav_files[0] if len(wav_files) == 1 else None

    def check_metadata(self, file_path: str) -> bool:
        """
        Checks if there is a sound_metadata.pkl file in the directory.

        Args:
            file_path (str): The path to the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.isfile(file_path)

    def create_music_record(self, dir_path: str) -> dict:
        """
        Creates a record for a DataFrame from a file path.

        Args:
            dir_path (str): String containing the freesound file path.

        Returns:
            dict: A dictionary containing file information or None if the directory does not have the necessary files.
        """
        if not self.check_wav_files(dir_path):
            self.logger.warning("No wav files found in %s", dir_path)
            return None

        metadata_file = os.path.join(dir_path, 'sound_metadata.pkl')
        if not self.check_metadata(metadata_file):
            self.logger.warning("No metadata file found in %s", dir_path)
            return None

        wav_file = self.get_wav_files(dir_path)
        if wav_file is None:
            self.logger.warning("Multiple or no wav files found in %s", dir_path)
            return None

        with open(metadata_file, 'rb') as file:
            sound_metadata = pickle.load(file)

        sound_name = sound_metadata.get('name', '')
        found_instruments = self.find_matching_strings(self.instrument_list, sound_name)
        sound_instr = found_instruments[0] if len(found_instruments) == 1 else ''

        music_record = {
            "relative_path": wav_file,
            "channels": self.check_dict(sound_metadata, "channels"),
            "filesize": self.check_dict(sound_metadata, "filesize"),
            "bitrate": self.check_dict(sound_metadata, "bitrate"),
            "bitdepth": self.check_dict(sound_metadata, "bitdepth"),
            "duration": self.check_dict(sound_metadata, "duration"),
            "samplerate": self.check_dict(sound_metadata, "samplerate"),
            "instrument_name": sound_instr
        }
        return music_record

    def create_music_set(self, dir_list: list) -> pd.DataFrame:
        """
        Creates a DataFrame containing information about music files.

        Args:
            dir_list (list): List of directories containing audio files and metadata.

        Returns:
            pd.DataFrame: DataFrame with music file information.
        """
        music_list = [self.create_music_record(dir_path) for dir_path in dir_list]
        music_fltrd = [i for i in music_list if i is not None]
        return pd.DataFrame(music_fltrd)

    def clean_music_df(self, music_file_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans music DataFrame by removing records where the target is missing.

        Args:
            music_file_df (pd.DataFrame): Initial DataFrame containing file info.

        Returns:
            pd.DataFrame: Processed DataFrame with no blank instrument names.
        """
        missing_recs = music_file_df.loc[music_file_df['instrument_name'] == '']
        n_missing = missing_recs.shape[0]
        pct_missing = round(100 * n_missing / music_file_df.shape[0], 2)
        self.logger.info("Records missing target variable: %s. Removing %s percent of records from our data", n_missing, pct_missing)
        return music_file_df.loc[music_file_df['instrument_name'] != '']

    def save_music_df(self, music_df_processed: pd.DataFrame, output_dir: str) -> None:
        """
        Outputs the processed music DataFrame containing music info.

        Args:
            music_df_processed (pd.DataFrame): The DataFrame to be saved.

        Raises:
            ValueError: If the DataFrame is empty.
            OSError: If the directory does not exist.
        """
        if music_df_processed.empty:
            raise ValueError("DataFrame contains no records!")

        if not os.path.isdir(output_dir):
            raise OSError(f"The path {output_dir} is not a valid directory.")

        filename = 'music_info_df.pkl'
        filepath = os.path.join(output_dir, filename)
        music_df_processed.to_pickle(filepath)
        self.logger.info('Successfully saved music dataframe')

    def process(self, root_dir, output_dir):
        """
        Main processing function to create, clean, and save the music DataFrame.

        Args:
            root_dir (str): The root directory containing the freesound files.
            output_dir (str): The directory to save the processed DataFrame.
        """
        fs_dirs = [os.path.join(root, directory) for root, dirs, _ in os.walk(root_dir) for directory in dirs]
        music_file_df = self.create_music_set(fs_dirs)
        music_file_df_clean = self.clean_music_df(music_file_df)
        self.save_music_df(music_file_df_clean, output_dir)


if __name__ == "__main__":
    INSTRUMENT_LIST = [
        'Clarinet', 'Sax Alto', 'Flute', 'Violin', 'Trumpet', 'Cello', 'Sax Tenor',
        'Piccolo', 'Sax Soprano', 'Sax Baritone', 'Oboe', 'Double Bass'
    ]
    processor = MusicMetadataProcessor(INSTRUMENT_LIST)
    processor.process('./freesound', './data/interim')
