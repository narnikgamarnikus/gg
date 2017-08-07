from channels import Group

def bet_connect(message):
    message.reply_channel.send({"accept": True})
    Group("bet").add(message.reply_channel)


def phone_numbers_disconnect(message):
    Group("phonenumbers").discard(message.reply_channel)