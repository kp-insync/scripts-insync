import requests
import json
import concurrent.futures


def fetch_intent(url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    intent = response['result']['tested_results'][0]['intent']
    confidence_score = response['result']['tested_results'][0]['confidence_score']
    return intent, confidence_score


def fetch_all_intents(urls, payloads):
    with concurrent.futures.ThreadPoolExecutor() as exe:  # Correct instantiation
        futures = [exe.submit(fetch_intent, url, payload) for url, payload in zip(urls, payloads)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results


def main(utterance):
    urls = ['http://dev.ai.shopinsync.com:8123/get-intent/api/v1',
            'http://dev.ai.shopinsync.com:8089/get_intent_knowledgeai']
    payloads = [
        {
            "market": "us_kleenrite",
            "utterances": [f"{utterance}"]},
        {
            "market": "us_kleenrite_knowledgeai",
            "utterances": [f"{utterance}"]
        }
    ]
    results = fetch_all_intents(urls, payloads)
    for result in results:
        print(result)


if __name__ == '__main__':
    utt = input('Sentence: ')
    main(utt)
