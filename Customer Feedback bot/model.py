import json
from transformers import pipeline


model = pipeline("text-classification", model="./my_saved_model")

def classify_text(text):
    result = model(text)
    return {
        'label': result[0]['label'],
        'confidence': result[0]['score']
    }

def lambda_handler(event, context):
   
    if 'text' in event:
        
        text = event['text']
        prediction = classify_text(text)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'text': text,
                'prediction': prediction['label'],
                'confidence': round(prediction['confidence'], 3)
            })
        }

    elif 'texts' in event:
        
        texts = event['texts']
        results = []
        for text in texts:
            prediction = classify_text(text)
            results.append({
                'text': text,
                'prediction': prediction['label'],
                'confidence': round(prediction['confidence'], 3)
            })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'results': results
            })
        }
    
   
    return {
        'statusCode': 400,
        'body': json.dumps({
            'message': 'Invalid request. Provide either "text" or "texts" in the body.'
        })
    }
