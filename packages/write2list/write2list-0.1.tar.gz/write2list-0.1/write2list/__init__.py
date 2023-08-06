def create(*dataTuple):
    try:
        response=[]
        response.insert(0, dataTuple[0])
        response.extend(dataTuple[1])
        response.insert(len(response),"</td><td style='vertical-align:top'>")
        response.extend(dataTuple[2])        
        response.insert(len(response),"</td></tr></table>")
        response.insert(len(response), "<small><i>NOTE: Language composition is a list of most used languages in my repositories. It is not a direct indication of my skill level.</i></small>")
        return response
    except Exception:
        return "Error: Cannot read the tuple. Please make sure you have entered the correct values."