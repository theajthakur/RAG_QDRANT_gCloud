from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import APIRouter
from .controller import generate_answer
from app.core.session_storage import storage

twilio_router=APIRouter()

@twilio_router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()

    incoming_message = form.get("Body")
    query={
        "user_name":form.get("ProfileName"),
        "query":incoming_message
    }
    sender = form.get("From")

    reply="Not supported!"

    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"Message from {sender}: {incoming_message}\n")
    print(f"Message from {sender}: {incoming_message}")

    if form.get("MessageType")=="text":
        reply = generate_answer(query=str(query["query"]), identifier=str(sender))

    twiml = MessagingResponse()
    twiml.message(reply)

    print(str(twiml))

    return Response(
        content=str(twiml),
        media_type="application/xml"
    )

@twilio_router.post("/webhook/whatsapp/status")
async def status(request: Request):
    form = await request.form()

    print(form["MessageSid"])
    print(form["MessageStatus"])

    return "OK"