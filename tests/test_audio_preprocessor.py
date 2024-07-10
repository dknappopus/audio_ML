import os
import pandas as pd
import pytest
import pickle
from src.preprocessing.audio_preprocessor import MusicMetadataProcessor



def test_check_dict(processor):
    """
    Test the check_dict method.
    """
    py_dict = {'key1': 'value1', 'key2': 'value2'}
    assert processor.check_dict(py_dict, 'key1') == 'value1'
    assert processor.check_dict(py_dict, 'key3') == ''

def test_find_matching_strings(processor):
    """
    Test the find_matching_strings method.
    """
    string_list = ['Violin', 'Flute', 'Cello']
    target_string = 'Sample Violin Track'
    result = processor.find_matching_strings(string_list, target_string)
    assert result == ['violin']

def test_check_wav_files(processor, setup_test_environment):
    """
    Test the check_wav_files method.
    """
    assert processor.check_wav_files(setup_test_environment) is True
    # assert processor.check_wav_files('./invalid_directory') is False

def test_get_wav_files(processor, setup_test_environment):
    """
    Test the get_wav_files method.
    """
    result = processor.get_wav_files(setup_test_environment)
    assert result.endswith('sample.wav')

def test_check_metadata(processor, setup_test_environment):
    """
    Test the check_metadata method.
    """
    metadata_file = setup_test_environment / "sound_metadata.pkl"
    assert processor.check_metadata(metadata_file) is True
    assert processor.check_metadata('./invalid_path/sound_metadata.pkl') is False

def test_create_music_record(processor, setup_test_environment):
    """
    Test the create_music_record method.
    """
    result = processor.create_music_record(setup_test_environment)
    assert result is not None
    assert result['relative_path'].endswith('sample.wav')
    assert result['instrument_name'] == 'violin'

def test_create_music_set(processor, setup_test_environment):
    """
    Test the create_music_set method.
    """
    dir_list = [str(setup_test_environment)]
    df = processor.create_music_set(dir_list)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df.iloc[0]['instrument_name'] == 'violin'

def test_clean_music_df(processor):
    """
    Test the clean_music_df method.
    """
    data = {
        'relative_path': ['path1', 'path2'],
        'instrument_name': ['violin', '']
    }
    music_df = pd.DataFrame(data)
    cleaned_df = processor.clean_music_df(music_df)
    assert cleaned_df.shape[0] == 1
    assert cleaned_df.iloc[0]['instrument_name'] == 'violin'

def test_save_music_df(processor, tmp_path):
    """
    Test the save_music_df method.
    """
    data = {
        'relative_path': ['path1'],
        'instrument_name': ['violin']
    }
    music_df = pd.DataFrame(data)
    output_dir = tmp_path / "data/interim"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor.save_music_df(music_df, output_dir)
    
    saved_file = output_dir / 'music_info_df.pkl'
    assert saved_file.exists()

def test_process_integration(processor, setup_test_environment, tmp_path):
    """
    Integration test for the entire processing pipeline.
    """
    output_dir = tmp_path / "data/interim"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor.process(setup_test_environment.parent.parent, output_dir)
    
    saved_file = output_dir / 'music_info_df.pkl'
    assert saved_file.exists()
    
    df = pd.read_pickle(saved_file)
    assert df.shape[0] == 1
    assert df.iloc[0]['instrument_name'] == 'violin'