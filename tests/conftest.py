import pytest
import pickle
from src.preprocessing.audio_preprocessor import MusicMetadataProcessor

# Sample data for testing
SAMPLE_METADATA = {
    'name': 'sample_violin',
    'channels': 2,
    'filesize': 12345,
    'bitrate': 320,
    'bitdepth': 16,
    'duration': 60,
    'samplerate': 44100
}

LOG_FILE = './project_logs/test_audio_preprocessing.log'
INSTRUMENT_LIST = [
    'Clarinet', 'Sax Alto', 'Flute', 'Violin', 'Trumpet', 'Cello', 'Sax Tenor',
    'Piccolo', 'Sax Soprano', 'Sax Baritone', 'Oboe', 'Double Bass'
]

@pytest.fixture
def setup_test_environment(tmp_path):
    """
    Fixture to set up the test environment by creating sample directories and files.
    """
    sample_dir = tmp_path / "freesound/sample_dir"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a sample wav file
    sample_wav = sample_dir / "sample.wav"
    sample_wav.touch()
    
    # Create a sample metadata file
    with open(sample_dir / "sound_metadata.pkl", "wb") as f:
        pickle.dump(SAMPLE_METADATA, f)
    
    return sample_dir

@pytest.fixture
def processor():
    """
    Fixture to create a MusicMetadataProcessor instance.
    """
    return MusicMetadataProcessor(INSTRUMENT_LIST, LOG_FILE)

@pytest.fixture()
def test_file():
    return './tests/overall quality of single note - trumpet - D#5.wav'