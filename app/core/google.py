from google import genai

client_google = genai.Client(
    vertexai=True,
    project="learncloud-501101",
    location="asia-south1",
)