# Django RADIUS EAP-MSCHAPv2 Authentication Backend

Based on https://github.com/mneitsabes/RADIUS-EAP-MSCHAPv2-Python-client.

# Usage

Add this to your ``settings.py`` :

<pre>
AUTHENTICATION_BACKENDS = [
    'django_radius_eap_mschapv2_authbackend.EAPMSCHAPv2RADIUSBackend.RADIUSEAPMSCHAPv2Backend',
]


RADIUS_HOSTS = ['ip_srv1', 'ip_srv2']
RADIUS_SECRET = '<secret>'
RADIUS_NAS_IP = '<NAS IP>'
RADIUS_NAS_ID = '<NAS IDENTIFIER>'</pre>

