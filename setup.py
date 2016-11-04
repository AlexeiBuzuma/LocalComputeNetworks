import setuptools
from sft.constants import APP_DATA_DIR


setuptools.setup(
    setup_requires=["pbr"],
    pbr=True,
    data_files=[(APP_DATA_DIR, ['etc/sft/sft.conf']), ],
)
