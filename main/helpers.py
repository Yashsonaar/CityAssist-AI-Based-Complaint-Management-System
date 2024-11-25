import pickle
from django.http import JsonResponse
from .models import Complaint 

with open("path/to/tfidf_vectorizer.pkl", "rb") as vec_file:
    tfidf_vectorizer = pickle.load(vec_file)

with open("path/to/xyz_complaint_classification_model.pkl", "rb") as model_file:
    classification_model = pickle.load(model_file)

def classify_latest_complaint(request):
    """
    View to fetch the latest complaint description, classify it using the pre-trained model, 
    and return the predicted category.
    """
    latest_complaint = Complaint.objects.latest('id') 
    description = latest_complaint.desc

    description_tfidf = tfidf_vectorizer.transform([description])
    predicted_category = classification_model.predict(description_tfidf)[0]

    latest_complaint.category = predicted_category
    latest_complaint.save()

    return JsonResponse({
        "description": description,
        "predicted_category": predicted_category,
    })
