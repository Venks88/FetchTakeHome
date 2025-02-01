import pytest
import subprocess

class TestGeolocUtil:
    @pytest.mark.parametrize("locations, expected_output", [
        (["123, MI"], "Location: Škofljica"),
        (["12345", "02135", "10001"], "Location: Schenectady"),
        (["qweqeqeqwe,qweqweq"], "No data found for http://api.openweathermap.org/geo/1.0/direct?q=qweqeqeqwe"),
        (["Columbus, OH"], "Location: Columbus, Ohio"),
        (["Columbus, OH", "Chicago, IL"], "Location: Columbus, Ohio"),
        ([";;;;;"], "Location: Unknown, [{'cod': '400', 'message': 'wrong latitude'}]"),
        ([""], "Location: Unknown, [{'cod': '400', 'message': 'wrong latitude'}]"),
        (["123123123123"], "Location: Unknown, [{'cod': '400', 'message': 'wrong latitude'}]"),
        (["12312"], "Location: Unknown, [{'cod': '400', 'message': 'wrong latitude'}]"),
        (["90210"], "Location: Beverly Hills"),
        (["9021090210"], "Location: Unknown, [{'cod': '400', 'message': 'wrong latitude'}]"),
        (["9 0 2 1 0"], "Location: Beverly Hills"),
        (["<<9 0 2 1 0>>"], "Location: Beverly Hills"),
        (["Columbus, OH", "Chicago, IL", "12345", "02135", "10001", "123123123123"], "Location: Columbus, Ohio")
    ])
    def test_geoloc_output(self, locations, expected_output):
        # Construct command
        cmd = ["python", "./Utility/geoloc_util.py", "--locations"] + locations

        # Run script and capture stdout
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Assert script runs successfully
        assert result.returncode == 0, f"Script failed for input {locations}"

        # Validate expected output
        actual_output = result.stdout.strip().split("\n")  # Normalize output for comparison
        assert any(expected_output in line for line in actual_output), f"Expected 'Location: Škofljica' in output, but got {actual_output}"