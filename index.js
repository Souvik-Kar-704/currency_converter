async function convertCurrency(amount, fromCurrency, toCurrency) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/convert/${amount}/${fromCurrency}/${toCurrency}`); //replace with your server address.
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