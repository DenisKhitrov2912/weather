import unittest
from unittest.mock import patch, MagicMock

import requests
from django.test import RequestFactory, TestCase
from .views import weather_view, get_weather_data


class WeatherViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('weather.views.get_weather_data')
    def test_weather_view_post_valid_city(self, mock_get_weather_data):
        mock_get_weather_data.return_value = {
            'current_condition': [{
                'temp_C': '25',
                'weatherDesc': [{'value': 'Sunny'}]
            }]
        }
        request = self.factory.post('/weather/', data={'city': 'Tokyo'})
        response = weather_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tokyo', response.content.decode('utf-8'))
        self.assertIn('25', response.content.decode('utf-8'))
        self.assertIn('Sunny', response.content.decode('utf-8'))

    @patch('weather.views.get_weather_data')
    def test_weather_view_post_invalid_city(self, mock_get_weather_data):
        mock_get_weather_data.return_value = None
        request = self.factory.post('/weather/', data={'city': 'InvalidCity'})
        response = weather_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Город не найден.', response.content.decode('utf-8'))

    def test_weather_view_get(self):
        request = self.factory.get('/weather/')
        response = weather_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<form', response.content.decode('utf-8'))


class GetWeatherDataTests(TestCase):

    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = \
            {'current_condition': [{'temp_C': '25',
                                    'weatherDesc': [{'value': 'Sunny'}]}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        data = get_weather_data('Tokyo')
        self.assertIsNotNone(data)
        self.assertIn('current_condition', data)

    @patch('requests.get')
    def test_get_weather_data_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException
        data = get_weather_data('InvalidCity')
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
