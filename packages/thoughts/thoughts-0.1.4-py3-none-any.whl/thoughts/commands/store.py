from thoughts import context as ctx

def process(command, context):
    
    item_to_store = command["#store"]

    ctx.Context.store_item(context, command, item_to_store)
