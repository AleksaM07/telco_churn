import os
import pytest
import pandas as pd
from etl.export_parquet import export_to_parquet
from etl.load_raw import load_csv_to_db

@pytest.fixture(scope='module')
def setup_db_and_export(tmp_path):
    # load raw and export
    load_csv_to_db()
    os.environ['PARQUET_PATH'] = str(tmp_path / 'test.parquet')
    export_to_parquet()
    return tmp_path / 'test.parquet'


def test_parquet_exists(setup_db_and_export):
    parquet = setup_db_and_export
    assert parquet.exists()
    df = pd.read_parquet(parquet)
    assert not df.empty
    assert 'customerID' in df.columns