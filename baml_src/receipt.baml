class ReceiptItem {
  description string
  quantity int
  price float
}

class Receipt {
  items ReceiptItem[]
  total_amount float
  date string @description(#"
    Date of the transaction.
    "#)
  time string @description(#"
    Time of the transaction.
    "#)

  business string @description(#"
    Name of the vendor or business that provided the receipt.
  "#)
     currency_type string @description(#"
    Currency used in the transaction. Default USD
    "#)
  address string?
  payment_method string? @description(#"
    Method of payment used for the transaction.
    "#)
}


function ExtractReceiptDetails(img: image) -> Receipt {
    client CustomGPT4oMini
    prompt #"
        {{_.role("user")}}
        Describe this image: {{ img }}
    "#
}


test Test_FRANCE_Receipt {
functions [ExtractReceiptDetails]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735354709/france_receipt.png"
    }
  }
}

test Test_UK_Receipt {
functions [ExtractReceiptDetails]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735354707/uk_receipt.png"
    }
  }
}

test Test_US_Receipt {
functions [ExtractReceiptDetails]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735352823/Screenshot_2024-12-27_at_5.28.33_PM_q7s230.png"
    }
  }
}

test Test_MEXICO_Receipt {
functions [ExtractReceiptDetails]
  args {
    img {
      url "https://res.cloudinary.com/dqjkf4zsf/image/upload/v1735354706/mexico_receipt.png"
    }
  }
}


