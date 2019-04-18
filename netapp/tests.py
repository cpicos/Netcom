from django.test import Client
from django.contrib.auth.models import User, Permission

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from .models import Client as modelClient
from .serializers import ClientSerializer

# Create your tests here.


# initialize the APIClient app
client = Client()

class ClientTest(APITestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        self.client.login(username=self.username, password=self.password)
        self.obj1 = modelClient.objects.create(name='TDD', dba='TDD', rfc='TDD', address='TDD', postal_code='TDD', created_by=self.user)
        self.obj2 = modelClient.objects.create(name='TDD2', dba='TDD2', rfc='TDD2', address='TDD2', postal_code='TDD2', created_by=self.user)

        all_permissions = Permission.objects.filter(content_type__app_label='netapp', content_type__model='client')
        for perm in all_permissions:
            self.user.user_permissions.add(perm)

        # FOR POSTS            
        self.valid_payload = {
            'name': 'TEST',
            'dba': 'TEST',
            'rfc': 'TEST',
            'address': 'TEST',
            'postal_code': 'TEST',
            'created_by': self.user.pk
        }

        # FOR PATCH
        self.update_payload = {
            'name': 'NUEVO NOMBRE',
            'dba': 'TDD',
            'rfc': 'TDD',
            'address': 'TDD',
            'postal_code': 'TDD',
            'created_by': self.user.pk
        }

    def test_get_all(self):
        response = self.client.get('/api/clients/', format='json')
        clients = modelClient.objects.all()
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_get_single(self):
        response = self.client.get('/api/clients/{0}/'.format(self.obj1.pk), format='json')
        client_1 = modelClient.objects.get(pk=self.obj1.pk)
        serializer = ClientSerializer(client_1, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_post(self):
        response = self.client.post('/api/clients/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_delete(self):
        response = self.client.delete('/api/clients/{0}/'.format(self.obj1.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_patch(self):
        response = self.client.patch('/api/clients/{0}/'.format(self.obj1.pk), self.update_payload, format='json')
        client_1 = modelClient.objects.get(pk=self.obj1.pk)
        serializer = ClientSerializer(client_1, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)