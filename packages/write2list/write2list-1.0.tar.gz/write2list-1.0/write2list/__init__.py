def create(dataTuple):
    try:
        response=[]
        for item in dataTuple:
            i=dataTuple.index(item)
            if i >= 0:
                response.extend(dataTuple[i])
        return response
    except Exception:
        return "Error: Cannot read the tuple. Please make sure you have entered the correct values."