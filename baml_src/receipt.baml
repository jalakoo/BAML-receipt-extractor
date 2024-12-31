// MODELS
class ReceiptItem {
  description string
  quantity int
  quantity_unit string? @description(#"
    Unit of measurement for the quantity.
    "#)
  price float
}

class Receipt {
  line_items ReceiptItem[]
  total_amount float
  date string @description(#"
    Date of the transaction.
    "#)
  time string @description(#"
    Time of the transaction in 24-hour format.
    "#)

  business string @description(#"
    Name of the vendor or business that provided the receipt.
  "#)
     currency_code string @description(#"
    ISO 4217 Currency code for the currency used in the transaction. Infer from address if no currency symbol, or common symbol used among different countries.
    "#)
  address string?
  payment_method string? @description(#"
    Method of payment used for the transaction.
    "#)
}

// FUNCTIONS
function ExtractReceiptFromImage(img: image) -> Receipt {
    client CustomGPT4oMini
    prompt #"
        {{_.role("user")}}
        
        Extract details from this image of a receipt: {{ img }}

        The currency type may need to be inferred from the address info extracted. Example: 12345 Sunshine St, Sunnyville, CA 12345 is in the US, so return USD.

        {{ ctx.output_format }}
    "#
}

// TESTS
function ExtractReceiptFromText(raw_text: string) -> Receipt {
  client CustomGPT4oMini
  prompt #"
    Parse the following content for receipt details. The currency type may need to be inferred from the address info extracted.

    Content:
    ---
    {{raw_text}}
    ---

    {{ ctx.output_format }}
  "#
}


test Test_FRANCE_Receipt {
functions [ExtractReceiptFromImage]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735354709/france_receipt.png"
    }
  }
}

test Test_UK_Receipt {
functions [ExtractReceiptFromImage]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735354707/uk_receipt.png"
    }
  }
}

test Test_US_Receipt {
functions [ExtractReceiptFromImage]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735352823/US_receipt.png"
    }
  }
}

test Test_MEXICO_Receipt {
functions [ExtractReceiptFromImage]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735354706/mexico_receipt.png"
    }
  }
}

test Test_JAPAN_Receipt {
functions [ExtractReceiptFromImage]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735603428/receipt_japan_2_f3w0cl.png"
    }
  }
}

