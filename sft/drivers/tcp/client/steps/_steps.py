from .raw_data_reader import raw_data_reader
from .raw_data_normalizer import raw_data_normalizer


steps = {
    "raw_data_reader": (raw_data_reader, ),
    "raw_data_normalizer": (raw_data_normalizer, ),
}
