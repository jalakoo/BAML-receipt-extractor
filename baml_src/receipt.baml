function ExtractReceiptFromImage(img: image) -> Receipt {
    client CustomGPT4oMini
    prompt #"
        {{_.role("user")}}
        
        Extract details from this image of a receipt: {{ img }}

        The currency type may need to be inferred from the address info extracted. Example: 12345 Sunshine St, Sunnyville, CA 12345 is in the US, so return USD.

        {{ ctx.output_format }}
    "#
}


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


