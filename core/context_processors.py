from django.http import request

def whom_context_processor(request):
    try:
        whom = request.session['whom']
        if(whom=="STAFF"):
            try:
                role = request.session['role']
            except KeyError:
                role = "GUEST"           
            return {'whom': whom , 'role': role}
        if(whom=="ADMIN"):
            try:
                role = request.session['role']
                name = request.session['name']
            except KeyError:
                role = "GUEST"        
                name="Placement"
            return {'whom': whom , 'role': role , 'name':name}
    except KeyError:
        whom = 'GUEST'  # Default to 'GUEST'
    return {'whom': whom}