```mermaid
graph LR

    Client[Pelanggan]
    APIGW[API Gateway]

    OrderSvc[Modul Pesanan]
    PaymentSvc[Modul Pembayaran]
    RestoSvc[Modul Katalog Resto]
    NotifSvc[Modul Kurir dan Notifikasi]

    Broker[(Message Broker)]

    Client -->|HTTP Request| APIGW
    APIGW -->|Buat Pesanan| OrderSvc

    OrderSvc -->|Request Pembayaran (Sinkron)| PaymentSvc

    OrderSvc -->|Publish OrderCreated| Broker
    PaymentSvc -->|Publish PaymentSuccess| Broker

    Broker -->|Subscribe Event| RestoSvc
    Broker -->|Subscribe Event| NotifSvc
```

