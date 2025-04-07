import os
from openai import OpenAI, AsyncOpenAI


def get_api_client(vendor: str = "openai"):
    """

    Get the API client for the specified vendor.
    Args:
        vendor (str): The vendor name. Supported values are "openai" and "google".
    Returns:
        OpenAI: An instance of the OpenAI client.
    Raises:
        ValueError: If the vendor is not supported or if the API key is not set.
        
    """
    
    if vendor.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        return OpenAI(api_key=api_key)
    elif vendor.lower() == "google" or vendor.lower() == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        base_url = os.getenv("GEMINI_BASE_URL")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
        return OpenAI(api_key=api_key, base_url=base_url)
        
    else:
        raise ValueError(f"Unsupported vendor: {vendor}")
    
async def get_api_async_client(vendor: str = "openai"):
    """
    Get the API client for the specified vendor.
    Args:
        vendor (str): The vendor name. Supported values are "openai" and "google".
    Returns:
        OpenAI: An instance of the OpenAI client.
    Raises:
        ValueError: If the vendor is not supported or if the API key is not set.
        
    """
    
    if vendor.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        return AsyncOpenAI(api_key=api_key)
    elif vendor.lower() == "google" or vendor.lower() == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        base_url = os.getenv("GEMINI_BASE_URL")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
        return AsyncOpenAI(api_key=api_key, base_url=base_url)
        
    else:
        raise ValueError(f"Unsupported vendor: {vendor}")