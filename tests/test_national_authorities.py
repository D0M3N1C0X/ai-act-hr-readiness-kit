"""The national authorities table: every country, a status each, a source for every verified row."""
import pandas as pd

from config import COUNTRIES, DATA


def test_every_country_once_with_a_known_status():
    na = pd.read_csv(DATA / "national_authorities.csv", keep_default_na=False)
    assert sorted(na["country"]) == sorted(COUNTRIES)
    known = {"Verified", "Verified (AESIA statute)", "Secondary", "Not checked"}
    assert set(na["status"].str.split(" ·").str[0]) <= known


def test_verified_rows_name_their_source_and_act():
    na = pd.read_csv(DATA / "national_authorities.csv", keep_default_na=False)
    v = na[na["status"].str.startswith("Verified")]
    assert (v["source"] != "").all() and (v["designated_by"] != "").all()
    assert set(v["country"]) >= {"PL", "DE", "IE"}
