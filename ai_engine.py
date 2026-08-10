import os
from dotenv import load_dotenv
from google import genai


# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY not found in .env file")


# =====================================
# Create Gemini Client
# =====================================

client = genai.Client(api_key=api_key)


# =====================================
# AI Startup Analyzer
# =====================================

def analyze_startup_idea(idea):

    prompt = f"""
You are an experienced startup consultant and investor.

Analyze the following startup idea professionally.

Return your response in the following format:

# Startup Summary

# Problem Statement

# Target Audience

# Unique Value Proposition

# Revenue Model

# Competitor Analysis

# SWOT Analysis

## Strengths:

## Weaknesses:

## Opportunities:

## Threats:

# MVP Features

# Startup Score

Give a realistic score out of 100.

# Recommendation

Give practical recommendations for improving the startup idea.

Startup Idea:
{idea}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        text = response.text

        # Remove unwanted Markdown code blocks
        text = text.replace("```markdown", "")
        text = text.replace("```", "")

        return text.strip()


    except Exception as e:

        error = str(e)


        # =====================================
        # Rate Limit / Quota Error
        # =====================================

        if "429" in error or "RESOURCE_EXHAUSTED" in error:

            if "PerDay" in error or "per day" in error.lower():

                return """
⚠️ Gemini Daily Quota Reached

The Gemini API daily quota for this project has been reached.

Please wait until the quota resets or check your
Google AI Studio Rate Limit page.

Your IdeaValidator application is working correctly.
"""

            else:

                return """
⚠️ Gemini Rate Limit Reached

The Gemini API has temporarily reached its
request or token limit.

Please wait a short time and try again.

Your IdeaValidator application is working correctly.
"""


        # =====================================
        # Invalid API Key
        # =====================================

        elif "API_KEY" in error or "PERMISSION_DENIED" in error:

            return """
❌ Invalid API Key

Please check your GEMINI_API_KEY inside the
.env file.
"""


        # =====================================
        # Model Not Found
        # =====================================

        elif "NOT_FOUND" in error:

            return """
❌ Gemini Model Unavailable

The selected Gemini model is currently unavailable
for this API project.

Please check the available models in Google AI Studio.
"""


        # =====================================
        # Internet / Connection Error
        # =====================================

        elif "getaddrinfo failed" in error:

            return """
❌ Internet Connection Error

Unable to connect to the Gemini API.

Please check your internet connection and try again.
"""


        # =====================================
        # Unknown Error
        # =====================================

        else:

            return f"""
❌ Unexpected Error

{error}
"""