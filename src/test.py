from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_calc_deposit_endpoint():
    test_cases = [
        (
            {"date": "01.01.2021", "periods": 7, "amount": 10000, "rate": 6},
            {
                "01.01.2021": 10050.0,
                "01.02.2021": 10100.25,
                "01.03.2021": 10150.75,
                "01.04.2021": 10201.51,
                "01.05.2021": 10252.51,
                "01.06.2021": 10303.78,
                "01.07.2021": 10355.29
            }
        ),
        (
            {"date": "01.01.2021", "periods": 7, "amount": 10000, "rate": 6},
            {
                "29.01.2024": 10050.0,
                "28.02.2024": 10100.25,
                "29.03.2024": 10150.75,
                "29.04.2024": 10201.51,
                "29.05.2024": 10252.51,
                "29.06.2024": 10303.78,
                "29.07.2024": 10355.29
            }
        ),
        (
            {"date": "31.01.2021", "periods": 7, "amount": 10000, "rate": 6},
            {
                "31.01.2021": 10050.0,
                "28.02.2021": 10100.25,
                "31.03.2021": 10150.75,
                "30.04.2021": 10201.51,
                "31.05.2021": 10252.51,
                "30.06.2021": 10303.78,
                "31.07.2021": 10355.29
            }
        ),
        (
            {"date": "22.01.2021", "periods": 7, "amount": 10000, "rate": 6},
            {
                "22.01.2021": 10050.0,
                "22.02.2021": 10100.25,
                "22.03.2021": 10150.75,
                "22.04.2021": 10201.51,
                "22.05.2021": 10252.51,
                "22.06.2021": 10303.78,
                "22.07.2021": 10355.29
            }
        )
    ]

    for data, expected_result in test_cases:
        response = client.post("/calculate", json=data)
        assert response.status_code == 200
        assert response.json() == expected_result
