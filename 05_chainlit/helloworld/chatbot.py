import chainlit as cl 

@cl.on_message
async def main(message: cl.Message):
    # our logics will goes here
    
    await cl.Message(content=f"Received Message: {message.content}").send()
