from volcano_sdk import VolcanoClient


def test_package_exports_client() -> None:
    assert VolcanoClient.__name__ == "VolcanoClient"
