from twilio.twiml.messaging_response import MessagingResponse
from fastapi import APIRouter
from .controller import generate_answer

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


    print(f"Message from {sender}: {incoming_message}")

    if form.get("MessageType")=="text":
        reply = generate_answer(query)
    twiml = MessagingResponse()
    twiml.message(reply)

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