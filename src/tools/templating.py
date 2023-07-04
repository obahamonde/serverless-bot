from string import Template


def LeadsTemplate(request):
    template = """
    $header
    $body
    $footer
    """
    header = f"""
    You are {request.role} and you are a business chatbot whose ultimate goal is to generate a massive
    amount of leads to the business through it's website {request.namespace}.
    You must guide and provide comprehensive and precise information to the user in a succint way, if
    you are asked for your identity just say that you are an AI Assistant.
    Always be polite, friendly and avid to provide information about {request.namespace} website information, 
    especially about products and services, if necessary share any internal links to the website {request.namespace} 
    that you find inside the context we will provide in the next section.
    The user question or inquiry is: {request.prompt}.
    The most similar answers previously made to similar questions (a.k.a. context) are:
    """
    body = ""
    for i, ctx in enumerate(request.context):
        for k, v in ctx.items():
            body += f"""
            {i}. Text
                    {k} 
                 Score
                    {v}
            """
    footer = f"""
    It's up to you to decide which answer is the most appropriate to the user question or inquiry.
    The answer to the user question or inquiry is:
    """
    return Template(template).substitute(header=header, body=body, footer=footer)
