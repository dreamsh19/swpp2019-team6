import unittest
from django.test import TestCase, Client
from rest_framework import status
import json

from .models import Travel,TravelCommit, Tag

from django.test.client import MULTIPART_CONTENT
from io import BytesIO
from PIL import Image


class TagTestCase(TestCase):

    def get_token(self, client):
        response = client.post('/api/user/signup/', data = {
            "email": "test@test.com",
            "password": "test",
            "nickname": "test"
        })
        assert response.status_code == status.HTTP_201_CREATED, response.content

        response = client.post('/api/user/auth/', data = {
            "email": "test@test.com",
            "password": "test"
        })
        token_json = json.loads(response.content)
        token = token_json["token"]
        return token

    def test_add_tag(self):
        client = Client()
        token = self.get_token(client)

        response = client.post('/api/travel/tag/TEST/',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        long_tag = 'a'*100
        response = client.post('/api/travel/tag/{}/'.format(long_tag),
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post('/api/travel/tag/TEST/',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_tags(self):
        client = Client()
        token = self.get_token(client)

        response = client.post('/api/travel/tag/TEST1/',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post('/api/travel/tag/TEST2/',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post('/api/travel/tag/TEST3/',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post('/api/travel/tag/TEST4/',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get('/api/travel/tag/TEST/',
                              HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 4)

        long_tag = 'a'*100
        response = client.get('/api/travel/tag/{}/'.format(long_tag),
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RecommendTestCase(TestCase):

    def get_token(self, client):
        response = client.post('/api/user/signup/', data = {
            "email": "test@test.com",
            "password": "test",
            "nickname": "test"
        })
        assert response.status_code == status.HTTP_201_CREATED, response.content

        response = client.post('/api/user/auth/', data = {
            "email": "test@test.com",
            "password": "test"
        })
        token_json = json.loads(response.content)
        token = token_json["token"]
        return token

    def test_get_recommend(self):
        client = Client()
        token = self.get_token(client)

        tag='tag1'
        Tag.objects.create(word=tag)
        temp_embed_vector= [1 for i in range(512)]
        temp_data1 = {
            "fork_parent": "",
            "head": {
            "days": [
            {
            "blocks": [
            {
                "title": "manhattan",
                "description": "",
                "time": "9:0",
                "start_location": ".",
                "end_location": "",
                "block_type": "CUS",
                "modified": True,
                "parent_block": None
                }
            ],
                "title": "",
                "day": "2019-12-13",
                "modified": True,
                "parent_day": None
            }
            ],
                "block_dist": [0,1,2,3,4],
                "travel_embed_vector":temp_embed_vector,
                "tags" : [tag,],
                "title": "new york",
                "summary": "",
                "description": "",
                "start_date": "2019-12-13",
                "end_date": "2019-12-13",
            },
        }
        temp_data1_json=json.dumps(temp_data1)

        response = client.post('/api/travel/', data=temp_data1_json, content_type='application/json',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post('/api/travel/', data=temp_data1_json, content_type='application/json',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post('/api/travel/', data=temp_data1_json, content_type='application/json',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post('/api/travel/', data=temp_data1_json, content_type='application/json',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post('/api/travel/', data=temp_data1_json, content_type='application/json',
                               HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/travel/recommend/2/3/',
                              HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        response = client.get('/api/travel/recommend/10/',
                              HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        response = client.get('/api/travel/recommend/1/',
                              HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        response = client.get('/api/travel/recommend/1/3/',
                              HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        response = client.get('/api/travel/1/',
                              HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CommentTestCase(TestCase):

    def setUp(self):
        client = Client()
        response = client.post('/api/user/signup/', data = {
            "email": "test@test.io",
            "password": "test",
            "nickname": "test"
        })
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        token = self.login(client)
        Tag.objects.create(word='tag1')


        travel_data = {
                        "head": {
	                            "days": [
	                                        {
		                                        "id": 4,
       		                                    "blocks": [],
	                            	            "title": "",
		                                        "day": "2019-12-14",
		                                        "modified": True,
		                                        "parent_day": None
	                                        }
	                            ],
	                            "block_dist": [],
	                            "travel_embed_vector": [],
                            	"title": "title1",
	                            "summary": "",
	                            "description": "",
	                            "start_date": "2019-12-14",
	                            "end_date": "2019-12-14",
                                "tags": ["tag1"]
                        },
                        "fork_parent": None,
                        "is_public" : False,
        }
        response = client.post('/api/travel/',
                                travel_data,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def login(self,client):

        response = client.post('/api/user/auth/', data = {
            "email": "test@test.io",
            "password": "test"
        })
        token_json = json.loads(response.content)
        token = token_json["token"]
        return token

    def test_comment_normal(self):
        client = Client()
        token = self.login(client)

        initial_comment = 'comment1'

        response = client.get('/api/travel/1/comment/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        content = json.loads(response.content)

        self.assertEqual(len(content),0)

        response = client.post('/api/travel/1/comment/',
                                {"content": initial_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = client.get('/api/travel/1/comment/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(len(content),1)
        self.assertEqual(content[0]['content'], initial_comment)

        modified_comment = 'comment1_modified'
        response = client.put('/api/travel/1/comment/1/',
                                {"content": modified_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)



        response = client.get('/api/travel/1/comment/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(len(content),1)
        self.assertEqual(content[0]['content'], modified_comment)

        response = client.delete('/api/travel/1/comment/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = client.get('/api/travel/1/comment/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(len(content),0)

    def test_comment_get_error(self):
        client = Client()
        response = client.post('/api/user/signup/', data = {
            "email": "test2@test.io",
            "password": "test",
            "nickname": "test2"
        })
        response = client.post('/api/user/auth/', data = {
            "email": "test2@test.io",
            "password": "test"
        })
        token_json = json.loads(response.content)
        token = token_json["token"]


        response = client.get('/api/travel/2/comment/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_comment_error(self):
        client1 = Client()
        token1 = self.login(client1)
        client2 = Client()
        response = client2.post('/api/user/signup/', data = {
            "email": "test2@test.io",
            "password": "test",
            "nickname": "test2"
        })
        response = client2.post('/api/user/auth/', data = {
            "email": "test2@test.io",
            "password": "test"
        })
        token_json = json.loads(response.content)
        token2 = token_json["token"]


        initial_comment = 'comment1'
        modified_comment = 'comment_modified'
        response = client1.post('/api/travel/1/comment/',
                                {"content": initial_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = client2.post('/api/travel/2/comment/',
                                {"content": initial_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token2))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        # response = client2.post('/api/travel/1/comment/',
        #                         {"content": initial_comment},
        #                         content_type='application/json',
        #                         HTTP_AUTHORIZATION="JWT {}".format(token2))
        # self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        response = client1.post('/api/travel/1/comment/',
                                {"contents": initial_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


        response = client2.put('/api/travel/2/comment/1/',
                                {"content": modified_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token2))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client2.put('/api/travel/1/comment/1/',
                                {"content": modified_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token2))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        response = client1.put('/api/travel/1/comment/1/',
                                {"contents": modified_comment},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        response = client2.delete('/api/travel/2/comment/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token2))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client2.delete('/api/travel/1/comment/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token2))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class TravelTestCase(TestCase):

    def setUp(self):
        client = Client()
        token = self.signup_and_login('test0@test.io', 'test', 'test0')
        Tag.objects.create(word='tag1')
        travel_data = {
                        "head": {
	                            "days": [
	                                        {
		                                        "id": 4,
       		                                    "blocks": [],
	                            	            "title": "",
		                                        "day": "2019-12-14",
		                                        "modified": True,
		                                        "parent_day": None
	                                        }
	                            ],
	                            "block_dist": [],
	                            "travel_embed_vector": [],
                            	"title": "title1",
	                            "summary": "",
	                            "description": "",
	                            "start_date": "2019-12-14",
	                            "end_date": "2019-12-14",
                                "tags": ["tag1"],
                        },
                        "fork_parent": None,
                        "is_public" : False,
        }
        response = client.post('/api/travel/',
                                travel_data,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def signup_and_login(self, email, password, nickname, login_only=False):
        client = Client()
        if not login_only:
            response = client.post('/api/user/signup/', data = {
                "email": email,
                "password": password,
                "nickname": nickname
            })
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = client.post('/api/user/auth/', data = {
            "email": email,
            "password": password
        })
        token_json = json.loads(response.content)
        token = token_json["token"]
        return token



    def test_fork(self):
        client = Client()
        token = self.signup_and_login('test@test.io','test','test')
        
        response = client.post('/api/travel/2/fork/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.post('/api/travel/1/fork/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        TravelCommit.objects.filter(id=1).update(start_date="2019-12-14",end_date="2019-12-13")
        response = client.post('/api/travel/1/fork/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_view_like_update(self):
        client = Client()
        token = self.signup_and_login('test@test.io','test','test')
        response = client.put('/api/travel/view/2/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.put('/api/travel/view/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = client.put('/api/travel/like/2/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.put('/api/travel/like/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_travel_settings(self):
        client = Client()
        token = self.signup_and_login('test0@test.io','test','test0', True)
        

        token1=self.signup_and_login('test@test.io','test','test')
        
        response = client.put('/api/travel/settings/1/',
                                { 'added_collaborator' : 'test1'},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.put('/api/travel/settings/1/',
                                { 'added_collaborator' : 'test'},
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
                
        response = client.get('/api/travel/collaborator/2/',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        response = client.put('/api/travel/settings/1/',
                                { 'deleted_collaborator' : 3 },
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        
        response = client.put('/api/travel/settings/1/',
                                { 'deleted_collaborator' : 2 },
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_post_travelCommit(self):
        client = Client()
        token = self.signup_and_login('test0@test.io','test','test0',True)
        
        data = {
	            "days": [
	                        {
		                        "id": 4,
       		                    "blocks": [],
	                            "title": "",
		                        "day": "2019-12-14",
		                        "modified": True,
		                        "parent_day": None
	                        }
	            ],
	            "block_dist": [],
	            "travel_embed_vector": [],
                "title": "title1",
	            "summary": "",
	            "description": "",
	            "start_date": "2019-12-14",
	            "end_date": "2019-12-14",
                "tags": ["tag1"]
        }

        
        response = client.post('/api/travel/2/travelCommit/', data,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.post('/api/travel/1/travelCommit/', data,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        response = client.get('/api/travel/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        response = client.get('/api/travel/user/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_photo(self):
        client = Client()

        token = self.signup_and_login('test0@test.io','test','test0',True)
        def get_temp_image_file():
            file = BytesIO()
            image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
            image.save(file, 'png')
            file.name = 'test.png'
            file.seek(0)
            return file 

        img = get_temp_image_file()
        data = {'photo' : img}
        response=client.put('/api/travel/travelCommit/2/photo/',
                                content_type=MULTIPART_CONTENT,
                                HTTP_AUTHORIZATION="JWT {}".format(token),
                                data=data)

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response=client.put('/api/travel/travelCommit/1/photo/',
                                content_type=MULTIPART_CONTENT,
                                HTTP_AUTHORIZATION="JWT {}".format(token),
                                data=data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_merge(self):
        client = Client()

        token = self.signup_and_login('test0@test.io','test','test0',True)
        token1= self.signup_and_login('test@test.io','test','test')

        response=client.put('/api/travel/travelCommit/2/merge/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response=client.put('/api/travel/travelCommit/1/merge/',
                                HTTP_AUTHORIZATION="JWT {}".format(token1))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        response=client.put('/api/travel/travelCommit/1/merge/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        travelCommit_data = {
                                "days": [
	                                        {
		                                        "id": 4,
       		                                    "blocks": [],
	                            	            "title": "",
		                                        "day": "2019-12-14",
		                                        "modified": True,
		                                        "parent_day": None
	                                        }
	                            ],
                                "block_dist": [],
                                "travel_embed_vector": [],
                                "title": "title",
                                "summary": "",
                                "description": "",
                                "start_date": "2019-12-14",
                                "end_date": "2019-12-14",
                                "tags": ["tag1"],
                            }
        response=client.post('/api/travel/1/travelCommit/', travelCommit_data,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        TravelCommit.objects.filter(id=2).update(travel_id=None)
        response=client.put('/api/travel/travelCommit/2/merge/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_search(self):
        client = Client()
        token= self.signup_and_login('test@test.io','test','test')

        response=client.get('/api/travel/search/tag1/',
                            HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_post_travel_error(self):
        client = Client()
        token = self.signup_and_login('test@test.io', 'test', 'test')
        travel_data_no_head = {
                        "fork_parent": None,
                        "is_public" : False,
        }
        response = client.post('/api/travel/',
                                travel_data_no_head,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        travel_data_no_title = {
                        "head": {
	                            "days": [
	                                        {
		                                        "id": 4,
       		                                    "blocks": [],
	                            	            "title": "",
		                                        "day": "2019-12-14",
		                                        "modified": True,
		                                        "parent_day": None
	                                        }
	                            ],
	                            "block_dist": [],
	                            "travel_embed_vector": [],
	                            "summary": "",
	                            "description": "",
	                            "start_date": "2019-12-14",
	                            "end_date": "2019-12-14",
                                "tags": ["tag1"],
                        },
                        "fork_parent": None,
                        "is_public" : False,
        }

        response = client.post('/api/travel/',
                                travel_data_no_title,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
        travelCommit_data_no_title = {
	                            "days": [
	                                        {
		                                        "id": 4,
       		                                    "blocks": [],
	                            	            "title": "",
		                                        "day": "2019-12-14",
		                                        "modified": True,
		                                        "parent_day": None
	                                        }
	                            ],
	                            "block_dist": [],
	                            "travel_embed_vector": [],
	                            "summary": "",
	                            "description": "",
	                            "start_date": "2019-12-14",
	                            "end_date": "2019-12-14",
                                "tags": ["tag1"],
                        }
        
        response = client.post('/api/travel/1/travelCommit/',
                                travelCommit_data_no_title,
                                content_type='application/json',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
                  
        

    def test_travel_id(self):
        client = Client()
        token = self.signup_and_login('test@test.io', 'test', 'test')
        
        response = client.get('/api/travel/2/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.get('/api/travel/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = client.delete('/api/travel/2/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        response = client.delete('/api/travel/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_travel_recent_n_popular(self):
        client = Client()
        token = self.signup_and_login('test@test.io', 'test', 'test')
        response = client.get('/api/travel/recent/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = client.get('/api/travel/popular/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_user_travel_list(self):
        client = Client()
        token = self.signup_and_login('test@test.io', 'test', 'test')
        response = client.get('/api/travel/user/1/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = client.get('/api/travel/user/2/',
                                HTTP_AUTHORIZATION="JWT {}".format(token))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

