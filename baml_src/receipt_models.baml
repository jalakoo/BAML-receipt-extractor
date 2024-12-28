class ReceiptItem {
  description string
  quantity int
  quantity_unit string? @description(#"
    Unit of measurement for the quantity.
    "#)
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
     currency_code string @description(#"
    ISO 4217 Currency code for the currency used in the transaction. Infer from address if no currency symbol, or common symbol used among different countries.
    "#)
  address string?
  payment_method string? @description(#"
    Method of payment used for the transaction.
    "#)
}
