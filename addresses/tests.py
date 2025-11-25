from rest_framework import status
from rest_framework.test import APITestCase
from .models import Address

class AddressBookAPITest(APITestCase):

    def setUp(self):
        # Create initial addresses
        self.address1 = Address.objects.create(label="Home", latitude=12.9716, longitude=77.5946)
        self.address2 = Address.objects.create(label="Office", latitude=13.0358, longitude=77.5970)

    def test_create_address(self):
        """Test creating a new address with valid coordinates"""
        data = {
            "label": "Gym",
            "latitude": 12.9850,
            "longitude": 77.6100
        }
        response = self.client.post('/api/addresses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 3)
        self.assertEqual(Address.objects.last().label, "Gym")

    def test_create_address_invalid_coordinates(self):
        """Test creating an address with invalid coordinates should fail"""
        data = {
            "label": "InvalidPlace",
            "latitude": 100.0,  # invalid latitude
            "longitude": 200.0  # invalid longitude
        }
        response = self.client.post('/api/addresses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_addresses(self):
        """Test listing all addresses"""
        response = self.client.get('/api/addresses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # two initial addresses

    def test_retrieve_address(self):
        """Test retrieving a single address by ID"""
        response = self.client.get(f'/api/addresses/{self.address1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], "Home")

    def test_update_address(self):
        """Test updating an existing address"""
        data = {"label": "Home Updated", "latitude": 12.9720, "longitude": 77.5950}
        response = self.client.put(f'/api/addresses/{self.address1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address1.refresh_from_db()
        self.assertEqual(self.address1.label, "Home Updated")
        self.assertEqual(self.address1.latitude, 12.9720)

    def test_delete_address(self):
        """Test deleting an address"""
        response = self.client.delete(f'/api/addresses/{self.address1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Address.objects.count(), 1)

    def test_nearby_addresses(self):
        """Test nearby addresses endpoint"""
        response = self.client.get('/api/addresses/nearby/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("nearby", response.data)
        self.assertEqual(len(response.data["nearby"]), 2)
