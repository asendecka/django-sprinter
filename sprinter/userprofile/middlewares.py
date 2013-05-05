from sprinter.userprofile.models import Sprinter


class EnsureSprinterMiddleware(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            return
        try:
            request.user.sprinter
        except Sprinter.DoesNotExist:
            Sprinter.objects.create(user=request.user)
