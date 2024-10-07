from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Check if there is an 'ErrorDetail' in the response data
        if isinstance(data, dict) and 'ErrorDetail' in str(data):
            # Wrap the errors in a JSON object with 'errors' as the key
            response = json.dumps({'errors': data})
        else:
            # Return the data as-is if no errors are found
            response = json.dumps(data)

        # Return the JSON response
        return response
