from timeside.server.tests.timeside_test_server import TimeSideTestServer
from timeside.server.models import *

class TestAnnotation(TimeSideTestServer):

    def obj_url(self,obj):
        return '/timeside/api/items/'+str(obj.uuid)+'/'

    def test_create_annotation_track(self):
        item=Item.objects.all()[0]
        user=User.objects.all()[0]
        data={
            "item": self.obj_url(item),
            "title": "test_create_annotation_track",
            "author": '/timeside/api/users/'+str(user.username)+'/',
            "is_public": False,
        }
        annotation_track=self.client.post('/timeside/api/annotation_tracks/',data)
        self.assertEqual(annotation_track.status_code,201)

        user = User.objects.create(username='usertest')
        self.client.force_authenticate(user)
        print(self.client.get('/timeside/api/annotation_tracks/').content)



    def test_check_privacy_of_annotation(self):
        user = User.objects.create(username='usertest')
        self.client.force_authenticate(user)
        print(User.objects.all())

        
