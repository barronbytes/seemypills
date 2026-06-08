import pytest

from app.features.upload_bottle.models import Bottle


def test_bottle_model_accepts_valid_attributes_succeeds():
    """
    Check that Bottle accepts valid mapped column values
    and stores them as instance attributes.
    """
    bottle = Bottle(brand_name="Tylenol", ocr_raw_text="TYLENOL EXTRA STRENGTH 500MG")

    assert bottle.brand_name == "Tylenol"
    assert bottle.ocr_raw_text == "TYLENOL EXTRA STRENGTH 500MG"


def test_bottle_model_rejects_unmapped_keyword_argument_fails():
    """
    Check that Bottle raises TypeError when constructed with a keyword
    argument that does not correspond to a mapped column.
    """
    with pytest.raises(TypeError):
        Bottle(brand_name="Tylenol", dosage_strength="500mg")
