from django.shortcuts import render

# Create your views here.
from .apps import ApiConfig
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import os
import requests
from tempfile import NamedTemporaryFile

@csrf_exempt
def index(request):
    if request.method == "POST":
        image = request.POST.get("image")
        print(f"Received image URL: {image}")  # For debugging

        if not image:
            return HttpResponseNotFound("Image URL not provided!!")

        try:
            # Fetch the image from the URL
            response = requests.get(image)
            response.raise_for_status()

            # Write the image data to a temporary file
            with NamedTemporaryFile(delete=False) as tmp:
                tmp.write(response.content)

            # Make predictions using your model
            predictions = ApiConfig.trained_model.predict(tmp.name).json()['predictions'][0]['predicted_classes']

            # Clean up the temporary file
            os.remove(tmp.name)

            return JsonResponse({"prediction": predictions})
        except requests.exceptions.RequestException as e:
            return HttpResponseNotFound(f"Failed to fetch image from URL: {str(e)}")
        except Exception as e:
            return HttpResponseNotFound(f"Error processing the image: {str(e)}")
    return HttpResponseNotFound("Only POST method is available")
