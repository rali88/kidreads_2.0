import openai
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_bullet_points(age, topic, gender):
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a creative assistant who generates story ideas."
        },
        {
            "role": "user",
            "content": f"Generate bullet points for a story for a {age}-year-old about {topic} with a {gender} main character."
        }
    ])
    bullet_points = response.choices[0].message.content.strip().split('\n')
    return bullet_points

def generate_story_page(bullet_points, history, characters):
    prompt = f"Using the following bullet points and previous story context, generate a page of the story:\n\n"
    prompt += "\n".join(bullet_points)
    prompt += f"\n\nPrevious story context:\n{history}\n\nCharacters:\n"
    for character, description in characters.items():
        prompt += f"{character}: {description}\n"

    response = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a creative assistant who writes stories and generates illustrations."
        },
        {
            "role": "user",
            "content": prompt
        }
    ])
    story_page = response.choices[0].message.content.strip()

    illustration_prompt = f"Generate an illustration description for the following story content. Maintain consistency with previous illustrations:\n\n{story_page}\n\nCharacters:\n"
    for character, description in characters.items():
        illustration_prompt += f"{character}: {description}\n"

    illustration_response = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a creative assistant who generates illustration descriptions."
        },
        {
            "role": "user",
            "content": illustration_prompt
        }
    ])
    illustration = illustration_response.choices[0].message.content.strip()

    return story_page, illustration

def extract_characters_from_illustration(illustration):
    """
    Use LangChain with OpenAI to extract character descriptions from the illustration text.
    """
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    prompt_template = PromptTemplate(
        input_variables=["illustration"],
        template="""
        Extract the character descriptions from the following illustration text. 
        Return the characters and their descriptions in the format 'CharacterName: description'.

        Illustration Text:
        {illustration}
        """
    )
    prompt = prompt_template.format(illustration=illustration)
    response = llm.invoke(prompt)
    characters = {}

    for line in response.strip().split("\n"):
        if ": " in line:
            name, description = line.split(": ", 1)
            characters[name] = description.strip()

    return characters
