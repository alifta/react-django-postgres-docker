from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_world(request):
    """A simple view that returns a greeting."""
    return Response({"message": f"Hello, world: {datetime.now().isoformat()}"})
