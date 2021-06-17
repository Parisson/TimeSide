from timeside.server.tests.timeside_test_server import TimeSideTestServer
from timeside.server.models import *

class TestAnnotation(TimeSideTestServer):

    def test_create_annotation_track(self):
        user = User.objects.all()[0]
        len_annotation_track = AnnotationTrack.objects.count()
        data = {
            "item": self.item_url, 
            "title": "test_create_annotation_track", 
            "author": '/timeside/api/users/' + str(user.username) + '/', 
            "is_public": False, 
        }
        annotation_track = self.client.post('/timeside/api/annotation_tracks/', data)
        self.assertEqual(annotation_track.status_code, 201)
        self.assertEqual(len_annotation_track + 1, AnnotationTrack.objects.count())

        data = {
            "item": self.item_url, 
            "title": "test_create_annotation_track_2", 
            "author": '/timeside/api/users/' + str(user.username) + '/', 
            "is_public": True, 
        }
        annotation_track_2 = self.client.post('/timeside/api/annotation_tracks/', data)
        self.assertEqual(annotation_track_2.status_code, 201)
        self.assertEqual(len_annotation_track + 2, AnnotationTrack.objects.count())

        list_annotation_track = self.client.get('/timeside/api/annotation_tracks/')
        self.assertEqual(list_annotation_track.status_code, 200)
        self.assertEqual(len(list_annotation_track.data), len_annotation_track + 2)

        #test_privacy_of_annotation

        user = User.objects.create(username = 'usertest')
        self.client.force_authenticate(user)
        list_annotation_track = self.client.get('/timeside/api/annotation_tracks/')
        self.assertEqual(list_annotation_track.status_code, 200)
        self.assertEqual(len(list_annotation_track.data), len_annotation_track + 1)

        
