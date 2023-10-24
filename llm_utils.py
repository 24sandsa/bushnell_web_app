import openai
from colorama import Fore, Style

openai.organization = ""
openai.api_key = "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"
model_id = "gpt-3.5-turbo"
MAX_CONTEXT_QUESTIONS = 10


# Generate GPT-3.5 Turbo Response
# FIXME 7/5/23: Recall capablities not working yet


def generateResponse(prompt, persona):

    messages = [{"role": "system",
                 "content": f"You are {persona}, you will respond as if you were {persona}"}]
    
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=model_id,
        messages=messages,
    )
    return response['choices'][0]['message']['content']

# For filtration of harmful content in any text based prompt





def moderation_filter(prompt):
    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail."
    }

    mod_response = openai.Moderation.create(input=prompt)

    if mod_response.results[0].flagged:
        return str(mod_response)

# For image generation from DALL-E


def get_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']


def get_embeddings(input):
    response = openai.Embedding.create(
        model='text-embedding-ada-002',
        input=input
    )
    return response


def run():
    print(Fore.GREEN + f"CLI using the {model_id} model from OpenAI")
    print(Fore.GREEN + "Image generation using the DALL-E model from OpenAI")
    switch = input("Text(0), Image(1), Embedding(2): ")

    if switch == "0":
        persona = input(Style.NORMAL + Fore.CYAN + "Enter Model Persona: ")
        while True:
            prompt = input(Style.NORMAL + Fore.CYAN + "Prompt: ")

            try:

                if moderation_filter(prompt) == None:
                    previous_QA = []
                    print(Fore.GREEN + "Moderation Filter Detects no Harmful Content")
                    print()
                    print(f"{persona} says: " + Style.BRIGHT +
                          Fore.YELLOW + generateResponse(prompt, persona, previous_QA))
                    print()

                else:
                    print(Fore.RED + "Prompt Contains Harmful Content, Log Below:")
                    print(Fore.RED + moderation_filter(prompt))

            except (openai.error.AuthenticationError):
                print(Fore.RED + "Missing API Key or Other Auth Error")

    elif switch == "1":
        try:
            img_prompt = input("Prompt: ")

            if moderation_filter(img_prompt) == None:
                print(Style.BRIGHT + Fore.YELLOW +
                      f"Image URL at {get_image(img_prompt)}")
            else:
                print(
                    Fore.RED + "Primary Moderation Filter Detects Harmful Prompting \n Log Below: ")
                print(Fore.RED + moderation_filter(img_prompt))

        except (openai.error.AuthenticationError):
            print(Fore.RED + "Missing API Key or Other Auth Error")
    elif switch == '2':
        embed = input('Enter string to embed: ')
        print(get_embeddings(embed))
