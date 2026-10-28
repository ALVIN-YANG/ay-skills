def act(request):
    if request["intent"] == "lookup":
        return "read"
    if request["intent"] == "set_address":
        return "write"
    return "none"
