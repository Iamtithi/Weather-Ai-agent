import os
import requests
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# 🔑 Set your API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyByAwruHci3v71MVsKwMlnxbtk3bFGb7Cc"
WEATHERSTACK_API_KEY = "your-weatherstack-api-key"

# 🌦️ Define weather function using Weatherstack
def get_weather(city: str) -> str:
    url = f"http://api.weatherstack.com/current?access_key=467d4690b238f028ae38413620d93e0e&query={city}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"⚠️ Error: {response.status_code} - {response.text}"

    data = response.json()

    if "current" not in data:
        return f"❌ Error from API: {data.get('error', {}).get('info', 'Unknown error')}"

    desc = data["current"]["weather_descriptions"][0]
    temp = data["current"]["temperature"]
    feels_like = data["current"]["feelslike"]
    humidity = data["current"]["humidity"]

    return (
        f"🌤️ The current weather in {city.title()} is '{desc}', "
        f"temperature: {temp}°C, feels like: {feels_like}°C, humidity: {humidity}%."
    )

# 🛠️ Wrap as a LangChain tool
weather_tool = Tool(
    name="Weather Lookup",
    func=get_weather,
    description="Get the current weather for a given city. Input should be the city name."
)

# 🧠 Use Gemini as the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# 🤖 Create the agent
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 🧪 Example query
while True:
    user_input = input("\n🌍 Enter a city name to check the weather (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    response = agent.run(f"What is the current weather in {user_input}?")
    print("\n🗨️ Agent Response:\n", response)
#response = agent.run("What's the weather like in buffalo right now?")
#print("\n🔎 Agent Response:\n", response)
