import socket

from django.contrib.auth.models import User
from django.conf import settings

from radius_eap_mschapv2 import RADIUS


class RADIUSEAPMSCHAPv2Backend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                for radius_host in settings.RADIUS_HOSTS:
                    try:
                        radius = RADIUS(radius_host,
                                        settings.RADIUS_SECRET,
                                        settings.RADIUS_NAS_IP,
                                        settings.RADIUS_NAS_ID)

                        ret = radius.is_credential_valid(username, password)

                        if ret:
                            return user
                        else:
                            return None

                    except (ValueError, socket.error):
                        pass
        except User.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
