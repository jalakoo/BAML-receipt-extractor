# Receipt Data Extraction

Receipt data extraction using [BAML](https://www.boundaryml.com)

## Output data

See the baml_src/receipt.baml file for defining the structured output data model.

Sample final JSON output:

```
{
  "line_items": [
    {
      "description": "Regular Fuel",
      "quantity": 13,
      "quantity_unit": "gallons",
      "price": 53.09
    },
    {
      "description": "Car Wash",
      "quantity": 1,
      "quantity_unit": null,
      "price": 7.99
    }
  ],
  "total_amount": 61.08,
  "date": "12/27/24",
  "time": "11:38",
  "business": "Costco",
  "currency_code": "USD",
  "address": "2345 Fenton Pkwy, San Diego, CA  92108",
  "payment_method": "Citibank Visa"
}
```

## Usage

1. Save the .env.sample file as .env and fill in any API keys

2. Use the functions in the baml_util.py file to extract data from receipt images or urls of receipt images.

## Samples

See branches for encapsulating examples (ie FastAPI server)
