from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware #Import the CORS middleware

import requests

app = FastAPI()

# Add the CORS middleware to your application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your HTML file
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

def get_exchange_rates():
    """Fetches exchange rates from a reliable API."""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD") #using USD as base for simplicity
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        rates = data.get("rates", {})
        return rates
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exchange rates: {e}")
@app.get("/")
def read_root():
    return {"message": "hello world"}
@app.get("/convert/{amount}/{from_currency}/{to_currency}")
async def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Converts currency from one to another."""
    rates = get_exchange_rates()

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in rates or to_currency not in rates:
        raise HTTPException(status_code=400, detail="Invalid currency code(s).")

    try:
        usd_amount = amount / rates[from_currency] # convert from currency to USD
        converted_amount = usd_amount * rates[to_currency] #convert USD to target currency
        return {"amount": converted_amount, "currency": to_currency}

    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot convert from a currency with a zero exchange rate.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# Example JS fetch API code to call this API:

"""
async function convertCurrency(amount, fromCurrency, toCurrency) {
  try {
    const response = await fetch(`/convert/${amount}/${fromCurrency}/${toCurrency}`); //replace with your server address.
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error; // Rethrow to handle it in the calling function
  }
}

// Example usage:
async function handleConversion() {
  try {
    const amount = parseFloat(document.getElementById('amount').value);
    const fromCurrency = document.getElementById('fromCurrency').value;
    const toCurrency = document.getElementById('toCurrency').value;

    const result = await convertCurrency(amount, fromCurrency, toCurrency);
    document.getElementById('result').textContent = `${amount} ${fromCurrency} = ${result.amount.toFixed(2)} ${result.currency}`;
  } catch (error) {
    document.getElementById('result').textContent = 'Conversion failed. Check console for details.';
  }
}

// HTML Example:
/*

l*/

"""