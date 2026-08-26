def test_package_exports_client() -> None:
    from volcano_sdk import VolcanoClient

    assert VolcanoClient.__name__ == "VolcanoClient"
